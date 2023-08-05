from pathlib import Path
from typing import Dict, List

from cerberus import Validator
from ruamel.yaml import YAML

import cognite.airworkflow.util.convert_string_times as window_size
import cognite.airworkflow.util.cron as cron
from cognite.airworkflow.model.config import Config


def write_yaml(path: Path, content: Dict, *, create_dirs: bool = False) -> None:
    if create_dirs:
        path.parent.mkdir(exist_ok=True)
    YAML(typ="safe").dump(content, path)


def load_yaml(path: Path) -> Dict:
    yaml = YAML(typ="safe").load(path)
    assert isinstance(yaml, dict)
    return yaml


def get_validator(schema_path: Path) -> Validator:
    schema = load_yaml(schema_path)
    validator = Validator(schema)
    return validator


def load_and_validate(path: Path, schema_path: Path) -> Config:
    yaml = load_yaml(path)
    validator = get_validator(schema_path)
    is_valid = validator.validate(yaml)
    if not is_valid:
        raise ValueError(f"Malformed file, {path} \n {validator.errors}")

    if "schedule" in yaml:
        cron.validate_and_update_cron(yaml, path)
        window_size.window_size_update(yaml)

    return Config(yaml)


def load_and_validate_multiple(paths: List[Path], schema_path: Path) -> Dict[Path, Config]:
    return {p.parent.parent: load_and_validate(p, schema_path) for p in paths}
