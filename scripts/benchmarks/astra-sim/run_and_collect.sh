#!/bin/bash
# ASTRA-sim ResNet-50 Orchestration Script
# Builds Docker image, runs simulations, and collects results
#
# Usage: bash scripts/benchmarks/astra-sim/run_and_collect.sh
#
# For ML Performance Survey - Issue #170
# Author: Flux (Tool Engineer)

set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
PROJECT_ROOT=$(cd "${SCRIPT_DIR}/../../.." && pwd)
RESULTS_DIR="${PROJECT_ROOT}/data/results/astra-sim"
IMAGE_NAME="mlperf-astra-sim"
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
RUN_ID=$(date +%Y%m%d_%H%M%S)
RUN_DIR="${RESULTS_DIR}/${RUN_ID}"

mkdir -p "${RUN_DIR}"

log() {
    echo "[$(date -u +%H:%M:%S)] $*" | tee -a "${RUN_DIR}/orchestrator.log"
}

# --- Step 1: Build Docker image ---
log "=== Phase 1: Docker Build ==="
log "Building ${IMAGE_NAME} from ${SCRIPT_DIR}/Dockerfile"

if docker build -t "${IMAGE_NAME}" "${SCRIPT_DIR}" 2>&1 | tee "${RUN_DIR}/docker_build.log"; then
    log "Docker build succeeded"
else
    log "ERROR: Docker build failed. See ${RUN_DIR}/docker_build.log"
    exit 1
fi

# --- Step 2: Verify binary exists ---
log "=== Phase 2: Verify Build ==="
if docker run --rm "${IMAGE_NAME}" test -f /app/astra-sim/build/astra_analytical/build/bin/AstraSim_Analytical_Congestion_Aware; then
    log "Binary verified: AstraSim_Analytical_Congestion_Aware"
else
    log "ERROR: Binary not found after build"
    exit 1
fi

# --- Step 3: Run microbenchmarks (sanity check) ---
log "=== Phase 3: Microbenchmark Sanity Check ==="
docker run --rm \
    -v "${RUN_DIR}:/app/results" \
    "${IMAGE_NAME}" \
    bash -c '/app/astra-sim/build/astra_analytical/build/bin/AstraSim_Analytical_Congestion_Aware \
        --workload-configuration=/app/astra-sim/examples/workload/microbenchmarks/all_reduce/8npus_1MB/all_reduce \
        --system-configuration=/app/astra-sim/examples/system/native_collectives/HGX-H100-validated.json \
        --network-configuration=/app/astra-sim/examples/network/analytical/HGX-H100-validated.yml \
        --remote-memory-configuration=/app/astra-sim/examples/remote_memory/analytical/no_memory_expansion.json \
        2>&1' | tee "${RUN_DIR}/microbench_all_reduce_8npus.log"

if [ ${PIPESTATUS[0]} -eq 0 ]; then
    log "Microbenchmark passed"
else
    log "WARNING: Microbenchmark failed (non-fatal, continuing)"
fi

# --- Step 4: Run ResNet-50 simulation ---
log "=== Phase 4: ResNet-50 Simulation ==="
docker run --rm \
    -v "${RUN_DIR}:/app/results" \
    "${IMAGE_NAME}" \
    bash /app/run_resnet50.sh 2>&1 | tee "${RUN_DIR}/resnet50_full.log"

if [ ${PIPESTATUS[0]} -eq 0 ]; then
    log "ResNet-50 simulation completed"
else
    log "WARNING: ResNet-50 simulation had errors (check logs)"
fi

# --- Step 5: Collect and summarize results ---
log "=== Phase 5: Results Summary ==="
log ""
log "Run ID: ${RUN_ID}"
log "Timestamp: ${TIMESTAMP}"
log "Results directory: ${RUN_DIR}"
log ""
log "Files generated:"
ls -la "${RUN_DIR}/" 2>/dev/null | tee -a "${RUN_DIR}/orchestrator.log"
log ""

# Extract key metrics from logs
log "=== Key Metrics ==="
for logfile in "${RUN_DIR}"/*.log; do
    [ ! -f "$logfile" ] && continue
    name=$(basename "$logfile")
    if grep -qiE "(sys\[|total|finish|tick)" "$logfile" 2>/dev/null; then
        log "--- ${name} ---"
        grep -iE "(sys\[|total|finish|tick)" "$logfile" | tail -10 | tee -a "${RUN_DIR}/orchestrator.log"
        log ""
    fi
done

log "=== Done ==="
log "To view results: ls ${RUN_DIR}/"
log "To re-run: bash ${SCRIPT_DIR}/run_and_collect.sh"
