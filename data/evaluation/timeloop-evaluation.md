# Timeloop Reproducibility Evaluation

This document assesses Timeloop's reproducibility, usability, and practical considerations for ML performance modeling research.

---

## Overview

**Tool:** Timeloop
**Paper:** "Timeloop: A Systematic Approach to DNN Accelerator Evaluation" (ISPASS 2019)
**Authors:** Parashar et al. (NVIDIA, MIT)
**Repository:** https://github.com/NVlabs/timeloop
**License:** BSD 3-Clause
**Evaluation Date:** 2026-02-07

---

## Setup Assessment

### Installation Options

| Method | Complexity | Time to First Result | Recommended For |
|--------|------------|---------------------|-----------------|
| Docker | Low | ~10-15 minutes | New users, quick evaluation |
| Native (Linux) | High | 1-2 hours | Development, production use |
| Native (macOS) | Very High | Not officially supported | Not recommended |

### Docker Setup (Recommended)

**Steps:**
```bash
git clone https://github.com/Accelergy-Project/timeloop-accelergy-exercises.git
cd timeloop-accelergy-exercises
cp docker-compose.yaml.template docker-compose.yaml
# Edit USER_UID/USER_GID as needed
DOCKER_ARCH=arm64 docker-compose up  # or amd64 for Intel/AMD
```

**Notes:**
- Pre-built images available for both arm64 (Apple Silicon) and amd64
- Includes Jupyter notebook interface for interactive exploration
- Workspace mounted for persistent file access
- Requires Docker daemon to be running

### Native Installation (Linux Only)

**Dependencies:**
1. Build tools: g++, cmake, scons, autotools
2. Libraries: libconfig++, libboost (filesystem, iostreams, log, serialization, thread), libyaml-cpp, libncurses, libgmp
3. NTL library (v11.5.1) - requires source build
4. Barvinok library (v0.41.6) - requires source build (~30 min compilation)

**Approximate Installation Time:** 1-2 hours including dependency builds

**Key Observation:** Native installation is Linux-specific due to apt-get dependencies. macOS users should use Docker.

---

## Repository Structure

```
timeloop/
├── configs/           # Example configurations (Eyeriss, Simba, etc.)
├── doc/               # Mapper documentation
├── src/               # C++ source code
├── scripts/           # Utility scripts
└── tests/             # Test configurations

timeloop-accelergy-exercises/
└── workspace/
    ├── tutorial_exercises/  # Step-by-step tutorials
    ├── example_designs/     # Reference architectures
    │   ├── eyeriss_like/
    │   ├── simba_like/
    │   ├── simple_weight_stationary/
    │   └── simple_output_stationary/
    └── layer_shapes/        # DNN workload specifications
        ├── resnet18/        # 21 layers
        ├── vgg16/           # 17 layers
        ├── alexnet/         # 9 layers
        ├── gpt2/            # 147 layers
        ├── vision_transformer/
        └── mobilebert/
```

---

## Workload Coverage

### Pre-defined Models

| Model | Layers | Type |
|-------|--------|------|
| AlexNet | 9 | CNN |
| VGG16 | 17 | CNN |
| ResNet18 | 21 | CNN |
| DenseNet201 | 202 | CNN |
| MobileNet-V3 | 65 | Mobile CNN |
| GPT-2 | 147 | Transformer |
| MobileBERT | 410 | Transformer |
| Vision Transformer (DPT-Large) | 228 | Vision Transformer |
| Phi-1.5 | 147 | LLM |

### Custom Workload Definition

Workloads are specified in YAML format:
```yaml
problem:
  instance: {C: 3, M: 64, P: 112, Q: 112, R: 7, S: 7, HStride: 2, WStride: 2}
```

Scripts provided for generating workloads from PyTorch models.

---

## Output Analysis

### Sample Output (Eyeriss-like, default problem)

**Summary Statistics:**
- GFLOPS @1GHz: 247.33
- PE Utilization: 75.00%
- Total Cycles: 86,016
- Total Energy: 59.28 uJ
- EDP: 5.10e+00 J*cycle

**Energy Breakdown (fJ/Compute):**

