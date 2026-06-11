# ── Base image ────────────────────────────────────────────────────────────────
# python:3.11-slim is a minimal Debian image with Python pre-installed.
# "slim" keeps the image size small by removing non-essential packages.
FROM python:3.11-slim

# ── Working directory ─────────────────────────────────────────────────────────
# All subsequent commands run inside /app.
# The project folder is mounted here at runtime via docker-compose volumes.
WORKDIR /app

# ── System dependencies ───────────────────────────────────────────────────────
# build-essential   — compilers needed by some Python packages (e.g. tokenizers)
# curl              — useful for health checks and debugging inside the container
# We clean up the apt cache in the same layer to keep the image lean.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
    && rm -rf /var/lib/apt/lists/*

# ── Python dependencies ───────────────────────────────────────────────────────
# Copy only requirements.txt first so Docker can cache this layer.
# The expensive pip install step is skipped on rebuild if requirements.txt
# has not changed — even if your code has.
COPY requirements.txt .

# Install CUDA-enabled PyTorch *before* the rest of requirements so that
# sentence-transformers picks up the GPU build instead of the CPU-only default.
# cu128 = CUDA 12.8 — required for RTX 5070 Ti (Blackwell sm_120). cu124 only goes up to sm_90.
# If the GPU is unavailable at runtime PyTorch falls back to CPU automatically.
# --timeout 600: PyTorch CUDA wheel is ~768 MB; default timeout of 60s is too short.
# --retries 5: retry on transient network failures.
RUN pip install --no-cache-dir --timeout 600 --retries 5 \
    torch \
    --index-url https://download.pytorch.org/whl/cu128

RUN pip install --no-cache-dir -r requirements.txt

# ── Default command ───────────────────────────────────────────────────────────
# Each service in docker-compose.yml overrides this with its own command.
CMD ["bash"]
