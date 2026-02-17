# LLM-Focused Benchmark Suite for Performance Modeling Tool Evaluation

This benchmark suite evaluates performance modeling tools against the workloads that matter most to modern ML practitioners: **LLM training** and **LLM inference**. Rather than generic rubrics, we define concrete scenarios representing real deployment decisions and assess which tools can address them.

---

## Design Rationale

Modern ML infrastructure spending is dominated by LLM workloads. Practitioners need tools that answer questions like:
- "How long will fine-tuning Llama-3-70B take on 64 H100s with FSDP?"
- "Can we serve Mixtral-8x7B at 200 QPS with P99 TTFT < 500ms on 4 A100s?"
- "What batch size maximizes throughput for Llama-3-8B decode on a single H100?"
- "Should we use speculative decoding for Llama-3-70B to meet our latency SLA?"
- "How much does prefix caching help for our RAG workload with 80% shared prefix?"

The benchmark suite is organized around these real decision points.

### Benchmark Design Principles

1. **Decision-driven**: Each benchmark maps to a deployment decision practitioners actually face.
2. **Workload-specific**: Parameters are drawn from real model architectures (Llama-2/3, Mixtral, GPT-3), not synthetic workloads.
3. **Multi-scale**: Scenarios span single-kernel to multi-node cluster to expose composition gaps.
4. **Architecture-aware**: Scenarios include modern innovations (GQA, MoE, speculative decoding) beyond vanilla transformers.
5. **Quantifiable**: Each scenario defines concrete model dimensions, hardware specs, and measurable metrics.

---

## Reference Model Specifications

All benchmarks reference real model architectures with exact dimensions. These parameters are needed by any tool attempting these predictions.

| Model | Params | Layers | Hidden | Heads | KV Heads | Inter | Vocab | Context |
|-------|--------|--------|--------|-------|----------|-------|-------|---------|
| Llama-2-7B | 6.74B | 32 | 4096 | 32 | 32 | 11008 | 32000 | 4096 |
| Llama-2-13B | 13.02B | 40 | 5120 | 40 | 40 | 13824 | 32000 | 4096 |
| Llama-2-70B | 68.98B | 80 | 8192 | 64 | 8 (GQA) | 28672 | 32000 | 4096 |
| Llama-3-8B | 8.03B | 32 | 4096 | 32 | 8 (GQA) | 14336 | 128256 | 8192 |
| Llama-3-70B | 70.55B | 80 | 8192 | 64 | 8 (GQA) | 28672 | 128256 | 8192 |
| GPT-3-175B | 174.6B | 96 | 12288 | 96 | 96 | 49152 | 50257 | 2048 |
| Mixtral-8x7B | 46.7B (12.9B active) | 32 | 4096 | 32 | 8 (GQA) | 14336 | 32000 | 32768 |
| Falcon-40B | 40.0B | 60 | 8192 | 128 | 1 (MQA) | 32768 | 65024 | 2048 |

### Reference Hardware Specifications

| GPU | FP16 TFLOPS | BF16 TFLOPS | HBM | HBM BW (TB/s) | NVLink BW (GB/s) | TDP (W) |
|-----|------------|------------|-----|---------------|-------------------|---------|
| H100 SXM | 989 | 989 | 80 GB HBM3 | 3.35 | 900 (NVLink 4) | 700 |
| A100-80G SXM | 312 | 312 | 80 GB HBM2e | 2.04 | 600 (NVLink 3) | 400 |
| A100-40G SXM | 312 | 312 | 40 GB HBM2e | 2.04 | 600 (NVLink 3) | 400 |
| L4 | 121 (FP16 w/sparsity) | 121 | 24 GB GDDR6 | 0.30 | N/A | 72 |
| T4 | 65 | N/A | 16 GB GDDR6 | 0.32 | N/A | 70 |

---

## Part 1: LLM Training Benchmarks (21 scenarios)

### T1. Single-GPU Training Kernel Performance (5 scenarios)

Predicting per-layer execution time for transformer training operations.

