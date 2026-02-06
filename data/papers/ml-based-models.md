# ML-Based Performance Modeling Papers

Papers focused on neural network surrogates, GNN-based models, transfer learning, and LLM inference prediction (2023-2026).

---

## Summary Table

| Title | Authors | Year | Venue | Approach | Target | Notes |
|-------|---------|------|-------|----------|--------|-------|
| NeuSight | Yu et al. | 2025 | ASPLOS | Hybrid | GPU | Tile-based prediction, 2.3% error on GPT-3/H100 |
| ESM | various | 2025 | DAC | ML-Based | Multi | Surrogate framework for HW-aware NAS, 97.6% accuracy |
| LitePred | Feng et al. | 2024 | NSDI | ML-Based | Edge | Transfer learning, 99.3% on 85 platforms |
| Latency Predictors for NAS | Dudziak et al. | 2024 | MLSys | ML-Based | Multi | Comprehensive study, 22.5% improvement |
| TC-GNN | Wang et al. | 2022 | HPCA | GNN | GPU | Tensor Core GNN accelerator |
| GPU Occupancy GNN | various | 2023 | CLUSTER | GNN | GPU | GNN-based occupancy prediction |
| Roofline-LLM | Imai et al. | 2024 | NeurIPS-WS | Hybrid | GPU | Roofline + ML for LLM latency |
| TLP | Zhai et al. | 2023 | ASPLOS | ML-Based | Multi | Deep learning cost model for tensor programs |
| ALCOP | various | 2023 | MLSys | Hybrid | GPU | XGBoost with analytical pre-training |
| Energon | Zhou et al. | 2023 | HPCA | Analytical | ASIC | Dynamic sparse attention, 168x speedup |
| Primate | various | 2024 | ICCAD | ML-Based | PIM | Token pruning with processing-in-memory |
| SWAT | various | 2024 | ASP-DAC | Analytical | FPGA | Swin Transformer accelerator |

---

## Categorization by Focus Area

### Neural Network Surrogate Models

- **NeuSight** (2025) - Tile-based GPU performance prediction
  - Key innovation: Breaks kernel execution into tiles, predicts utilization per tile
  - Reduces GPT-3 latency error from 121.4% to 2.3% on H100
  - Supports H100, A100, V100, MI100, MI250

- **ESM** (2025) - Surrogate models for hardware-aware NAS
  - Framework for comparing surrogate model architectures
  - FCC encoding achieves 97.6% accuracy on ResNet supernet
  - Outperforms lookup table and statistical encoding

- **Habitat** (2021) - Runtime-based cross-GPU predictor
  - Uses wave scaling and pre-trained MLPs
  - Foundational work that NeuSight improves upon

- **LitePred** (2024) - Transferable latency prediction
  - VAE-based data sampler for efficient transfer
  - 99.3% accuracy on 85 edge platforms
  - Less than 1 hour adaptation cost

### GNN-Based Models for Dataflow/Graphs

- **TC-GNN** (2022) - Tensor Core acceleration for GNNs
  - First GPU TCU-based GNN framework
  - Reconciles sparse GNN computation with dense TCU
  - 1.70x speedup over Deep Graph Library

- **GNN Computational Graph** (2022) - IO/Memory optimization
  - Analyzes GNN dataflow from computation/IO/memory perspective
  - 2.75x speedup, 6.89x less memory IO, 7.73x less memory

- **HyperGef** (2023) - Hypergraph neural network fusion
  - Kernel fusion framework for HyperGNN on GPUs

- **GPU Occupancy GNN** (2023) - Occupancy prediction
  - Uses GNN to predict GPU occupancy for DL models

### Transfer Learning for Cross-Platform Prediction

- **Latency Predictors for NAS** (2024) - Comprehensive study
  - Analyzes transfer learning and meta-learning for NAS
  - 22.5% average improvement, up to 87.6% on hard tasks
  - End-to-end training strategy outperforms existing methods

- **Multi-Hardware Adaptive Latency** (2024) - Cross-platform
  - Adaptive prediction across different hardware platforms

- **CNN Latency Heterogeneous** (2024) - Mobile devices
  - Prediction across diverse mobile devices and ML frameworks

- **RISC-V NAS** (2024) - New architecture support
  - First latency-constrained NAS for RISC-V devices

### LLM Inference Performance Modeling

- **Roofline-LLM** (2024) - Roofline-driven ML method
  - Combines roofline model with machine learning
  - Interpretable performance ceiling for LLM inference

- **Latency-Aware Scaling** (2025) - Test-time scaling
  - Branch-wise parallelism improves accuracy with no extra time
  - Sequence-wise parallelism with speculative decoding

- **Edge LLM Survey** (2025) - Comprehensive survey
  - Covers speculative decoding and model offloading
  - Single-device and multi-device strategies

