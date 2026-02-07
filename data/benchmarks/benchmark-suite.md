# Common Benchmark Suite for Tool Evaluation

This document defines a standardized benchmark suite for fairly comparing ML performance modeling tools. The suite is designed to cover diverse workload categories while remaining practical to execute across all surveyed tools.

---

## Design Principles

1. **Representativeness**: Workloads span major ML categories (CNN, Transformer, LLM, training)
2. **Practicality**: Benchmarks are runnable on available hardware without GPUs
3. **Fairness**: Same workloads used across all tools where applicable
4. **Reproducibility**: All configurations fully documented

---

## Benchmark Categories

### Category 1: CNN Inference

| Benchmark | Model | Input Shape | Ops (GFLOPs) | Params (M) | Rationale |
|-----------|-------|-------------|--------------|------------|-----------|
| CNN-1 | ResNet-50 | 1x3x224x224 | 4.1 | 25.6 | Industry standard, widely supported |
| CNN-2 | VGG-16 | 1x3x224x224 | 15.5 | 138 | Memory-bound baseline |
| CNN-3 | MobileNet-V2 | 1x3x224x224 | 0.3 | 3.4 | Edge deployment representative |

**Selection Rationale:**
- ResNet-50: Most benchmarked CNN, baseline for all accelerators
- VGG-16: High memory bandwidth requirements, stresses memory hierarchy
- MobileNet-V2: Depthwise separable convolutions, edge-focused

### Category 2: Transformer Inference

| Benchmark | Model | Seq Length | Ops (GFLOPs) | Params (M) | Rationale |
|-----------|-------|------------|--------------|------------|-----------|
| XFMR-1 | BERT-base | 128 | 11.2 | 110 | NLP baseline |
| XFMR-2 | BERT-base | 512 | 45 | 110 | Longer context stress test |
| XFMR-3 | ViT-B/16 | 224x224 | 17.6 | 86 | Vision transformer baseline |

**Selection Rationale:**
- BERT-base: Standard NLP workload, attention-dominant
- Variable sequence lengths test quadratic attention scaling
- ViT bridges vision and transformer domains

### Category 3: LLM Inference

| Benchmark | Model | Config | Prefill Tokens | Decode Tokens | Rationale |
|-----------|-------|--------|----------------|---------------|-----------|
| LLM-1 | Llama-2-7B | TP1 | 128 | 128 | Single-GPU baseline |
| LLM-2 | Llama-2-7B | TP1 | 2048 | 256 | Long context prefill |
| LLM-3 | Llama-2-70B | TP4 | 512 | 256 | Multi-GPU scaling |

**Selection Rationale:**
- Llama-2 models are well-profiled in VIDUR and widely used
- Covers both prefill-heavy and decode-heavy workloads
- Tests tensor parallelism scaling (TP1 vs TP4)

### Category 4: Distributed Training

| Benchmark | Workload | NPUs | Collective | Data Size | Rationale |
|-----------|----------|------|------------|-----------|-----------|
| DIST-1 | AllReduce | 8 | Ring | 1 MB | Basic collective |
| DIST-2 | AllReduce | 8 | Ring | 1 GB | Large gradient sync |
| DIST-3 | AllReduce | 32 | Tree | 1 GB | Scaling test |
| DIST-4 | AllGather | 8 | Ring | 256 MB | Attention parallel |

**Selection Rationale:**
- AllReduce dominates data-parallel training communication
- Size variation tests bandwidth vs latency regimes
- 8 and 32 NPU tests cover typical cluster sizes

---

## Hardware Configurations

### Configuration A: Single Accelerator (CPU-based simulation)

For tools that model accelerator architectures (Timeloop, MAESTRO):

| Component | Specification |
|-----------|--------------|
| Architecture | Eyeriss-like (spatial, weight-stationary) |
| PE Array | 16x16 MACs |
| Local SRAM | 128 KB (weights), 32 KB (activations) |
| Global Buffer | 1 MB |
| DRAM Bandwidth | 25 GB/s |

### Configuration B: Edge Device (for nn-Meter)

| Device | SoC | Predictor |
|--------|-----|-----------|
| Mobile CPU | Cortex-A76 | cortexA76cpu_tflite21 |
| Mobile GPU | Adreno 640 | adreno640gpu_tflite21 |

### Configuration C: GPU Cluster (for VIDUR, ASTRA-sim)

| Configuration | GPUs | Topology | Bandwidth |
|--------------|------|----------|-----------|
| Single Node | 8x A100 | NVSwitch | 600 GB/s |
| Multi Node | 4x8 A100 | NVLink + IB | 400 GB/s NVL, 200 Gb/s IB |

### Configuration D: HPC System (for ASTRA-sim)

| Configuration | NPUs | Topology |
|--------------|------|----------|
| HGX-H100 | 8 | Switch, 400 GB/s |
| DGX-V100 | 8 | Hybrid mesh |

---

## Workload Specifications

### CNN Workload Files

All CNN workloads specified in YAML (Timeloop format):

```yaml
# resnet50_conv1.yaml
problem:
  instance:
    C: 3      # Input channels
    M: 64     # Output channels
    P: 112    # Output height
    Q: 112    # Output width
    R: 7      # Filter height
    S: 7      # Filter width
    HStride: 2
    WStride: 2
```

Full layer definitions available in `workloads/cnn/`.

### Transformer Workload Specifications

BERT-base layer configuration:

| Layer Type | Dimensions | Notes |
|------------|-----------|-------|
| Self-Attention | (B, S, 768) -> (B, S, 768) | 12 heads |
| FFN-1 | (B, S, 768) -> (B, S, 3072) | 4x expansion |
| FFN-2 | (B, S, 3072) -> (B, S, 768) | Projection |