| ID | Operation | Model | Config | Key Metric | Decision It Informs |
|----|-----------|-------|--------|------------|---------------------|
| T1.1 | Attention forward+backward | Llama-2-7B | seq=2048, bs=4, H100, bf16 | Latency (ms) | FlashAttention vs standard attention |
| T1.2 | Attention forward+backward | Llama-2-7B | seq=8192, bs=1, H100, bf16 | Latency (ms) | Long-context training feasibility |
| T1.3 | MLP forward+backward | Llama-2-7B | hidden=4096, inter=11008, H100, bf16 | Latency (ms) | Compute roofline utilization |
| T1.4 | Attention forward+backward | Llama-2-7B | seq=2048, bs=4, A100-80G, bf16 | Latency (ms) | GPU generation comparison |
| T1.5 | Full training iteration | GPT-3-175B | single layer, H100, bf16 | Latency (ms) | Per-layer profiling for pipeline parallelism |

**What this tests:** Kernel-level prediction accuracy for transformer-specific operations (not CNNs). Captures the attention quadratic scaling, MLP memory bandwidth, and mixed-precision behavior unique to LLM training.

**Expected behavior patterns:**
- T1.1 vs T1.2: Attention latency should scale ~16x (8192/2048)^2 for standard attention, ~4x for FlashAttention (linear in seq_len).
- T1.1 vs T1.4: H100 should be ~2-3x faster than A100 for attention (higher HBM bandwidth + larger L2).
- T1.3: MLP is compute-bound at batch_size=4; should approach H100 bf16 peak (989 TFLOPS). FLOPs = 2 * bs * seq * hidden * inter * 2 (fwd+bwd) * 3 (two linear layers) ≈ 2.9 TFLOPS per iteration.
- T1.5: GPT-3 single layer has ~1.8B params; forward+backward ≈ 6 * 1.8B * bs * seq FLOPs.

### T2. Distributed Training Communication (6 scenarios)

Communication overhead for LLM-scale distributed training.

| ID | Scenario | Model | Parallelism | GPUs | Topology | Key Metric |
|----|----------|-------|-------------|------|----------|------------|
| T2.1 | Data-parallel gradient sync | Llama-2-7B | DP=8 | 8 x H100 | NVSwitch | AllReduce time (ms) for 7B params |
| T2.2 | Tensor-parallel all-gather | Llama-2-70B | TP=8 | 8 x H100 | NVSwitch | AllGather time (ms), 70B activations |
| T2.3 | Pipeline-parallel micro-batch | GPT-3-175B | PP=8, DP=8 | 64 x H100 | NVLink+IB | Bubble overhead (%) |
| T2.4 | FSDP all-gather + reduce-scatter | Llama-2-13B | FSDP=8 | 8 x H100 | NVSwitch | Communication/compute overlap ratio |
| T2.5 | Expert-parallel routing | Mixtral-8x7B | EP=8, DP=4 | 32 x H100 | NVLink+IB | All-to-All time (ms), token routing |
| T2.6 | Cross-node gradient sync | Llama-2-70B | DP=4 | 32 x H100 (4 nodes) | InfiniBand 400G | AllReduce over IB vs NVLink |

**What this tests:** Whether tools can model the multi-dimensional parallelism (DP+TP+PP+EP) and hierarchical topologies (intra-node NVLink vs inter-node IB) that define LLM training scaling.

**Expected behavior patterns:**
- T2.1: AllReduce of 7B params (28 GB in bf16) over 8 H100 NVLink. Ring AllReduce: 2*(N-1)/N * 28 GB / 900 GB/s ≈ 0.054s ≈ 54 ms theoretical minimum.
- T2.2: AllGather for TP reconstructs full activation tensor. For Llama-70B with TP=8, each GPU holds 1/8 of hidden dim; AllGather is bandwidth-limited on NVLink.
- T2.3: Pipeline bubble = (PP-1)/total_microbatches. With PP=8, interleaved schedule should achieve <15% bubble with sufficient microbatches.
- T2.5: All-to-All for MoE routes tokens across 8 expert-parallel ranks. Message size depends on expert capacity factor and tokens per sequence.
- T2.6: Cross-node IB (400 Gb/s ≈ 50 GB/s per link) is ~18x slower than intra-node NVLink (900 GB/s), creating a hierarchical communication bottleneck.

### T3. Training Scaling and Memory (5 scenarios)

End-to-end training throughput and memory constraints.

