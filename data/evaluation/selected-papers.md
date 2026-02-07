# Selected Tools for Comprehensive Third-Party Evaluation

This document identifies the final set of tools from our literature survey for experimental evaluation. Selection is based on: open-source availability, reproducibility, impact, category coverage, and active maintenance.

---

## Final Tool Selection Summary

| # | Tool | Category | Sub-category | Repository | Availability | Hardware Req |
|---|------|----------|--------------|------------|--------------|--------------|
| 1 | Timeloop | Analytical | Accelerator DSE | NVlabs/timeloop | Open Source | CPU only |
| 2 | MAESTRO | Analytical | Dataflow Analysis | maestro-project/maestro | Open Source | CPU only |
| 3 | nn-Meter | ML-Based | Edge Latency | microsoft/nn-Meter | Open Source | Edge device (optional) |
| 4 | NeuSight | ML-Based | GPU Latency | PSAL-POSTECH/NeuSight | Open Source | GPU (for validation) |
| 5 | HELP | ML-Based | Meta-Learning | - | Code Available | CPU only |
| 6 | TVM/Ansor | ML-Based | Compiler Cost Model | apache/tvm | Open Source | Target HW for tuning |
| 7 | ASTRA-sim | Simulation | Distributed Training | astra-sim/astra-sim | Open Source | CPU only |
| 8 | VIDUR | Simulation | LLM Inference | microsoft/vidur | Open Source | CPU only |
| 9 | Accel-Sim | Simulation | GPU Cycle-Accurate | accel-sim/accel-sim-framework | Open Source | CPU only |
| 10 | TLP | ML-Based | Tensor Program | - | Code Available | Target HW for training |

**Total: 10 tools** covering Analytical (2), ML-Based (5), and Simulation (3) approaches.

---

## Selection Rationale

### Coverage by Modeling Approach

| Approach | Tools | Coverage |
|----------|-------|----------|
| Analytical | Timeloop, MAESTRO | Accelerator modeling, dataflow analysis |
| ML-Based | nn-Meter, NeuSight, HELP, TVM/Ansor, TLP | Edge, GPU, transfer learning, compiler |
| Simulation | ASTRA-sim, VIDUR, Accel-Sim | Distributed, LLM, GPU cycle-accurate |

### Coverage by Target Hardware

| Hardware | Tools |
|----------|-------|
| DNN Accelerators | Timeloop, MAESTRO |
| Edge Devices | nn-Meter |
| GPUs | NeuSight, Accel-Sim, TVM/Ansor |
| Distributed Systems | ASTRA-sim |
| LLM Serving | VIDUR |
| Multi-platform | HELP, TLP |

### Coverage by Workload Type

| Workload | Tools |
|----------|-------|
| CNN | Timeloop, MAESTRO, nn-Meter, NeuSight |
| Transformer/LLM | NeuSight, VIDUR, TLP |
| Distributed Training | ASTRA-sim |
| General Tensor Programs | TVM/Ansor, TLP |

---

## 1. Timeloop (Analytical - Accelerator DSE)

**Paper:** Timeloop: A Systematic Approach to DNN Accelerator Evaluation (ISPASS 2019)

**Authors:** Parashar et al. (NVIDIA, MIT)

### Why Selected

- **Foundational:** Most-cited analytical framework for DNN accelerator modeling
- **Industry adoption:** Used in 100+ papers, maintained by NVIDIA
- **Comprehensive:** Models energy, latency, and area for spatial architectures
- **Well-documented:** Extensive tutorials and examples

### Repository

- **URL:** https://github.com/NVlabs/timeloop
- **License:** BSD 3-Clause
- **Last Updated:** Active (2024)
- **Stars:** 400+

### Reproducibility Assessment

| Aspect | Status | Notes |
|--------|--------|-------|
| Code availability | Complete | Full source code |
| Documentation | Excellent | Tutorials, examples, wiki |
| Dependencies | Standard | C++, Python, Accelergy for energy |
| Pre-built configs | Yes | Multiple accelerator examples |
| Docker support | Yes | Available |

### Evaluation Plan