Where B=batch size, S=sequence length.

### LLM Workload Traces

For VIDUR, use included traces:

| Trace | Description | File |
|-------|-------------|------|
| Conversational | Short turns, variable length | splitwise_conv.csv |
| Code Generation | Longer outputs | splitwise_code.csv |
| Summarization | Long inputs, short outputs | arxiv_summarization_filtered_*.csv |

### Distributed Training Traces

For ASTRA-sim, use included Chakra traces:

| Trace | Location |
|-------|----------|
| AllReduce 8 NPU | examples/workload/microbenchmarks/all_reduce/8npus_1MB/ |
| AllGather 8 NPU | examples/workload/microbenchmarks/all_gather/8npus_1MB/ |

---

## Execution Methodology

### Phase 1: Tool Setup

1. Install each tool following documented procedures
2. Verify installation with provided examples
3. Record setup time and any issues encountered

### Phase 2: Workload Execution

For each (tool, benchmark) combination:

1. **Configure workload**: Use specifications above
2. **Execute prediction/simulation**: Record command and parameters
3. **Collect metrics**:
   - Primary: Latency/throughput prediction
   - Secondary: Energy (if available), memory usage
   - Meta: Prediction time, memory footprint

### Phase 3: Ground Truth Collection

Where hardware is available:

| Workload Category | Ground Truth Source |
|-------------------|-------------------|
| CNN/Transformer | PyTorch profiler on target device |
| LLM Inference | vLLM benchmarks (if GPU available) |
| Distributed | Published results or NCCL tests |

### Phase 4: Analysis

1. Compute accuracy metrics vs ground truth
2. Compare tool predictions against each other
3. Identify systematic biases

---

## Metrics to Collect

### Per-Workload Metrics

| Metric | Unit | Description |
|--------|------|-------------|
| Latency | ms | End-to-end execution time |
| Throughput | samples/s or tokens/s | Rate of processing |
| Energy | mJ | Total energy (if available) |
| Memory Peak | MB | Maximum memory usage |

### Per-Tool Metrics

| Metric | Unit | Description |
|--------|------|-------------|
| Prediction Time | s | Time to generate prediction |
| Model Load Time | s | Time to initialize tool |
| Peak RAM | GB | Tool memory footprint |

### Accuracy Metrics (vs Ground Truth)

| Metric | Formula | Target |
|--------|---------|--------|
| MAPE | mean(abs(pred-actual)/actual) | <10% |
| Spearman Correlation | rank correlation | >0.9 |
| Max Error | max(abs(pred-actual)/actual) | <25% |

---

## Tool-Benchmark Compatibility Matrix

| Benchmark | Timeloop | nn-Meter | ASTRA-sim | VIDUR |
|-----------|----------|----------|-----------|-------|
| CNN-1 (ResNet-50) | Yes | Yes | No | No |
| CNN-2 (VGG-16) | Yes | Yes | No | No |
| CNN-3 (MobileNet-V2) | Yes | Yes | No | No |
| XFMR-1 (BERT-128) | Yes | Yes | No | No |
| XFMR-2 (BERT-512) | Yes | Yes | No | No |
| XFMR-3 (ViT-B) | Yes | Yes | No | No |
| LLM-1 (Llama-7B) | No | No | No | Yes |
| LLM-2 (Llama-7B long) | No | No | No | Yes |
| LLM-3 (Llama-70B) | No | No | No | Yes |
| DIST-1 (AR 8 NPU) | No | No | Yes | No |
| DIST-2 (AR 8 NPU 1GB) | No | No | Yes | No |
| DIST-3 (AR 32 NPU) | No | No | Yes | No |
| DIST-4 (AG 8 NPU) | No | No | Yes | No |

**Note:** Each tool evaluated on applicable benchmarks only. Cross-tool comparisons made within compatible workload categories.

---

## Reproducibility Requirements

### Code Artifacts

All benchmark execution scripts will be provided in `scripts/benchmarks/`:

```
scripts/benchmarks/
├── timeloop/
│   ├── run_cnn.sh
│   └── run_transformer.sh
├── nn-meter/
│   └── run_all.py
├── astra-sim/
│   └── run_distributed.sh
└── vidur/
    └── run_llm.sh
```

### Configuration Files

All workload configurations in `data/benchmarks/workloads/`:

```
data/benchmarks/workloads/
├── cnn/
│   ├── resnet50.yaml
│   ├── vgg16.yaml
│   └── mobilenetv2.yaml
├── transformer/
│   ├── bert_base_128.yaml
│   ├── bert_base_512.yaml
│   └── vit_b_16.yaml
└── llm/
    └── llama_configs.yaml
```

### Results Storage

Raw results stored in `data/results/`:

```
data/results/
├── timeloop/
│   └── <benchmark>_<config>_<timestamp>.json
├── nn-meter/
│   └── predictions_<timestamp>.csv
├── astra-sim/
│   └── <benchmark>_<timestamp>.log
└── vidur/
    └── <benchmark>_<timestamp>/
```

---

## Version Control

| Item | Version/Date |
|------|-------------|
| Benchmark Suite | v1.0 (2026-02-07) |
| Timeloop | Latest Docker image |
| nn-Meter | pip package (with sklearn 1.0.2) |
| ASTRA-sim | Main branch + Docker |
| VIDUR | Main branch + Python 3.10 |

---

## Expected Outcomes

1. **Standardized comparison**: All tools evaluated on same workloads
2. **Category-specific insights**: Best tool per workload category identified
3. **Accuracy validation**: Published claims verified or refuted
4. **Practical guidance**: Clear recommendations for practitioners

---

*Document by Leo | ML Performance Survey Project*