- **Queueing-LLM** (2025) - Queueing theory for LLM
  - Applies queueing theory to LLM serving performance
  - Addresses challenges in prediction and scheduling

### Hybrid Analytical + ML Models

- **TLP** (2023) - Deep learning cost model
  - Combines analytical insights with deep learning
  - For tensor program tuning in compilers

- **ALCOP** (2023) - XGBoost with analytical pre-training
  - Pre-trains XGBoost offline with analytical model predictions
  - Improves autotuning convergence

- **Calculon** (2023) - Distributed training model
  - Analytical decomposition of computation and communication
  - Scalable to large distributed systems

- **MAD-Max** (2024) - Memory-aware decomposition
  - Hybrid model for distributed training optimization

### Transformer Hardware Accelerators

- **Energon** (2023) - Dynamic sparse attention
  - Algorithm-architecture co-design
  - 168x speedup over CPU, 8.7x over V100 GPU

- **H3DAtten** (2023) - Hybrid in-memory computing
  - Combines analog and digital compute-in-memory
  - For vision transformers

- **ADAPTOR** (2024) - Runtime-adaptive FPGA
  - Adapts to varying transformer parameters
  - Dense matrix computation optimization

- **Primate** (2024) - PIM with dynamic pruning
  - Processing-in-memory with token pruning
  - Pipeline strategy for parallelism

- **SWAT** (2024) - Swin Transformer accelerator
  - Efficient FPGA design for Swin Transformer

- **Binarized Transformer** (2024) - End-to-end co-design
  - Hardware-software co-design for edge deployment

---

## Key Themes and Trends

### 1. Tile-Based Prediction Emerges as State-of-the-Art
- NeuSight's tile-level approach dramatically improves accuracy
- Mirrors actual GPU execution model (CUDA tiles)
- Enables prediction on unseen GPUs without execution

### 2. Transfer Learning Becomes Essential
- LitePred achieves 99.3% accuracy with minimal adaptation
- Meta-learning and few-shot approaches reduce data requirements
- Cross-platform prediction increasingly important

### 3. LLM Inference Requires New Modeling Approaches
- Roofline model being extended to LLM inference
- Speculative decoding changes performance characteristics
- Queueing theory provides new analytical foundations

### 4. Hybrid Models Outperform Pure Approaches
- Combining analytical models with ML improves accuracy
- Pre-training with analytical predictions speeds convergence
- Physics-informed approaches (NeuSight tiles) more robust

### 5. GNN-Based Models Enable Graph-Level Optimization
- GNNs model computational graphs effectively
- Enable kernel fusion and memory optimization
- Hardware-aware acceleration (TC-GNN)

---

## Papers to Deep-Dive (High Priority)

1. **NeuSight** - State-of-the-art GPU performance prediction
2. **LitePred** - Best transfer learning approach for edge devices
3. **Latency Predictors for NAS** - Comprehensive methodology comparison
4. **Roofline-LLM** - Bridges analytical and ML for LLM inference
5. **TLP** - Modern deep learning cost model for compilers

---

## Comparison: Surrogate vs Analytical Approaches

| Aspect | Surrogate/ML-Based | Analytical | Hybrid |
|--------|-------------------|------------|--------|
| Accuracy | High (95-99%) | Moderate (70-90%) | Highest (97-99%) |
| Generalization | Device-specific | Architecture-dependent | Best of both |
| Training Cost | Hours-days | None | Moderate |
| Interpretability | Low | High | Medium |
| New Hardware | Requires retraining | Manual updates | Minimal adaptation |
| Workload Types | Any with data | Well-understood only | Any |

---

## Gap Analysis for Survey

### Well-Covered Areas
- GPU performance prediction (many papers)
- Edge device latency (nn-Meter, LitePred)
- Tensor compiler cost models (TVM, Ansor, TLP)

### Emerging Areas (Need More Coverage)
- LLM-specific performance modeling
- Multi-device/distributed prediction
- Processing-in-memory performance models
- Quantum-classical hybrid workloads

### Underexplored Areas
- Online/adaptive cost models
- Uncertainty quantification in predictions
- Energy/power modeling with ML
- Model serving with heterogeneous hardware

---

## Relationship to Prior Work

This catalog extends our ML venues collection with:
- More recent papers (2023-2026 focus)
- Emphasis on surrogates and transfer learning
- LLM-specific modeling approaches
- Hardware accelerator co-design papers

Cross-references with architecture venues:
- NeuSight complements MAESTRO/Timeloop for GPU prediction
- Surrogate models can accelerate design space exploration in ArchGym
- Transfer learning applies to cross-accelerator prediction

---

## Notes

- Papers prioritized from peer-reviewed venues (ASPLOS, NSDI, MLSys, HPCA, DAC, ICCAD)
- Preprints included where they address key gaps
- Focus on papers with open-source implementations where possible