1. **Setup:** Install via Docker or source
2. **Workloads:** Run on ResNet-50, BERT, MobileNet layers
3. **Metrics:** Compare predicted vs. published accuracy claims (5-10% error)
4. **Time:** Measure exploration speed (mappings/second)

### Hardware Requirements

- **Minimum:** Linux, 8GB RAM, multi-core CPU
- **Recommended:** 16GB RAM for large design spaces
- **GPU:** Not required

---

## 2. MAESTRO (Analytical - Dataflow Analysis)

**Paper:** MAESTRO: A Data-Centric Approach to Understand Reuse, Performance, and Hardware Cost of DNN Mappings (MICRO 2019)

**Authors:** Kwon et al. (Georgia Tech)

### Why Selected

- **Complementary to Timeloop:** Data-centric vs. loop-nest representation
- **Intuitive notation:** Dataflow directives easier to understand
- **Academic adoption:** Widely used in architecture research
- **Different perspective:** Validates analytical modeling approach

### Repository

- **URL:** https://github.com/maestro-project/maestro
- **License:** BSD 3-Clause
- **Last Updated:** 2023
- **Stars:** 200+

### Reproducibility Assessment

| Aspect | Status | Notes |
|--------|--------|-------|
| Code availability | Complete | Full source code |
| Documentation | Good | README, examples |
| Dependencies | Standard | C++, Python |
| Pre-built configs | Yes | Example dataflows |
| Web interface | Yes | Online demo available |

### Evaluation Plan

1. **Setup:** Build from source or use web interface
2. **Workloads:** Run same layers as Timeloop for comparison
3. **Metrics:** Compare predictions between MAESTRO and Timeloop
4. **Usability:** Assess learning curve vs. Timeloop

### Hardware Requirements

- **Minimum:** Linux, 4GB RAM
- **GPU:** Not required

---

## 3. nn-Meter (ML-Based - Edge Latency)

**Paper:** nn-Meter: Towards Accurate Latency Prediction of Deep-Learning Model Inference on Diverse Edge Devices (MobiSys 2021, Best Paper)

**Authors:** Zhang et al. (Microsoft Research)

### Why Selected

- **State-of-the-art accuracy:** 99% on edge devices
- **Practical impact:** Used in Azure ML for hardware-aware NAS
- **Novel approach:** Kernel-level decomposition with adaptive sampling
- **Well-maintained:** Active development by Microsoft

### Repository

- **URL:** https://github.com/microsoft/nn-Meter
- **License:** MIT
- **Last Updated:** 2024
- **Stars:** 700+

### Reproducibility Assessment

| Aspect | Status | Notes |
|--------|--------|-------|
| Code availability | Complete | Full framework + predictors |
| Documentation | Good | README, examples |
| Pre-trained models | Yes | Multiple edge devices |
| Dependencies | Standard | Python, PyTorch/TensorFlow |
| Test datasets | Partial | Some NAS benchmarks |

### Evaluation Plan

1. **Setup:** pip install nn-meter
2. **Workloads:** Predict latency for NAS-Bench models
3. **Validation:** Compare predictions vs. actual measurements on available device
4. **Metrics:** MAPE, correlation with ground truth

### Hardware Requirements

- **Minimum:** Python environment, any modern CPU
- **For validation:** Access to edge device (Pixel phone, Raspberry Pi, or Intel VPU)
- **Note:** Pre-trained predictors available; training new predictors requires target device

---

## 4. NeuSight (ML-Based - GPU Latency)

**Paper:** NeuSight: Near-Instant Neural Network Inference via Tile-Based GPU Performance Prediction (ASPLOS 2025)

**Authors:** Yu et al. (POSTECH)

### Why Selected

- **State-of-the-art GPU prediction:** 97.7% accuracy
- **Novel tile-based approach:** Captures GPU memory hierarchy effects
- **Broad coverage:** Works on CNNs, Transformers, and LLMs
- **Aligned with survey scope:** Directly addresses ML performance prediction

### Repository

- **URL:** https://github.com/PSAL-POSTECH/NeuSight
- **License:** Apache 2.0
- **Last Updated:** 2024
- **Stars:** 50+

### Reproducibility Assessment