| ID | Scenario | Model | Hardware | Config | Key Metric |
|----|----------|-------|----------|--------|------------|
| T3.1 | Maximum batch size | Llama-2-7B | 1 x A100-80G | bf16, seq=2048 | Max batch size before OOM |
| T3.2 | Activation checkpointing tradeoff | Llama-2-13B | 1 x H100 | With/without checkpointing | Throughput (tokens/s) vs memory (GB) |
| T3.3 | Strong scaling efficiency | Llama-2-70B | 8→16→32→64 H100 | TP=8, DP varies | Scaling efficiency (%) |
| T3.4 | Training time estimation | Llama-3-8B | 64 x H100 | 1T tokens, FSDP | Total training time (hours) |
| T3.5 | Hardware comparison | Llama-2-7B | 8 x H100 vs 8 x A100 | Same config | Throughput ratio |

**What this tests:** Whether tools can predict memory capacity limits, compute-memory tradeoffs from checkpointing, and the diminishing returns of scaling — the decisions that determine training infrastructure cost.

**Expected behavior patterns:**
- T3.1: Memory breakdown for Llama-2-7B training: model params (14 GB in bf16), optimizer states (28 GB for AdamW fp32), gradients (14 GB), activations (~2 GB per layer * 32 layers * bs). Max bs ≈ (80 - 14 - 28 - 14) / (2*32) ≈ bs of ~3 at seq=2048 without checkpointing.
- T3.2: Activation checkpointing reduces activation memory ~5x but increases compute ~33% (recompute forward pass for each layer during backward). Tools must capture this tradeoff.
- T3.4: Estimated FLOPs for 8B model on 1T tokens: 6 * 8B * 1T = 4.8e22 FLOPs. At 64 H100 with 50% MFU: 64 * 989e12 * 0.5 = 3.16e16 FLOPS. Time ≈ 4.8e22 / 3.16e16 ≈ 1.52e6 seconds ≈ 17.6 days.
- T3.5: H100 vs A100 throughput ratio should be ~2.5-3x for compute-bound LLM training (989/312 TFLOPS ratio, modulated by memory bandwidth differences).

### T4. Advanced Training Scenarios (5 scenarios) — NEW

Emerging training patterns not covered by basic benchmarks.

| ID | Scenario | Model | Hardware | Config | Key Metric |
|----|----------|-------|----------|--------|------------|
| T4.1 | Mixed-precision training | Llama-2-7B | 1 x H100 | fp8 vs bf16 | Throughput improvement, loss convergence |
| T4.2 | Sequence-parallel training | Llama-3-70B | 8 x H100 | SP=8, seq=32768 | Memory per GPU, communication overhead |
| T4.3 | Gradient accumulation | Llama-2-7B | 8 x H100 | micro_bs=1, grad_accum=64 | Effective batch size vs throughput |
| T4.4 | LoRA fine-tuning | Llama-2-70B | 1 x A100-80G | rank=16, alpha=32 | Memory savings, throughput vs full fine-tune |
| T4.5 | Context extension training | Llama-3-8B | 8 x H100 | seq=32768, RoPE scaling | Memory per GPU, attention compute |

**What this tests:** Whether tools can model advanced training optimizations that practitioners use to reduce costs: FP8 precision, sequence parallelism for long contexts, gradient accumulation for large effective batch sizes, parameter-efficient fine-tuning, and context window extension.

**Expected behavior patterns:**
- T4.1: FP8 on H100 should provide ~2x compute throughput over bf16 for matmuls, but with master weights still in fp32/bf16.
- T4.2: Sequence parallelism distributes activation memory across ranks. With SP=8, activation memory per GPU drops ~8x, but adds AllGather/ReduceScatter per layer.
- T4.4: LoRA with rank=16 for 70B model: trainable params ≈ 2 * rank * hidden * num_layers * 2 (Q,V projections) ≈ 2*16*8192*80*2 ≈ 41.9M (0.06% of total). Memory: model in bf16 (140 GB, need multi-GPU or quantization) + LoRA params (0.08 GB) + optimizer states for LoRA only (0.16 GB).

---

## Part 2: LLM Inference Benchmarks (24 scenarios)

### I1. Single-Request Latency (5 scenarios)

Predicting per-request performance for LLM inference.

