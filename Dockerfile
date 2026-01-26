FROM astral/uv:python3.13-alpine
LABEL authors="jirobassik"

RUN apk update && apk add --no-cache bash && apk add binutils

# Disable development dependencies
ENV UV_NO_DEV=1

WORKDIR /FastSync
COPY . .

RUN uv sync --locked
RUN uv run pyinstaller fast_sync.py --distpath "compiled/dist" --workpath "compiled/build" --specpath "compiled" --onefile --name fs

RUN cp /FastSync/compiled/dist/fs /usr/local/bin/

ENTRYPOINT ["bash"]