| Aspect | Status | Notes |
|--------|--------|-------|
| Code availability | Complete | Full framework |
| Documentation | Good | README, examples |
| Pre-trained models | Yes | NVIDIA GPU predictors |
| Dependencies | Standard | Python, PyTorch |
| Validation data | Yes | Benchmark results |

### Evaluation Plan

1. **Setup:** Clone repo, install dependencies
2. **Workloads:** Predict latency for ResNet, BERT, GPT-2
3. **Validation:** Compare vs. actual GPU measurements if available
4. **Metrics:** MAPE, correlation, prediction speed

### Hardware Requirements

- **Minimum:** Python environment, CPU
- **For validation:** NVIDIA GPU (any recent generation)
- **Note:** Pre-trained models available for various NVIDIA GPUs

---

## 5. HELP (ML-Based - Meta-Learning Transfer)

**Paper:** Hardware-Adaptive Efficient Latency Prediction for NAS via Meta-Learning (NeurIPS 2021)

**Authors:** Lee et al. (KAIST, Samsung)

### Why Selected

- **Novel approach:** Meta-learning for cross-hardware transfer
- **Sample efficiency:** Works with only 10-100 samples on new device
- **GNN architecture encoding:** Captures graph structure effectively
- **Addresses key challenge:** Hardware adaptation without full retraining

### Repository

- **URL:** Code available via paper supplementary
- **License:** Research use
- **Last Updated:** 2021
- **Stars:** N/A (GitHub link in paper)

### Reproducibility Assessment

| Aspect | Status | Notes |
|--------|--------|-------|
| Code availability | Complete | Full implementation |
| Documentation | Moderate | Paper + README |
| Pre-trained models | Yes | Meta-learned weights |
| Dependencies | Standard | Python, PyTorch |
| Validation data | Yes | NAS-Bench experiments |

### Evaluation Plan

1. **Setup:** Clone repo, install dependencies
2. **Workloads:** NAS-Bench-201 architectures
3. **Transfer test:** Adapt to new hardware with few samples
4. **Metrics:** Accuracy vs. number of adaptation samples

### Hardware Requirements

- **Minimum:** Python environment, 8GB RAM
- **For transfer:** Access to target hardware for few-shot samples
- **Note:** Meta-training requires multiple source platforms (or use provided)

---

## 6. TVM/Ansor (ML-Based - Compiler Cost Model)

**Paper:** Ansor: Generating High-Performance Tensor Programs for Deep Learning (OSDI 2020)

**Authors:** Zheng et al. (UC Berkeley, OctoML)

### Why Selected

- **Production system:** Apache TVM is widely deployed
- **Integrated cost model:** ML model guides compiler optimization
- **TenSet dataset:** 52M records enable reproducible research
- **Practical impact:** Enables hardware-agnostic optimization

### Repository

- **URL:** https://github.com/apache/tvm
- **License:** Apache 2.0
- **Last Updated:** Active (2024)
- **Stars:** 11000+

### Reproducibility Assessment

| Aspect | Status | Notes |
|--------|--------|-------|
| Code availability | Complete | Full compiler + cost model |
| Documentation | Excellent | Extensive tutorials |
| TenSet dataset | Yes | 52M training records |
| Dependencies | Moderate | C++, Python, LLVM |
| Pre-built configs | Yes | Multiple targets |

### Evaluation Plan

1. **Setup:** Install TVM from source
2. **Workloads:** Run autotuning on operators (conv2d, matmul)
3. **Cost model:** Evaluate prediction accuracy during search
4. **Metrics:** Search efficiency, final performance vs. cuDNN

### Hardware Requirements

- **Minimum:** Linux, 16GB RAM, multi-core CPU
- **For tuning:** Target hardware (GPU, CPU, or accelerator)
- **Note:** Can evaluate cost model without hardware using TenSet

---

## 7. ASTRA-sim (Simulation - Distributed Training)

**Paper:** ASTRA-sim: Enabling SW/HW Co-Design Exploration for Distributed DL Training Platforms (ISPASS 2020, arXiv 2023)

**Authors:** Won et al. (Georgia Tech, Meta, Intel, AMD)

### Why Selected

- **Unique capability:** Only framework for end-to-end distributed training simulation
- **Industry backing:** Developed with Meta, Intel, AMD
- **Practical scope:** Models compute, memory, and network interactions
- **Active development:** Continuous updates for modern workloads