| ID | Scenario | Model | Hardware | Config | Key Metric |
|----|----------|-------|----------|--------|------------|
| I1.1 | Short prompt, short generation | Llama-2-7B | 1 x A100-80G | prefill=128, decode=128 | TTFT (ms), TPOT (ms) |
| I1.2 | Long prompt, short generation | Llama-2-7B | 1 x A100-80G | prefill=4096, decode=64 | TTFT (ms), prefill throughput |
| I1.3 | Short prompt, long generation | Llama-2-7B | 1 x A100-80G | prefill=64, decode=2048 | Decode throughput (tokens/s) |
| I1.4 | Large model single-request | Llama-2-70B | 4 x A100-80G, TP=4 | prefill=512, decode=256 | TTFT (ms), TPOT (ms) |
| I1.5 | Prefill-heavy summarization | Llama-3-8B | 1 x H100 | prefill=8192, decode=128 | TTFT (ms), memory (GB) |

**What this tests:** The fundamental prefill (compute-bound) vs decode (memory-bound) distinction. Tools must understand that prefill scales with sequence length squared (attention) while decode is bottlenecked by KV cache memory bandwidth.

**Expected behavior patterns:**
- I1.1: Prefill 128 tokens is very fast (<5ms on A100). Decode at 128 tokens: TPOT ≈ model_params * 2 / HBM_BW = 7B * 2 / 2.04 TB/s ≈ 6.9 ms/token (memory-bound).
- I1.2: Prefill 4096 tokens on A100: FLOPs ≈ 2 * 7B * 4096 ≈ 5.7e13. At 312 TFLOPS: ~183 ms (compute-bound).
- I1.3: Long decode is memory-bandwidth-bound throughout. Total decode time ≈ 2048 * 6.9 ms ≈ 14.1s.
- I1.4: TP=4 splits model across 4 GPUs. Decode TPOT ≈ (70B/4) * 2 / 2.04 TB/s + AllReduce overhead ≈ 17.2 ms + comm.
- I1.5: Prefill 8192 on H100: FLOPs ≈ 2 * 8B * 8192 ≈ 1.3e14. At 989 TFLOPS: ~131 ms. KV cache for 8192 context: 2 * 32 layers * 8 KV_heads * 128 head_dim * 8192 * 2 bytes ≈ 1.07 GB.

### I2. Batched Serving Throughput (6 scenarios)

Performance under concurrent request serving.

| ID | Scenario | Model | Hardware | Serving Config | Key Metric |
|----|----------|-------|----------|---------------|------------|
| I2.1 | Low-load chatbot | Llama-2-7B | 1 x A100-80G | QPS=2, Poisson | P50/P99 E2E latency (s) |
| I2.2 | Medium-load API | Llama-2-7B | 1 x A100-80G | QPS=10, Poisson | Throughput (tokens/s), P99 TTFT |
| I2.3 | High-load stress test | Llama-2-7B | 1 x A100-80G | QPS=50, Poisson | Saturation point, queue depth |
| I2.4 | Continuous batching | Llama-2-7B | 1 x A100-80G | vLLM defaults | Throughput vs static batching |
| I2.5 | Chunked prefill | Llama-2-7B | 1 x A100-80G | Sarathi chunking | TTFT variance reduction |
| I2.6 | Multi-GPU serving | Llama-2-70B | 4 x A100-80G, TP=4 | QPS=5, Poisson | E2E latency, GPU utilization |

**What this tests:** Whether tools capture scheduling dynamics — continuous batching, chunked prefill, preemption — that determine real-world serving throughput. Static per-request prediction is insufficient; tools must model queuing and interference.

**Expected behavior patterns:**
- I2.1 vs I2.3: At QPS=2, system is lightly loaded; P99 should be close to P50. At QPS=50, queuing effects dominate; P99 >> P50. Tool must model M/G/1 queuing behavior.
- I2.4: Continuous batching (Orca-style) should yield 2-5x throughput improvement over static batching by avoiding padding waste and enabling early completion.
- I2.5: Chunked prefill (Sarathi) should reduce TTFT variance by preventing long prefills from blocking decode iterations. P99 TTFT should decrease significantly vs I2.4.

### I3. KV Cache and Memory Management (4 scenarios)

Memory-dominated inference scenarios.

