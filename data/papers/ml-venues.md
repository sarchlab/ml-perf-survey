# ML Venues Paper Summary

Papers on ML performance modeling from MLSys, NeurIPS, ICML, ICLR, OSDI (2018-2024).

---

## Summary Table

| Title | Authors | Year | Venue | Approach | Target | Notes |
|-------|---------|------|-------|----------|--------|-------|
| TVM: End-to-End Optimizing Compiler | Chen et al. | 2018 | OSDI | ML-Based | Multi | Foundational DL compiler with learned cost model |
| Halide Autoscheduler | Adams et al. | 2019 | SIGGRAPH | ML-Based | CPU/GPU | Tree search with learned cost model |
| Ansor: High-Performance Tensor Programs | Zheng et al. | 2020 | OSDI | ML-Based | Multi | Hierarchical search, up to 3.8x speedup |
| Once-for-All | Cai et al. | 2020 | ICLR | ML-Based | Multi | NAS with accuracy predictor, 10^19 settings |
| nn-Meter | Zhang et al. | 2021 | MobiSys | ML-Based | Edge | Best Paper. Kernel-level, 99% accuracy |
| TenSet | Zheng et al. | 2021 | NeurIPS | Dataset | Multi | Large-scale program performance dataset |
| MetaTune | Janik et al. | 2021 | arXiv | ML-Based | Multi | Meta-learning for autotuning |
| MetaSchedule | Shao et al. | 2022 | NeurIPS | ML-Based | Multi | Probabilistic cost-model-driven search |
| FlexGen | Sheng et al. | 2023 | ICML | Analytical | GPU | LP-based offloading for LLM inference |
| VIDUR | Agrawal et al. | 2024 | MLSys | Simulation | GPU | LLM inference simulator, <5% error |
| Latency Predictors for NAS | various | 2024 | MLSys | ML-Based | Multi | Comprehensive NAS predictor study |
| FlashDecoding++ | various | 2024 | MLSys | Analytical | GPU | LLM inference optimization |
| MEDUSA | Cai et al. | 2024 | ICML | ML-Based | GPU | Speculative decoding, 2.2-2.8x speedup |
| HW-GPT-Bench | various | 2024 | NeurIPS | Benchmark | Multi | Hardware-aware NAS benchmark for LLMs |
| CALO-GNN | various | 2024 | OpenReview | ML-Based | Multi | GNN cost model with uncertainty |
| ROFT | various | 2025 | Sci Reports | Hybrid | GPU | Roofline-based autotuning, 4-10x faster |

---

## Categorization by Focus Area

### Compiler Cost Models
- **TVM** (2018) - XGBoost regression cost model for tensor optimization
- **Halide Autoscheduler** (2019) - Tree search with learned cost model
- **Ansor** (2020) - Hierarchical search with evolutionary refinement
- **TenSet** (2021) - Training dataset for learned compilers
- **MetaSchedule** (2022) - Probabilistic search with learned model
- **MetaTune** (2021) - Meta-learning for fast transfer
- **CALO-GNN** (2024) - GNN with calibrated uncertainty
- **ROFT** (2025) - Roofline-augmented cost model

### Neural Architecture Search Predictors
- **Once-for-All** (2020) - Train once, specialize via predictor
- **nn-Meter** (2021) - Kernel-level latency on edge devices
- **Latency Predictors for NAS** (2024) - Comprehensive predictor analysis
- **HW-GPT-Bench** (2024) - Benchmark for LLM NAS

### LLM Inference Optimization
- **FlexGen** (2023) - Offloading with LP optimization
- **VIDUR** (2024) - Large-scale LLM simulation (<5% error)
- **FlashDecoding++** (2024) - Asynchronous decoding optimization
- **MEDUSA** (2024) - Multi-head speculative decoding

---

## Categorization by Modeling Approach

### ML-Based (Learned Cost Models)
- TVM, Halide Autoscheduler, Ansor - XGBoost/NN regression
- nn-Meter - Kernel-level prediction with adaptive sampling
- CALO-GNN - Graph neural network with uncertainty quantification
- MetaTune - Meta-learning for fast adaptation

### Hybrid (Analytical + ML)
- ROFT - Roofline model augmented with learning
- NeuSight - Physics-informed tile-based prediction

### Simulation-Based
- VIDUR - Discrete-event simulation for LLM serving

### Analytical
- FlexGen - Linear programming for offloading decisions

---

## Key Themes and Trends

### 1. Compiler Cost Models Mature
- Evolution: Hand-crafted → XGBoost → GNN with uncertainty
- Key challenge: Transfer across devices/workloads
- TenSet dataset enables reproducible research

### 2. NAS Latency Prediction Advances
- nn-Meter achieves 99% accuracy on edge devices
- 2024 MLSys paper shows 22.5% improvement with better predictors
- HW-GPT-Bench extends to LLM architectures

### 3. LLM-Specific Modeling Emerges
- VIDUR: First large-scale LLM inference simulator
- MEDUSA: Novel speculative decoding approach
- FlexGen: Analytical offloading optimization

### 4. Meta-Learning for Efficiency
- MetaTune: Fast adaptation to new hardware
- Latency Predictors study: Transfer learning benefits

---

## Papers to Deep-Dive (High Priority)

1. **Ansor** - State-of-the-art tensor compiler cost model
2. **nn-Meter** - Best-in-class edge latency prediction
3. **VIDUR** - Essential for LLM serving research
4. **Latency Predictors for NAS** - Comprehensive analysis of approaches
5. **TenSet** - Enables reproducible cost model research

---

## Comparison: Architecture vs ML Venues

| Aspect | Architecture Venues | ML Venues |
|--------|---------------------|-----------|
| Focus | Accelerator design, simulation | Compiler optimization, NAS |
| Approach | More analytical models | More learned models |
| Hardware | Custom accelerators, GPUs | GPUs, edge devices |
| Workloads | DNN operators | Full models, LLMs |
| Accuracy | Often <10% error | 1-5% for specialized |
| Speed | 2000x over simulation | Minutes for compilation |

Both communities contribute essential pieces to the performance modeling puzzle.