### Repository

- **URL:** https://github.com/astra-sim/astra-sim
- **License:** MIT
- **Last Updated:** Active (2024)
- **Stars:** 200+

### Reproducibility Assessment

| Aspect | Status | Notes |
|--------|--------|-------|
| Code availability | Complete | Full simulator |
| Documentation | Good | Tutorials, Chakra trace format |
| Example traces | Yes | Sample distributed workloads |
| Network backends | Multiple | Analytical, NS-3, Garnet |
| Dependencies | Moderate | C++, Python, optional NS-3 |

### Evaluation Plan

1. **Setup:** Build from source (CMake)
2. **Workloads:** Run example Chakra traces (GPT-like, ResNet)
3. **Configurations:** Test 2/4/8 GPU setups
4. **Metrics:** Compare scaling efficiency predictions vs. claimed accuracy (5-15% error)

### Hardware Requirements

- **Minimum:** Linux, 16GB RAM, multi-core CPU
- **Recommended:** 32GB RAM for large simulations
- **GPU:** Not required (simulation only)

---

## 8. VIDUR (Simulation - LLM Inference)

**Paper:** VIDUR: A Large-Scale Simulation Framework for LLM Inference (MLSys 2024)

**Authors:** Agrawal et al. (Microsoft Research)

### Why Selected

- **Novel contribution:** First comprehensive LLM inference simulator
- **High accuracy:** <5% error on real traces
- **Practical use:** Enables capacity planning without GPU clusters
- **Recent and relevant:** Addresses emerging LLM serving challenges

### Repository

- **URL:** https://github.com/microsoft/vidur
- **License:** MIT
- **Last Updated:** 2024
- **Stars:** 100+

### Reproducibility Assessment

| Aspect | Status | Notes |
|--------|--------|-------|
| Code availability | Complete | Full simulator |
| Documentation | Good | README, examples |
| Sample traces | Yes | Request arrival patterns |
| Serving policies | Multiple | Various scheduling algorithms |
| Dependencies | Standard | Python |

### Evaluation Plan

1. **Setup:** pip install or clone repo
2. **Workloads:** Simulate LLaMA-7B/13B serving with sample traces
3. **Configurations:** Test different scheduling policies (vLLM, Orca-style)
4. **Metrics:** Compare predicted latency/throughput vs. claimed accuracy

### Hardware Requirements

- **Minimum:** Python environment, 8GB RAM
- **Recommended:** 16GB RAM for large trace simulations
- **GPU:** Not required (simulation only)

---

## 9. Accel-Sim (Simulation - GPU Cycle-Accurate)

**Paper:** Accel-Sim: An Extensible Simulation Framework for Validated GPU Modeling (ISCA 2020)

**Authors:** Khairy et al. (Purdue)

### Why Selected

- **High fidelity:** Cycle-accurate GPU simulation with 90-97% correlation
- **Modern GPU support:** Validated on Volta, Turing, Ampere
- **SASS-level:** Uses real GPU traces for accuracy
- **Reference standard:** Ground truth for validating analytical/ML models

### Repository

- **URL:** https://github.com/accel-sim/accel-sim-framework
- **License:** BSD 3-Clause
- **Last Updated:** Active (2024)
- **Stars:** 300+

### Reproducibility Assessment

| Aspect | Status | Notes |
|--------|--------|-------|
| Code availability | Complete | Full simulator |
| Documentation | Good | Tutorials, configs |
| GPU configs | Yes | Multiple generations |
| SASS tracer | Yes | For trace collection |
| Dependencies | Moderate | C++, CUDA toolkit |

### Evaluation Plan

1. **Setup:** Build from source
2. **Workloads:** Run DNN kernel traces (GEMM, convolution)
3. **Validation:** Compare simulated vs. real GPU (if available)
4. **Use case:** Validate analytical model predictions

### Hardware Requirements

- **Minimum:** Linux, 32GB RAM (simulation is memory-intensive)
- **For trace collection:** NVIDIA GPU
- **Note:** Pre-collected traces available for some workloads

---

