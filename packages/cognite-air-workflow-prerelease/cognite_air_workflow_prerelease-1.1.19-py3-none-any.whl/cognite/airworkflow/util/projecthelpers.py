import os
from pathlib import Path
from typing import Dict, List, Set

from ruamel.yaml import YAML

import cognite.airworkflow.util.file as file
from cognite.airworkflow.util import env


def load_yaml(path: Path) -> Dict:
    yaml = YAML(typ="safe").load(path)
    assert isinstance(yaml, dict)
    return yaml


working_path = env.get_env_value("PWD")
ROOT_DIR = Path(working_path)
FUNCTIONS_PATH = ROOT_DIR / "functions"
IGNORE_MODELS_PATH = ROOT_DIR / ".ignore_models"

# Paths within a functions folder
FUNCTION_REL_PATH = Path("function")
FUNCTION_REL_CONFIG_PATH = FUNCTION_REL_PATH / "config.yaml"


def project_name_finder() -> Set:
    ignore_models = file.read_file_to_list(IGNORE_MODELS_PATH)

    directory_contents = os.listdir(FUNCTIONS_PATH)
    directory_paths: List = list(
        filter(lambda x: x not in ignore_models, directory_contents),
    )
    function_paths: List = [x for x in directory_paths if os.path.isfile(FUNCTIONS_PATH / x / FUNCTION_REL_CONFIG_PATH)]

    return set(function_paths)
