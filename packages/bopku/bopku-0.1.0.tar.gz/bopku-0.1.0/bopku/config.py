from __future__ import annotations
import os.path
import json
from dacite import from_dict
from dataclasses import asdict, dataclass


def get_config_dir() -> str:
    """Returns the default directory for the Store.  This is intentionally
    underscored to indicate that `Store.get_default_directory` is the intended
    way to get this information.  This is also done so
    `Store.get_default_directory` can be mocked in tests and
    `get_config_dir` can be tested.
    """
    ret = os.environ.get("BOPKU_HOME") or os.path.join(
        os.environ.get("XDG_CACHE_HOME") or os.path.expanduser("~/.cache"),
        "bopku",
    )
    return os.path.realpath(ret)


CONFIG_DIR = get_config_dir()


def join(to: str, fr: str = CONFIG_DIR) -> str:
    return os.path.join(fr, to)


if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(join("README"), "w") as f:
        f.write("Folder ini diatur oleh aplikasi bopku.\n")

CONFIG_FILEPATH = join("config.json")


@dataclass
class Config:
    app: str = "bopku"
    directory: str = CONFIG_DIR
    database_uri: str = os.environ.get(
        "DATABASE_URL", "sqlite:///" + join("app.sqlite")
    )
    session: int = 1


config = Config()

if not os.path.isfile(CONFIG_FILEPATH):
    with open(CONFIG_FILEPATH, "w") as json_file:
        json.dump(asdict(config), json_file)
else:
    with open(CONFIG_FILEPATH, "r") as json_file:
        config = from_dict(Config, json.load(json_file))