## 10. TLP (ML-Based - Tensor Program Cost Model)

**Paper:** TLP: A Deep Learning-Based Cost Model for Tensor Program Tuning (ASPLOS 2023)

**Authors:** Zhai et al.

### Why Selected

- **State-of-the-art cost model:** Transformer-based, outperforms XGBoost/MLP
- **Program representation:** Tokenizes tensor programs
- **TenSet compatible:** Can leverage 52M-record dataset
- **Modern architecture:** Demonstrates transformer benefits for cost modeling

### Repository

- **URL:** Code available via paper
- **License:** Research use
- **Last Updated:** 2023

### Reproducibility Assessment

| Aspect | Status | Notes |
|--------|--------|-------|
| Code availability | Partial | Implementation available |
| Documentation | Moderate | Paper details |
| TenSet data | Yes | Standard dataset |
| Dependencies | Standard | Python, PyTorch |

### Evaluation Plan

1. **Setup:** Clone repo, install dependencies
2. **Workloads:** TenSet benchmark programs
3. **Comparison:** Compare vs. Ansor MLP cost model
4. **Metrics:** MAPE, search efficiency improvement

### Hardware Requirements

- **Minimum:** Python environment, 16GB RAM for training
- **GPU:** Recommended for training (not required for inference)

---

## Evaluation Priority and Schedule

### Phase 1: CPU-Only Setup (Week 1-2)

Tools requiring no GPU for evaluation:

1. **Timeloop** - Analytical accelerator modeling
2. **MAESTRO** - Dataflow analysis comparison
3. **ASTRA-sim** - Distributed training simulation
4. **VIDUR** - LLM inference simulation
5. **nn-Meter** - Edge prediction (pre-trained models)

### Phase 2: GPU/Hardware Validation (Week 3-4)

Tools requiring hardware for full validation:

6. **NeuSight** - GPU latency prediction
7. **TVM/Ansor** - Compiler cost model
8. **Accel-Sim** - GPU cycle-accurate simulation
9. **HELP** - Transfer learning evaluation
10. **TLP** - Tensor program cost model

---

## Alternatives Considered (Not Selected)

### GPGPU-Sim (Original)

- **Reason:** Accel-Sim is the modern successor with better correlation
- **Alternative:** Use Accel-Sim instead

### gem5

- **Reason:** CPU-focused, ML extensions less mature than specialized tools
- **Alternative:** Include if evaluating CPU inference specifically

### LitePred

- **Reason:** Similar to nn-Meter/HELP but less reproducible
- **Alternative:** Could add if 85-platform transfer is priority

### FlashAttention

- **Reason:** Optimization kernel, not performance predictor (out of survey scope)
- **Note:** Important related work but not a modeling tool

### CALO-GNN

- **Reason:** No public implementation available
- **Alternative:** Monitor for future release

---

## Expected Outcomes

1. **Validation of accuracy claims** - Verify published error rates across all tools
2. **Usability assessment** - Document setup complexity and learning curve
3. **Category comparison** - Side-by-side comparison within each approach
4. **Cross-approach insights** - When to use analytical vs. ML vs. simulation
5. **Gaps identification** - What's missing from current tool ecosystem
6. **Practitioner recommendations** - Guide for tool selection by use case

---

## Justification Summary

| Tool | Category | Justification |
|------|----------|---------------|
| Timeloop | Analytical | Industry standard, excellent docs, NVIDIA-backed |
| MAESTRO | Analytical | Complements Timeloop with data-centric view |
| nn-Meter | ML-Based | Best Paper award, 99% accuracy, Microsoft-maintained |
| NeuSight | ML-Based | State-of-the-art GPU prediction, tile-based novelty |
| HELP | ML-Based | Meta-learning enables practical transfer |
| TVM/Ansor | ML-Based | Production compiler with TenSet dataset |
| ASTRA-sim | Simulation | Unique distributed training capability |
| VIDUR | Simulation | Only LLM inference simulator, <5% error |
| Accel-Sim | Simulation | Ground truth GPU simulation, 90%+ correlation |
| TLP | ML-Based | Transformer cost model, modern approach |

---

*Finalized by Maya | ML Performance Survey Project*
*Last Updated: 2026-02-06*
