import ast
import sys
from pathlib import Path

import pytest

from software360 import cli


def test_parser_accepts_supported_commands() -> None:
    parser = cli.build_parser()

    assert parser.parse_args(["show-config"]).command == "show-config"
    assert parser.parse_args(["generate-data"]).command == "generate-data"


def test_show_config_prints_validated_settings(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("S360_ENVIRONMENT", "test")
    monkeypatch.setenv("S360_CATALOG_PREFIX", "software360")
    monkeypatch.setattr(sys, "argv", ["software360", "show-config"])

    cli.main()

    output = ast.literal_eval(capsys.readouterr().out)
    assert output["environment"] == "test"
    assert output["catalog_prefix"] == "software360"


def test_invalid_command_shows_help_without_traceback(
    capsys: pytest.CaptureFixture[str],
) -> None:
    parser = cli.build_parser()

    with pytest.raises(SystemExit) as error:
        parser.parse_args(["invalid-command"])

    stderr = capsys.readouterr().err
    assert error.value.code == 2
    assert "usage: software360" in stderr
    assert "invalid choice" in stderr
    assert "Traceback" not in stderr
