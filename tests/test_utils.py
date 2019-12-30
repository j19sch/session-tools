import pytest
from session_noter.utils import validate_config_file


def test_config_validation_duplicate_command():
    config = {
        "note_types": [
            {"type": "question", "command": "q"},
            {"type": "also_question", "command": "q"},
        ]
    }
    with pytest.raises(
        SystemExit, match="Duplicate command in config.yml: also_question"
    ):
        validate_config_file(config)


def test_config_validation_no_duplicate_command():
    config = {
        "note_types": [
            {"type": "question", "command": "q"},
            {"type": "issue", "command": "i"},
        ]
    }

    validate_config_file(config)
