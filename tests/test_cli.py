import pytest
from click.testing import CliRunner
from conftest import FIXTURE_DIR_INTERNAL

from fast_sync.cli.main import fast_sync_cli


@pytest.mark.cli
@pytest.mark.parametrize("direction", ["left", "right"])
def test_missing(direction):
    runner = CliRunner()
    result = runner.invoke(
        fast_sync_cli,
        [
            "missing",
            "-l",
            f"{(FIXTURE_DIR_INTERNAL / 'Simple1')}",
            "-r",
            f"{(FIXTURE_DIR_INTERNAL / 'Simple2')}",
            direction,
        ],
    )
    assert result.exit_code == 0


@pytest.mark.cli
def test_duplicates():
    runner = CliRunner()
    result = runner.invoke(
        fast_sync_cli,
        [
            "duplicates",
            "-f",
            f"{(FIXTURE_DIR_INTERNAL / 'TestEqual')}",
            "resolve",
        ],
    )
    assert result.exit_code == 1


@pytest.mark.cli
@pytest.mark.parametrize("commands", ["sync", "missing", "duplicates"])
def test_view_help(commands):
    runner = CliRunner()
    result = runner.invoke(
        fast_sync_cli,
        [
            "view-help",
            commands,
        ],
    )
    assert result.exit_code == 0
