# GPU Ground-Truth Benchmarks

Collects **actual GPU execution timings** for standard transformer workloads using PyTorch/CUDA directly. These measurements are **tool-independent** and serve as ground truth to compare against performance prediction tool estimates (NeuSight, ASTRA-sim, VIDUR, etc.).

## Purpose

Performance prediction tools estimate metrics like kernel latency, throughput, and memory usage. To evaluate their accuracy, we need ground-truth measurements from real hardware. These scripts measure actual execution times for the fundamental operations that compose transformer models:

| Benchmark | What it measures | Why it matters |
|-----------|-----------------|----------------|
| `gemm_benchmark.py` | Matrix multiplication at transformer-relevant sizes | Core compute primitive; QKV projections, FFN layers |
| `attention_benchmark.py` | Multi-head scaled dot-product attention | Most memory-bound operation; prefill vs decode |
| `ffn_benchmark.py` | Feed-forward network layers (LLaMA SiLU, GPT GELU) | Compute-bound layers with activation functions |
| `forward_pass_benchmark.py` | Full transformer decoder blocks (attention + FFN + norm) | End-to-end layer timing including all overheads |

## Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| GPU | NVIDIA A100 (40GB) | NVIDIA H100 SXM (80GB) |
| CUDA | 12.0+ | 12.2+ |
| PyTorch | 2.0+ | 2.2+ |
| Python | 3.10+ | 3.10+ |

## Quick Start

```bash
cd scripts/gpu_experiments/ground_truth/

# Run all benchmarks (default: fp16)
./run_all.sh

# Run with a specific dtype
./run_all.sh --dtype bf16

# Run individual benchmarks
python3 gemm_benchmark.py --dtype fp16 --iters 100
python3 attention_benchmark.py --dtype fp16
python3 ffn_benchmark.py --dtype bf16
python3 forward_pass_benchmark.py --dtype fp16
```

## Output

Each benchmark produces JSON and CSV files in `results/`:

```
results/
├── gemm_fp16.json           # GEMM timings + GPU info
├── gemm_fp16.csv            # Same data in CSV
├── attention_fp16.json
├── attention_fp16.csv
├── ffn_fp16.json
├── ffn_fp16.csv
├── forward_pass_fp16.json
└── forward_pass_fp16.csv
```

### JSON output format

```json
{
  "benchmark": "gemm",
  "gpu_info": {
    "gpu_name": "NVIDIA H100 SXM",
    "gpu_memory_gb": 80.0,
    "cuda_version": "12.2",
    "pytorch_version": "2.2.0"
  },
  "timestamp": "2026-02-18T12:00:00+0000",
  "results": [
    {
      "M": 1024, "K": 4096, "N": 12288,
      "median_ms": 0.1234,
      "mean_ms": 0.1256,
      "min_ms": 0.1201,
      "tflops": 82.5
    }
  ]
}
```

## Workload Configurations

### GEMM sizes
Derived from real transformer model dimensions (7B, 13B, 70B parameter models):
- QKV projections: `(batch*seq, hidden, 3*hidden)`
- FFN up-projection: `(batch*seq, hidden, 4*hidden)`
- Single-token decode: `(1, hidden, ...)`

### Attention configs
- **Prefill**: Processing full prompts (seq_len = 512, 1024, 2048)
- **Decode**: Generating tokens one at a time (seq_len = 1, varying batch)
- Model sizes: 7B (32 heads), 13B (40 heads), 70B (64 heads)

### FFN configs
- LLaMA-style: gate + up projection with SiLU activation
- GPT-style: single projection with GELU activation
- Both prefill and decode scenarios

### Forward pass configs
- Single transformer block and stacked layers (4, 8)
- Full decoder block: RMSNorm -> attention -> residual -> RMSNorm -> FFN -> residual

## Comparing Against Tool Predictions

After collecting ground-truth timings, compare them to tool predictions:

1. **GEMM latency**: Compare `gemm_fp16.csv` median_ms against NeuSight kernel predictions
2. **Attention latency**: Compare `attention_fp16.csv` against FlashAttention estimates
3. **End-to-end layer time**: Compare `forward_pass_fp16.csv` against full-model prediction tools
4. **Memory usage**: Compare `peak_mem_mb` values against tool memory estimates

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `nvidia-smi` not found | Install NVIDIA driver: `sudo apt install nvidia-driver-535` |
| `torch.cuda.is_available()` returns False | Reinstall PyTorch with CUDA: `pip install torch --index-url https://download.pytorch.org/whl/cu121` |
| Out of GPU memory | Reduce `--iters` or skip large configs |
| `RMSNorm` not found | Requires PyTorch >= 2.4; use `LayerNorm` fallback or upgrade |
