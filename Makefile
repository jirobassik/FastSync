compile:
	uv run pyinstaller fast_sync.py --distpath "compiled/dist" --workpath "compiled/build" --specpath "compiled" --onefile --name fs

ruff:
	uv run ruff check .
	uv run ruff format . --exclude "fast_sync/cli/main.py" --check

pytest:
	uv run pytest tests -m "not big" tests/test_path_setup.py tests/test_sync_manager.py