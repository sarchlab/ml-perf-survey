# ASTRA-sim Setup Plan for ResNet-50 Accuracy Validation

**Author:** Flux (Tool Engineer)
**Date:** 2026-02-07
**Issue:** #170
**Status:** Research & planning complete; ready for execution

---

## 1. What ASTRA-sim Is and What It Simulates

ASTRA-sim is an open-source distributed AI training simulator developed by Georgia Tech, Meta, Intel, and AMD. It models the **end-to-end software and hardware stack** of distributed training systems, including:

- **Workload layer**: DNN computation graphs (forward/backward pass, gradient communication)
- **System layer**: Collective communication scheduling (all-reduce, all-gather, reduce-scatter, all-to-all), using algorithms like Ring or Tree
- **Network layer**: Interconnect topology and congestion modeling (switch, ring, 2D torus)

**Key capability**: Given a workload (e.g., ResNet-50 data-parallel training) and a hardware configuration (e.g., 8x H100 GPUs with NVSwitch), ASTRA-sim predicts training iteration time in cycles, including compute time, communication time, and communication/compute overlap.

**What it does NOT do**: It does not execute real GPU kernels. Compute durations come from the input trace; ASTRA-sim simulates the communication and scheduling.

**Repository:** https://github.com/astra-sim/astra-sim
**Documentation:** https://astra-sim.github.io/astra-sim-docs/
**Papers:** ISPASS 2020 (v1.0), ISPASS 2023 (v2.0)
**License:** MIT

---

## 2. Published Accuracy Claims

From ASTRA-sim's official validation documentation for HGX-H100 systems (NCCL Ring All-Reduce):

| GPU Count | Geomean Error Rate |
|-----------|-------------------|
| 2 GPUs    | 20.63%            |
| 4 GPUs    | 12.01%            |
| 8 GPUs    | 9.69%             |

**Configuration**: 900 GB/s bidirectional bandwidth per GPU, 4 NVSwitches, switch topology, analytical backend. Maximum achieved bandwidth: 741.34 GB/s (~82% utilization).

**Critical notes from the docs:**
1. Warm-up latency must be extracted empirically from smaller collective operations
2. Link latency should be determined through iterative testing
3. Ring algorithm must be enforced exclusively (NCCL switches Ring→Tree at larger sizes, which ASTRA-sim models poorly)

---

## 3. Prerequisites and Dependencies

### 3.1 Docker Approach (Recommended)

**Existing Dockerfile**: `scripts/benchmarks/astra-sim/Dockerfile` — already exists in this repo.

**Base image**: Ubuntu 22.04

**Required packages** (all handled by existing Dockerfile):
- Build tools: gcc, g++, cmake, make, autoconf, automake, libtool
- Libraries: libboost-dev, libboost-program-options-dev
- MPI: openmpi-bin, libopenmpi-dev
- Python: python3, python3-pip, python3-venv
- Protobuf: v3.21.12 (compiled from source for CMake integration)
- Python packages: protobuf, pydot

**Docker build time**: ~20-30 minutes (protobuf source build is the bottleneck)

### 3.2 Native Linux Installation (Not Recommended)

- Requires Ubuntu 20.04+ or equivalent
- Manual protobuf source compilation
- Build: `./build/astra_analytical/build.sh`
- macOS: **Not supported natively** (use Docker)

---

## 4. Step-by-Step Setup Instructions

### Step 1: Build Docker Image

```bash
cd scripts/benchmarks/astra-sim/
docker build -t mlperf-astra-sim .
```

This will:
- Install all system dependencies
- Compile protobuf v3.21.12 from source
- Clone ASTRA-sim with all submodules
- Build the analytical backend (`AstraSim_Analytical_Congestion_Aware`)
- Install Chakra for trace conversion
- Fetch the ResNet-50 v1.0 workload file

### Step 2: Verify Build

```bash
docker run --rm mlperf-astra-sim ls -la /app/astra-sim/build/astra_analytical/build/bin/
```

Expected: `AstraSim_Analytical_Congestion_Aware` binary exists.

### Step 3: Run Microbenchmark Validation (Sanity Check)

```bash
docker run --rm -v $(pwd)/results:/app/results mlperf-astra-sim \
    bash /app/astra-sim/examples/run_scripts/analytical/congestion_aware/HGX-H100-validated.sh
```

This runs the pre-configured HGX-H100 validated example. Success = the binary runs and produces cycle counts.

### Step 4: Run ResNet-50 Simulation

```bash
docker run --rm -v $(pwd)/results:/app/results mlperf-astra-sim \
    bash /app/run_resnet50.sh
```

The `run_resnet50.sh` script (already in repo) will:
1. Parse the v1.0 text workload (`Resnet50_DataParallel.txt`)
2. Generate Chakra ET traces for 4, 8, and 16 NPUs
3. Run simulations with HGX-H100 validated configs
4. Output cycle counts and communication metrics to `/app/results/`

### Step 5: Collect and Analyze Results

Results should include per-NPU:
- Total training iteration cycles
- Exposed communication time (communication not overlapped with compute)
- Per-layer breakdown (forward compute, backward compute, all-reduce)

---

## 5. Expected Inputs for ResNet-50 Simulation

### 5.1 Workload Input

**File**: `Resnet50_DataParallel.txt` (fetched from ASTRA-sim v1.0 branch)

