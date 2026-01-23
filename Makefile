compile:
	uv run pyinstaller fast_sync.py --distpath "compiled/dist" --workpath "compiled/build" --specpath "compiled" --onefile --name fs