FROM astral/uv:python3.13-alpine
LABEL authors="jirobassik"

RUN apk update && apk add --no-cache bash && apk add binutils

# Setup a non-root user
RUN addgroup -S -g 1000 nonroot && adduser -S -D -g 1000 -u 1000 nonroot

# Install the project into `/FastSync`
WORKDIR /FastSync

# Disable development dependencies
ENV UV_NO_DEV=1

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Ensure installed tools can be executed out of the box
ENV UV_TOOL_BIN_DIR=/usr/local/bin


# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project


# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
COPY . /FastSync
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked


# Generate executable file
RUN uv run pyinstaller fast_sync.py \
    --distpath "compiled/dist" \
    --workpath "compiled/build" \
    --specpath "compiled" \
    --onefile --name fs

# Copy executable file fast_sync in bin
RUN cp /FastSync/compiled/dist/fs /usr/local/bin/

# Use the non-root user to run our application
USER nonroot

ENTRYPOINT ["bash"]