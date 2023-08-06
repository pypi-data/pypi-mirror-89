from __future__ import annotations

from enum import Enum
import json
import os
from pathlib import Path, PurePath
from shutil import copytree, ignore_patterns
from tempfile import gettempdir

import click
from loguru import logger
from pydantic import BaseSettings as _BaseConfig, Field, PydanticValueError, validator

from .utils import trash


class _PathNotWritableDirectoryError(PydanticValueError):
    code = 'path.not_writable_directory'
    msg_template = '"{path}" is not a writable directory'


_default_profile = '__default__'
_novalidate = '__novalidate__'


def _get_default_config_dir() -> Path:
    return Path(click.get_app_dir('instawow'))


def _validate_expand_path(value: Path) -> Path:
    try:
        return value.expanduser().resolve()
    except RuntimeError as error:
        # pathlib will raise a ``RuntimeError`` for non-existent ~users
        raise ValueError(str(error)) from error


def _validate_path_is_writable_dir(value: Path) -> Path:
    if not (value.is_dir() and os.access(value, os.W_OK)):
        raise _PathNotWritableDirectoryError(path=value)

    return value


class BaseConfig(_BaseConfig):
    class Config:  # type: ignore
        env_prefix = 'INSTAWOW_'

    def _build_values(
        self, init_kwargs: dict[str, object], *args: object, **kwargs: object
    ) -> dict[str, object]:
        # Prioritise env vars
        return {**init_kwargs, **self._build_environ()}


class Flavour(str, Enum):
    retail = 'retail'
    classic = 'classic'


class GlobalConfig(BaseConfig):
    config_dir: Path = Field(default_factory=_get_default_config_dir)
    profile: str = Field(_default_profile, min_length=1, strip_whitespace=True)
    addon_dir: Path
    game_flavour: Flavour
    auto_update_check: bool = True
    temp_dir: Path = Path(gettempdir(), 'instawow')

    @validator('config_dir', 'addon_dir', 'temp_dir')
    def _validate_expand_path(cls, value: Path) -> Path:
        return _validate_expand_path(value)

    @validator('addon_dir')
    def _validate_path_is_writable_dir(cls, value: Path) -> Path:
        if value.name == _novalidate:
            return value
        return _validate_path_is_writable_dir(value)

    @staticmethod
    def is_classic_folder(folder: os.PathLike[str]) -> bool:
        tail = PurePath(folder).parts[-3:]
        return tuple(map(str.casefold, tail)) in {
            ('_classic_', 'interface', 'addons'),
            ('_classic_ptr_', 'interface', 'addons'),
        }

    @classmethod
    def get_dummy_config(cls, **kwargs: object) -> GlobalConfig:
        "Create a dummy configuration with default values."
        template = {'game_flavour': Flavour.retail, 'addon_dir': _novalidate}
        dummy_config = cls.parse_obj({**template, **kwargs})
        return dummy_config

    @classmethod
    def list_profiles(cls) -> list[str]:
        "List the profiles contained in ``config_dir``."
        dummy_config = cls.get_dummy_config()
        profiles = [c.parent.name for c in dummy_config.config_dir.glob('profiles/*/config.json')]
        return profiles

    @classmethod
    def read(cls, profile: str) -> GlobalConfig:
        "Read the configuration from disk."
        dummy_config = cls.get_dummy_config(profile=profile)
        dummy_config.migrate_legacy_dirs()
        config = cls.parse_raw(dummy_config.config_file.read_text(encoding='utf-8'))
        if dummy_config.profile != config.profile:
            raise ValueError(
                'profile location does not match profile value of '
                f'"{config.profile}" in {dummy_config.config_file}'
            )
        return config

    def ensure_dirs(self) -> GlobalConfig:
        "Create the various folders used by instawow."
        for dir_ in (
            self.config_dir,
            self.profile_dir,
            self.logging_dir,
            self.plugin_dir,
            self.temp_dir,
            self.cache_dir,
        ):
            dir_.mkdir(exist_ok=True, parents=True)
        return self

    def write(self) -> GlobalConfig:
        """Write the configuration on disk.

        ``write``, unlike ``ensure_dirs``, should only be called when configuring
        instawow.  This means that environment overrides should only be persisted
        if made during configuration.
        """
        self.ensure_dirs()
        includes = {'addon_dir', 'game_flavour', 'profile'}
        output = self.json(include=includes, indent=2)
        self.config_file.write_text(output, encoding='utf-8')
        return self

    def migrate_legacy_dirs(self) -> GlobalConfig:
        "Migrate a profile-less configuration to the new format."
        legacy_config_file = self.config_dir / 'config.json'
        if (
            self.profile == _default_profile
            and not self.profile_dir.exists()
            and legacy_config_file.exists()
        ):
            legacy_json = json.loads(legacy_config_file.read_text(encoding='utf-8'))
            legacy_json.pop('profile', None)
            legacy_config = self.parse_obj(legacy_json)
            ignores = ignore_patterns('profiles')

            logger.info('migrating legacy configuration')
            copytree(self.config_dir, self.profile_dir, ignore=ignores)
            legacy_config.write()
            trash(
                [i for i in self.config_dir.iterdir() if i.name != 'profiles'], dest=self.temp_dir
            )

        return self

    def delete(self) -> None:
        "Delete the configuration files associated with this profile."
        trash((self.profile_dir,), dest=self.temp_dir, missing_ok=True)

    @property
    def is_classic(self) -> bool:
        return self.game_flavour is Flavour.classic

    @property
    def is_retail(self) -> bool:
        return self.game_flavour is Flavour.retail

    @property
    def profile_dir(self) -> Path:
        return self.config_dir / 'profiles' / self.profile

    @property
    def logging_dir(self) -> Path:
        return self.profile_dir / 'logs'

    @property
    def plugin_dir(self) -> Path:
        return self.profile_dir / 'plugins'

    @property
    def config_file(self) -> Path:
        return self.profile_dir / 'config.json'

    @property
    def db_file(self) -> Path:
        return self.profile_dir / 'db.sqlite'

    @property
    def cache_dir(self) -> Path:
        return self.temp_dir / 'cache'


Config = GlobalConfig


def setup_logging(config: GlobalConfig, log_level: str = 'INFO') -> int:
    import logging

    class InterceptHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            # Get the corresponding Loguru level if it exists
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find caller from where the logged message originated
            frame = logging.currentframe()
            depth = 2
            while frame and frame.f_code.co_filename == getattr(logging, '__file__', None):
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

    logging.basicConfig(handlers=[InterceptHandler()], level=log_level)
    handler = {
        'sink': config.logging_dir / 'error.log',
        'level': log_level,
        'rotation': '1 MB',
        'enqueue': True,
    }
    (handler_id,) = logger.configure(handlers=(handler,))
    return handler_id