| Component | Energy | Percentage |
|-----------|--------|------------|
| DRAM | 3380.86 | 61.8% |
| weights_spad | 1006.69 | 18.4% |
| psum_spad | 386.77 | 7.1% |
| shared_glb | 375.27 | 6.9% |
| mac | 207.69 | 3.8% |
| ifmap_spad | 112.37 | 2.1% |
| **Total** | **5469.65** | **100%** |

**Key Insight:** DRAM dominates energy (62%), validating dataflow optimization importance.

---

## Accuracy Claims vs. Reality

### Published Claims (ISPASS 2019)

- Energy: within 10% of RTL simulation
- Latency: cycle-accurate at memory buffer level
- Validated against Eyeriss silicon measurements

### Evaluation Observations

1. **Reference outputs provided:** All example designs include pre-computed reference outputs for verification
2. **Deterministic results:** Same configuration produces identical results
3. **Consistent with literature:** Energy breakdown matches Eyeriss paper patterns

### Limitations Noted

From the documentation:
- Mapper may not find globally optimal mappings (uses heuristics)
- Non-divisible tiling factors not explored (requires workload padding)
- Convergence time varies (30 min typical, can be longer)

---

## Usability Assessment

### Strengths

| Aspect | Rating | Notes |
|--------|--------|-------|
| Documentation | Excellent | Tutorials, wiki, Jupyter notebooks |
| Example coverage | Excellent | Multiple architectures and workloads |
| Output detail | Excellent | Per-component energy, bandwidth, utilization |
| Input flexibility | Good | YAML-based, supports Jinja2 templates |
| Community | Good | Active GitHub, maintained by NVIDIA |

### Challenges

| Aspect | Rating | Notes |
|--------|--------|-------|
| Installation | Moderate | Docker easy; native complex |
| macOS support | Poor | Not officially supported |
| Learning curve | Steep | Many concepts (dataflow, mapping space) |
| Simulation time | Variable | Can be 30+ minutes for complex problems |

---

## Reproducibility Checklist

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Source code available | Yes | Full C++ source |
| Build instructions | Yes | Makefile, documentation |
| Dependencies documented | Yes | README, Makefile |
| Pre-built containers | Yes | Docker images (arm64, amd64) |
| Example inputs | Yes | Multiple architectures |
| Reference outputs | Yes | Included in exercises |
| Test suite | Partial | Basic tests, but limited coverage |

**Reproducibility Score: 9/10**

---

## Practical Recommendations

### For Researchers

1. **Start with Docker** - Gets you running in 15 minutes
2. **Follow the tutorials** - Essential for understanding dataflow concepts
3. **Use pre-defined architectures** - Eyeriss, Simba are well-validated
4. **Verify with reference outputs** - Compare your results to included baselines

### For Practitioners

1. **Design space exploration** - Use mapper for automatic optimization
2. **Energy estimation** - Pair with Accelergy for accurate energy modeling
3. **Architecture comparison** - Leverage multiple included designs
4. **Custom workloads** - Use provided scripts to generate from PyTorch

### Known Limitations

1. **Not for GPU modeling** - Designed for spatial accelerators (TPU-like, Eyeriss-like)
2. **Mapping heuristics** - May not find global optimum
3. **Simulation time** - Can be slow for large design spaces
4. **Linux-focused** - Docker required for other platforms

---

## Comparison with Alternatives

| Tool | Focus | Speed | Ease of Use |
|------|-------|-------|-------------|
| **Timeloop** | Spatial accelerators | Fast (analytical) | Moderate |
| SCALE-Sim | Systolic arrays | Fast | Easy |
| MAESTRO | Dataflow modeling | Fast | Easy |
| Accel-Sim/GPGPU-Sim | GPUs | Very slow (cycle-accurate) | Hard |

---

## Conclusion

**Timeloop is highly reproducible and well-suited for DNN accelerator research.**

Key findings:
- Docker provides quick, reliable setup
- Extensive examples and documentation
- Reference outputs enable result verification
- Active maintenance by NVIDIA

Recommended for:
- Accelerator architecture research
- Dataflow optimization studies
- Energy efficiency analysis
- Educational purposes

Not recommended for:
- GPU kernel modeling (use Accel-Sim instead)
- Production deployment (analytical, not cycle-accurate)
- Quick latency estimates (use nn-Meter for edge devices)

---

*Evaluation by Leo | ML Performance Survey Project*