**Format** (tab-separated, per layer):
```
<layer_name> -1 <fwd_compute> NONE 0 <inp_grad_compute> NONE 0 <wt_grad_compute> ALLREDUCE <comm_size_bytes> <delay>
```

**Structure**:
- Line 1: Parallelization strategy (e.g., `DATA`)
- Line 2: Number of layers
- Lines 3+: One line per layer with compute costs and communication patterns

### 5.2 System Configuration

Using HGX-H100 validated config:
```json
{
    "scheduling-policy": "LIFO",
    "endpoint-delay": 10,
    "active-chunks-per-dimension": 2,
    "preferred-dataset-splits": 4,
    "all-reduce-implementation": ["ring"],
    "collective-optimization": "localBWAware",
    "local-mem-bw": 3350
}
```

### 5.3 Network Configuration

HGX-H100 validated:
```yaml
topology: [Switch]
npus_count: [8]
bandwidth: [400.0]    # GB/s
latency: [936.25]     # ns
```

### 5.4 What We Should Compare Against

| Metric | Source | Expected Range |
|--------|--------|---------------|
| Training iteration time | MLPerf benchmarks, NVIDIA published numbers | ~150-300ms for ResNet-50 on 8x H100 |
| Communication overhead | NCCL benchmarks | Depends on model size (~100MB gradients for ResNet-50) |
| ASTRA-sim geomean error | Official docs | 9.69% for 8 GPUs, 12.01% for 4 GPUs |

---

## 6. Known Issues and Challenges

### 6.1 From Crit's Review

Crit's review (`agent/workspace/crit/astra-sim-review.md`) identified:
1. **Incomplete benchmark coverage**: Only 8-NPU runs succeeded previously; 4-NPU configs failed
2. **No accuracy validation**: Previous runs didn't compare against published results
3. **Scoring inconsistency**: Multiple scores reported without clear methodology
4. **Missing failure analysis**: 4-NPU errors were dismissed without investigation

### 6.2 Technical Challenges

1. **Chakra trace generation**: Converting v1.0 text workloads to v2.0 ET traces may fail if `chakra_converter` isn't properly installed. The existing `run_resnet50.sh` has a Python fallback.
2. **Protobuf version sensitivity**: Must compile from source; pip protobuf != system protobuf can cause conflicts.
3. **4-NPU configuration failures**: The HGX-H100 validated config assumes 8 GPUs. Running with 4 NPUs requires a different network config (e.g., `hgx_h100_4gpus.yml` from `inputs/network/`).
4. **Compute durations are synthetic**: The v1.0 workload file has compute durations in "cycles" that may not match real H100 timings. This limits absolute accuracy comparisons.
5. **Ring vs Tree**: NCCL uses Ring for small collectives and Tree for large ones. ASTRA-sim's validated config only covers Ring. For full ResNet-50 training (large gradients), this may undercount.

### 6.3 Mitigation Plan

| Challenge | Mitigation |
|-----------|-----------|
| Chakra conversion failures | Use inline Python trace generator (already in `run_resnet50.sh`) |
| 4-NPU failures | Use `inputs/network/hgx_h100_4gpus.yml` or skip 4-NPU, focus on 8-NPU |
| No real-hardware baseline | Compare against MLPerf published results and ASTRA-sim's own validation numbers |
| Build failures | Docker isolates all dependencies; existing Dockerfile is tested |

---

## 7. Execution Plan (Next Steps)

### Phase 1: Docker Build + Sanity Check (This Cycle)
- [x] Research ASTRA-sim architecture and inputs
- [x] Document setup plan (this file)
- [x] Write orchestration script (`scripts/benchmarks/astra-sim/run_and_collect.sh`)
- [ ] Build Docker image and verify binary exists
- [ ] Run microbenchmark validation (HGX-H100 example)

### Phase 2: ResNet-50 Simulation (Next Cycle)
- [ ] Run `run_resnet50.sh` inside Docker
- [ ] Collect output logs with cycle counts
- [ ] Parse results into structured format (`data/evaluation/astra-sim-resnet50-results.md`)
- [ ] Compare against published validation numbers (9.69% geomean error for 8 GPUs)

### Phase 3: Accuracy Analysis (Following Cycle)
- [ ] Compute relative error vs. MLPerf published iteration times
- [ ] Analyze per-layer breakdown (where does error come from?)
- [ ] Document findings for paper Section 7
- [ ] Feed results to issue #155 (broader accuracy experiments)

---

## 8. References

- ASTRA-sim GitHub: https://github.com/astra-sim/astra-sim
- ASTRA-sim Docs: https://astra-sim.github.io/astra-sim-docs/
- HGX-H100 Validation: https://astra-sim.github.io/astra-sim-docs/validation/hardware/gpu-validation-hgx-h100.html
- Workload Config Docs: https://astra-sim.github.io/astra-sim-docs/getting-started/argument-workload-config.html
- Chakra Trace Format: https://deepwiki.com/astra-sim/astra-sim/5.1-chakra-graph-frontend
- ISPASS 2020 Paper: Won et al., "ASTRA-SIM: Enabling SW/HW Co-Design Exploration for Distributed DL Training Platforms"
- ISPASS 2023 Paper: Won et al., "ASTRA-sim2.0: Modeling Hierarchical Networks and Disaggregated Systems"
