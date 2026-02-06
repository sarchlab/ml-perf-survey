# Architecture Venues Paper Summary

Papers on ML/DNN performance modeling from MICRO, ISCA, HPCA, ASPLOS (2016-2025).

---

## Summary Table

| Title | Authors | Year | Venue | Approach | Target HW | Notes |
|-------|---------|------|-------|----------|-----------|-------|
| Eyeriss: Spatial Architecture for Energy-Efficient Dataflow | Chen, Emer, Sze | 2016 | ISCA | Analytical | NPU | Foundational row stationary dataflow |
| Timeloop: Systematic DNN Accelerator Evaluation | Parashar et al. | 2019 | ISPASS | Analytical | NPU | Core analytical framework |
| MAESTRO: Understanding DNN Dataflows | Kwon et al. | 2019 | MICRO | Analytical | NPU | Data-centric cost model |
| Path Forward Beyond Simulators | Li, Sun, Jog | 2020 | HPCA | ML-Based | GPU | Fast GPU execution prediction |
| MLPerf Inference Benchmark | Reddi et al. | 2020 | ISCA | Benchmark | Multi | Industry standard ML benchmark |
| Habitat: Runtime Performance Predictor | Yu et al. | 2021 | ATC | ML-Based | GPU | Cross-GPU prediction, 11.8% error |
| Sparseloop: Sparse Tensor Accelerator Modeling | Wu, Sze, Emer | 2022 | MICRO | Analytical | NPU | 2000x faster than simulation |
| GRANITE: GNN Throughput Estimation | Sykora et al. | 2022 | IISWC | ML-Based | CPU | GNN-based basic block prediction |
| Themis: Network-Aware Scheduling | various | 2022 | ISCA | Analytical | Multi | Distributed training modeling |
| ArchGym: ML-Assisted Architecture Design | Krishnan et al. | 2023 | ISCA | Hybrid | Multi | Framework connecting ML to simulators |
| Regression Model for DNN Latency | Li, Sun, Jog | 2023 | ISPASS | ML-Based | GPU | End-to-end latency prediction |
| MoCA: Memory-Centric Execution | Shao et al. | 2023 | HPCA | Analytical | NPU | Multi-tenant DNN performance |
| MERCURY: Input Similarity Acceleration | various | 2023 | HPCA | Hybrid | GPU | Training acceleration |
| ADA-GP: Adaptive Gradient Prediction | various | 2023 | MICRO | ML-Based | GPU | Gradient prediction for training |
| ASTRA-sim: Distributed ML Simulation | Won et al. | 2023 | arXiv | Simulation | Multi | Full-system distributed simulation |
| Soter: Tensor-Architecture Modeling | various | 2024 | ISCA | Analytical | NPU | Spatial accelerator modeling |
| Tandem Processor | Park et al. | 2024 | ASPLOS | Analytical | NPU | Emerging DNN operators |
| TAO: DL-based Microarch Simulation | various | 2024 | SIGMETRICS | ML-Based | Multi | Transfer learning for simulation |
| BBS: Bi-directional Bit-level Sparsity | various | 2024 | MICRO | Analytical | NPU | Sparsity-aware acceleration |
| SCAR: Multi-Model Scheduling | various | 2024 | MICRO | Analytical | NPU | Multi-chiplet scheduling |
| NeuSight: GPU Performance Forecasting | Lee, Phanishayee, Mahajan | 2025 | ASPLOS | ML-Based | GPU | Tile-based prediction, 8.9% error |
| TrioSim: Multi-GPU DNN Simulation | various | 2025 | ISCA | Simulation | GPU | Large-scale multi-GPU simulation |

---

## Categorization by Approach

### Analytical Models
- **Timeloop** (2019) - Foundational framework for DNN accelerator modeling
- **MAESTRO** (2019) - Data-centric cost model for dataflows
- **Sparseloop** (2022) - Extension for sparse tensor accelerators
- **Soter** (2024) - Spatial accelerator modeling

### ML-Based Models
- **Path Forward Beyond Simulators** (2020) - GPU execution prediction
- **Habitat** (2021) - Cross-GPU training performance prediction
- **GRANITE** (2022) - GNN for basic block throughput
- **NeuSight** (2025) - Tile-based GPU performance forecasting

### Simulation-Based
- **ASTRA-sim** (2023) - Distributed ML platform simulation
- **TrioSim** (2025) - Multi-GPU DNN workload simulation

### Hybrid Approaches
- **ArchGym** (2023) - ML + simulator integration
- **TAO** (2024) - DL-enhanced microarchitecture simulation

---

## Categorization by Target Hardware

### GPU
- Path Forward Beyond Simulators (HPCA 2020)
- Habitat (ATC 2021)
- MERCURY (HPCA 2023)
- ADA-GP (MICRO 2023)
- NeuSight (ASPLOS 2025)
- TrioSim (ISCA 2025)

### DNN Accelerators/NPU
- Eyeriss (ISCA 2016)
- Timeloop (ISPASS 2019)
- MAESTRO (MICRO 2019)
- Sparseloop (MICRO 2022)
- MoCA (HPCA 2023)
- Soter (ISCA 2024)
- Tandem Processor (ASPLOS 2024)

### Multi-Device/Distributed
- MLPerf (ISCA 2020)
- Themis (ISCA 2022)
- ArchGym (ISCA 2023)
- ASTRA-sim (2023)
- TAO (SIGMETRICS 2024)

---

## Key Observations

1. **Analytical models dominate accelerator design**: Timeloop/MAESTRO family provides fast exploration
2. **ML-based models gaining traction for GPUs**: NeuSight achieves 8.9% error across diverse GPUs
3. **Sparse/irregular workloads remain challenging**: Sparseloop addresses this gap
4. **Distributed training modeling emerging**: ASTRA-sim, Themis for multi-device scenarios
5. **Hybrid approaches combining speed and accuracy**: ArchGym, TAO blend analytical and learned components

---

## Papers to Deep-Dive (High Priority)

1. **Timeloop/Sparseloop** - Core analytical framework used widely
2. **NeuSight** - State-of-the-art GPU prediction
3. **MAESTRO** - Alternative analytical approach
4. **Habitat** - Practical cross-GPU prediction
5. **ASTRA-sim** - Distributed training simulation