| ID | Scenario | Model | Hardware | Config | Key Metric |
|----|----------|-------|----------|--------|------------|
| I3.1 | KV cache sizing | Llama-2-7B | 1 x A100-80G | max_seq=4096, varying concurrent | Max concurrent requests before OOM |
| I3.2 | PagedAttention efficiency | Llama-2-7B | 1 x A100-80G | vLLM paged vs contiguous | Memory utilization (%), fragmentation |
| I3.3 | Long-context memory | Llama-3-8B | 1 x H100 | context=32K, bs=1 | KV cache size (GB), decode speed |
| I3.4 | Memory-throughput tradeoff | Llama-2-13B | 1 x A100-80G | varying max_num_seqs | Throughput vs memory curve |

**What this tests:** KV cache management is the bottleneck for LLM serving. Tools must predict memory consumption as a function of sequence length, batch size, and attention mechanism to answer capacity planning questions.

**Expected behavior patterns:**
- I3.1: KV cache per request at max_seq=4096: 2 * 32 layers * 32 heads * 128 dim * 4096 * 2 bytes (bf16) = 2.15 GB. Model weights: ~14 GB. Available for KV: 80 - 14 ≈ 66 GB. Max concurrent: ~30 requests (with fragmentation overhead).
- I3.2: PagedAttention reduces waste from ~50-70% (contiguous, pre-allocated) to <5% (paged, on-demand). Tools should predict ~2x effective capacity gain.
- I3.3: KV cache at 32K context for Llama-3-8B (GQA with 8 KV heads): 2 * 32 * 8 * 128 * 32768 * 2 bytes = 4.29 GB per request. Decode becomes extremely memory-bandwidth-bound.

### I4. Model Architecture Variants (4 scenarios)

Inference characteristics across different LLM architectures.

| ID | Model Type | Model | Hardware | Config | Key Metric |
|----|-----------|-------|----------|--------|------------|
| I4.1 | Dense decoder | Llama-2-7B | 1 x A100-80G | standard | Baseline latency |
| I4.2 | Mixture-of-experts | Mixtral-8x7B | 2 x A100-80G | expert routing | Expert activation latency, load balance |
| I4.3 | Grouped-query attention | Llama-2-70B (GQA) | 4 x A100-80G | TP=4 | KV cache reduction, attention speedup |
| I4.4 | Multi-query attention | Falcon-40B (MQA) | 4 x A100-80G | TP=4 | Decode throughput vs Llama-2 |

**What this tests:** Whether tools generalize beyond vanilla transformers to modern architectural innovations (MoE routing, GQA/MQA attention patterns) that fundamentally change performance characteristics.

**Expected behavior patterns:**
- I4.2: Mixtral activates 2 of 8 experts per token. Total params 46.7B but active params 12.9B per token. Model needs ~93 GB in bf16 (all experts loaded), so minimum 2 A100-80G. Expert routing adds All-to-All communication in EP mode. Load imbalance can cause 10-30% throughput loss.
- I4.3: GQA with 8 KV heads (vs 64 query heads for Llama-2-70B) reduces KV cache 8x. For 4096 context: GQA KV cache = 2 * 80 * 8 * 128 * 4096 * 2 = 1.34 GB vs MHA = 10.74 GB. Significant capacity improvement.
- I4.4: MQA (1 KV head) reduces KV cache further but may lose quality. Decode is faster due to less KV cache to read.

### I5. Advanced Inference Scenarios (5 scenarios) — NEW

Emerging inference optimizations critical for production deployments.

| ID | Scenario | Model | Hardware | Config | Key Metric |
|----|----------|-------|----------|--------|------------|
| I5.1 | Speculative decoding | Llama-2-70B + Llama-2-7B draft | 4 x A100-80G, TP=4 | k=5 speculation tokens | Decode speedup vs autoregressive |
| I5.2 | Prefix caching (RAG) | Llama-3-8B | 1 x H100 | 80% shared prefix (4096 tokens) | TTFT reduction, memory savings |
| I5.3 | Disaggregated serving | Llama-2-70B | 8 x A100-80G | 4 prefill + 4 decode | Throughput vs collocated serving |
| I5.4 | Quantized inference | Llama-2-70B | 1 x A100-80G | INT4 (GPTQ/AWQ) | Throughput improvement, memory reduction |
| I5.5 | Multi-LoRA serving | Llama-2-7B | 1 x A100-80G | 10 LoRA adapters, varying QPS | Adapter switching overhead, throughput |

