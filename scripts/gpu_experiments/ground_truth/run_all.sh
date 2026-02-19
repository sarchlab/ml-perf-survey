#!/bin/bash
# Ground-truth GPU benchmark suite.
#
# Collects actual GPU execution timings for standard transformer workloads.
# These measurements are tool-independent and serve as ground truth to
# compare against performance prediction tool estimates.
#
# Requirements: NVIDIA GPU, CUDA 12.x, PyTorch 2.x with CUDA support
#
# Usage:
#   ./run_all.sh              # Run all benchmarks with defaults (fp16)
#   ./run_all.sh --dtype bf16 # Run all benchmarks in bfloat16
#   ./run_all.sh --help       # Show options

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTS_DIR="${SCRIPT_DIR}/results"
DTYPE="${1:-fp16}"

# Strip leading -- from dtype if passed as --dtype value
if [[ "$DTYPE" == "--dtype" ]]; then
    DTYPE="${2:-fp16}"
elif [[ "$DTYPE" == "--help" ]] || [[ "$DTYPE" == "-h" ]]; then
    echo "Usage: $0 [--dtype fp16|fp32|bf16]"
    echo ""
    echo "Runs all ground-truth GPU benchmarks and saves results to results/"
    echo ""
    echo "Benchmarks:"
    echo "  gemm_benchmark.py         - Matrix multiplication (GEMM) at various sizes"
    echo "  attention_benchmark.py    - Multi-head attention (prefill + decode)"
    echo "  ffn_benchmark.py          - Feed-forward network layers"
    echo "  forward_pass_benchmark.py - Full transformer block forward pass"
    exit 0
fi

mkdir -p "$RESULTS_DIR"

echo "============================================="
echo " GPU Ground-Truth Benchmark Suite"
echo "============================================="
echo ""

# Check GPU availability
if ! python3 -c "import torch; assert torch.cuda.is_available(), 'No GPU'" 2>/dev/null; then
    echo "ERROR: No CUDA GPU detected. These benchmarks require an NVIDIA GPU."
    echo "Check: nvidia-smi, nvcc --version, python3 -c 'import torch; print(torch.cuda.is_available())'"
    exit 1
fi

python3 -c "
import torch
props = torch.cuda.get_device_properties(0)
print(f'GPU: {props.name} ({props.total_mem / (1024**3):.1f} GB)')
print(f'CUDA: {torch.version.cuda}, PyTorch: {torch.__version__}')
print(f'GPU Count: {torch.cuda.device_count()}')
"

echo ""
echo "Data type: $DTYPE"
echo "Results directory: $RESULTS_DIR"
echo ""

BENCHMARKS=(
    "gemm_benchmark.py:GEMM (Matrix Multiply)"
    "attention_benchmark.py:Multi-Head Attention"
    "ffn_benchmark.py:Feed-Forward Network"
    "forward_pass_benchmark.py:Transformer Forward Pass"
)

FAILED=0
for entry in "${BENCHMARKS[@]}"; do
    script="${entry%%:*}"
    name="${entry##*:}"

    echo "============================================="
    echo " Running: $name"
    echo "============================================="
    echo ""

    if python3 "${SCRIPT_DIR}/${script}" --dtype "$DTYPE" --output-dir "$RESULTS_DIR"; then
        echo ""
        echo "  -> $name DONE"
    else
        echo ""
        echo "  -> $name FAILED"
        FAILED=$((FAILED + 1))
    fi
    echo ""
done

echo "============================================="
echo " Summary"
echo "============================================="
echo "Results saved to: $RESULTS_DIR/"
ls -la "$RESULTS_DIR/"
echo ""

if [[ $FAILED -gt 0 ]]; then
    echo "WARNING: $FAILED benchmark(s) failed."
    exit 1
else
    echo "All benchmarks completed successfully."
fi