**What this tests:** Whether tools can model the optimization techniques that production LLM serving systems actually use. These techniques fundamentally change performance characteristics and are rapidly becoming standard.

**Expected behavior patterns:**
- I5.1: Speculative decoding with k=5 and ~70% acceptance rate. Draft model adds ~10% compute overhead. Net speedup ≈ accepted_tokens / (1 + draft_overhead) ≈ 3.5/1.1 ≈ 3.2x for memory-bound decode. Exact speedup depends on draft model quality.
- I5.2: With 80% shared prefix (4096 of 5120 total tokens), TTFT drops to ~20% of non-cached baseline. KV cache memory for shared prefix is amortized across requests. Tools must model cache hit rate and eviction policy.
- I5.3: DistServe-style disaggregation separates prefill (compute-bound) and decode (memory-bound) onto different GPU pools. Expected throughput gain 1.5-2x under mixed workloads by avoiding interference.
- I5.4: INT4 quantization reduces model size 4x (70B: 140 GB → 35 GB, fits single A100-80G). Decode throughput ≈ 4x (memory-bandwidth-bound). Prefill improvement less dramatic (~1.5-2x, still compute-bound).

---

## Part 3: Tool Capability Assessment

### Benchmark Coverage Matrix

Each benchmark maps to tool capabilities. A tool either **supports** the scenario (can produce a prediction) or **does not** (the workload is outside its scope).

| Benchmark | NeuSight | ASTRA-sim | VIDUR | Timeloop | nn-Meter |
|-----------|----------|-----------|-------|----------|----------|
| **T1: Training Kernels (5)** | | | | | |
| T1.1–T1.4 Attention/MLP kernels | Partial (inference only) | No | No | No | No |
| T1.5 Full training iteration | No | No | No | No | No |
| **T2: Distributed Training (6)** | | | | | |
| T2.1 DP gradient sync | No | Yes (AllReduce) | No | No | No |
| T2.2 TP all-gather | No | Yes (AllGather) | No | No | No |
| T2.3 PP micro-batch pipeline | No | Partial (no PP scheduling) | No | No | No |
| T2.4 FSDP overlap | No | Partial (no overlap model) | No | No | No |
| T2.5 MoE expert routing | No | Yes (All-to-All) | No | No | No |
| T2.6 Cross-node communication | No | Yes (multi-topology) | No | No | No |
| **T3: Training Scale (5)** | | | | | |
| T3.1–T3.5 Memory/scaling | No | Partial (comm only) | No | No | No |
| **T4: Advanced Training (5)** | | | | | |
| T4.1 FP8 training | No | No | No | No | No |
| T4.2 Sequence parallelism | No | Partial (comm only) | No | No | No |
| T4.3 Gradient accumulation | No | No | No | No | No |
| T4.4 LoRA fine-tuning | No | No | No | No | No |
| T4.5 Context extension | No | No | No | No | No |
| **I1: Single-Request Latency (5)** | | | | | |
| I1.1–I1.3 Single-GPU inference | Partial (no TTFT/TPOT) | No | Yes | No | No |
| I1.4 Multi-GPU inference | No | No | Yes (TP supported) | No | No |
| I1.5 Long-context inference | No | No | Yes | No | No |
| **I2: Batched Serving (6)** | | | | | |
| I2.1–I2.3 Load levels | No | No | Yes | No | No |
| I2.4 Continuous batching | No | No | Yes (vLLM) | No | No |
| I2.5 Chunked prefill | No | No | Yes (Sarathi) | No | No |
| I2.6 Multi-GPU serving | No | No | Yes | No | No |
| **I3: KV Cache/Memory (4)** | | | | | |
| I3.1–I3.4 Memory management | No | No | Partial (no PagedAttn detail) | No | No |
| **I4: Architecture Variants (4)** | | | | | |
| I4.1 Dense decoder | Partial | No | Yes | No | No |
| I4.2 MoE inference | No | No | No | No | No |
| I4.3–I4.4 GQA/MQA | No | No | Partial | No | No |
| **I5: Advanced Inference (5)** | | | | | |
| I5.1 Speculative decoding | No | No | No | No | No |
| I5.2 Prefix caching | No | No | No | No | No |
| I5.3 Disaggregated serving | No | No | No | No | No |
| I5.4 Quantized inference | No | No | No | No | No |
| I5.5 Multi-LoRA serving | No | No | No | No | No |

### Coverage Summary

| Tool | Training (21) | Inference (24) | Total (45) | Full | Partial |
|------|--------------|----------------|-----------|------|---------|
| NeuSight | 0/21 | 0/24 | 0/45 | 0 | 7 |
| ASTRA-sim | 5/21 | 0/24 | 5/45 | 5 | 4 |
| VIDUR | 0/21 | 12/24 | 12/45 | 12 | 2 |
| Timeloop | 0/21 | 0/24 | 0/45 | 0 | 0 |
| nn-Meter | 0/21 | 0/24 | 0/45 | 0 | 0 |

### Key Finding

**No single tool covers even a third of the LLM benchmark suite.** The expanded 45-scenario suite (from the original 35) reveals even starker gaps:
- VIDUR provides the broadest LLM coverage (12/45, all inference serving).
- ASTRA-sim covers distributed communication (5/45, all training communication).
- The **entire advanced training category (T4)** has zero tool coverage — no tool models FP8 training, sequence parallelism, LoRA fine-tuning, or context extension.
- The **entire advanced inference category (I5)** has zero tool coverage — no tool models speculative decoding, prefix caching, disaggregated serving, or quantized inference.
- Only 17/45 scenarios (38%) have any tool coverage (full or partial). **62% of modern LLM workload scenarios are completely unaddressed.**

---

## Part 4: Gap Analysis

### Critical Unaddressed Scenarios

1. **LLM training kernel prediction (T1):** NeuSight predicts inference kernels but not training (backward pass, gradient accumulation, optimizer steps). No tool fills this gap.

2. **Multi-dimensional parallelism (T2.3, T2.4):** ASTRA-sim models individual collectives but not the interleaved pipeline parallelism schedules (1F1B, interleaved) or FSDP compute-communication overlap that dominate real training.

3. **End-to-end training time (T3.4):** Requires composing kernel prediction + communication + memory + parallelism strategy — no tool chain provides this.

4. **Advanced training optimizations (T4):** FP8 training, sequence parallelism, LoRA fine-tuning, and context extension are standard practice but have zero tool coverage. These optimizations change performance characteristics by 2-4x, making predictions without them useless for real deployment decisions.

5. **MoE inference (I4.2):** Mixtral-class models with expert routing are increasingly deployed but no evaluated tool models expert selection, load imbalance, or routing overhead.

6. **KV cache management (I3):** VIDUR models serving but doesn't expose PagedAttention-level memory prediction. The gap between "memory used" and "how to optimize memory" remains unaddressed.

7. **Hardware comparison (T3.5, across all):** Practitioners frequently compare H100 vs A100 vs MI300X. Only NeuSight supports multiple GPU types, but only for inference kernels.

8. **Production inference optimizations (I5):** Speculative decoding, prefix caching, disaggregated serving, and quantized inference are deployed at scale by every major LLM provider. No evaluated tool can predict performance under these optimizations, making the tools unsuitable for production capacity planning.

### Severity Assessment

| Gap | Severity | Impact | Why It Matters |
|-----|----------|--------|----------------|
| Training kernels (T1) | Critical | Cannot predict training costs | Training compute costs dominate LLM budgets |
| E2E training time (T3.4) | Critical | Cannot plan training runs | Multi-million dollar training runs need accurate estimates |
| Advanced training (T4) | High | Real deployments use these | LoRA, FP8 are standard; predictions without them are unrealistic |
| Speculative decoding (I5.1) | High | Growing production use | 2-3x speedup changes cost calculus |
| Prefix caching (I5.2) | High | Universal in RAG | RAG dominates enterprise deployment |
| Disaggregated serving (I5.3) | Medium | Emerging technique | Not yet universal but growing rapidly |
| Quantized inference (I5.4) | Critical | Standard practice | Most production deployments use INT4/INT8 |

---

*Document by experiment-runner | ML Performance Survey Project | v3.0 (2026-02-16)*
*Expanded from v2.0 with concrete workload parameters, expected behaviors, and advanced scenarios per human directive #250*
