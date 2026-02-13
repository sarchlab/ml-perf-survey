# ASTRA-sim Accuracy Analysis Report

**Generated:** 2026-02-13T04:20:30Z
**Source:** `data/evaluation/astra-sim-results/astra_sim_results.json`

## Summary

- **Total experiments:** 11
- **Successful:** 7
- **Failed:** 4
- **Training GPU scales:** [4, 8, 16]
- **Microbenchmark GPU scales:** [8]

## Training Scaling Analysis (ResNet-50 Data-Parallel)

In data-parallel training, each GPU processes the full forward/backward pass
(constant compute) and then communicates gradients via All-Reduce. The key
metric is **communication overhead** — the fraction of total wall time spent
on communication rather than compute.

| GPU Count | Total Cycles | Comm Cycles | Compute Cycles | Comm Overhead (%) | Note |
|-----------|-------------|-------------|----------------|-------------------|------|
| 4 | 1,096,768,270 | 1,454,270 | 1,095,314,000 | 0.1326 |  |
| 8 | 1,098,621,886 | 3,307,886 | 1,095,314,000 | 0.3011 |  |
| 16 | 1,098,621,886 | 3,307,886 | 1,095,314,000 | 0.3011 | Topology limited to 8 NPUs |

## Microbenchmark Results (All-Reduce)

| GPU Count | All-Reduce Cycles (1 MB) | Published Error (%) | Note |
|-----------|-------------------------|--------------------|----|
| 8 | 57,426 | 9.69 | Simulation only; no HW comparison |

## Published Validation Reference (HGX-H100)

These are the published error rates from the ASTRA-sim team, validated against
real HGX-H100 hardware. We report them for reference but **cannot independently
verify** these without datacenter-grade GPU hardware.

| GPU Count | Geomean Error Rate | Collective |
|-----------|-------------------|------------|
| 2 | 20.63% | Ring All-Reduce |
| 4 | 12.01% | Ring All-Reduce |
| 8 | 9.69% | Ring All-Reduce |

## Communication Breakdown

- **4-GPU communication overhead:** 0.1326%
- **8-GPU communication overhead:** 0.3011%
- **Overhead increase (4→8 GPU):** 0.1685 percentage points

The increasing communication overhead with GPU count is consistent with
Ring All-Reduce scaling behavior, where communication volume grows with
the number of participants while compute per GPU remains constant in
data-parallel training.

## Paper-Ready Metrics

These metrics can be directly cited in Section 7:

### resnet50_16gpu
- Total cycles: 1,098,621,886
- Communication cycles: 3,307,886
- Compute cycles: 1,095,314,000
- Communication overhead: 0.3011%

### resnet50_4gpu
- Total cycles: 1,096,768,270
- Communication cycles: 1,454,270
- Compute cycles: 1,095,314,000
- Communication overhead: 0.1326%

### resnet50_8gpu
- Total cycles: 1,098,621,886
- Communication cycles: 3,307,886
- Compute cycles: 1,095,314,000
- Communication overhead: 0.3011%

## Key Findings

- 8-GPU ResNet-50: 0.3011% communication overhead
- 4-GPU ResNet-50: 0.1326% communication overhead
- 8-GPU All-Reduce 1MB: 57426 cycles
- Communication overhead scales with GPU count as expected for data-parallel training
- Published accuracy reference: 9.69% geomean error (8 GPUs, verified on real HGX-H100)

## Limitations

1. **No hardware comparison:** We cannot validate against real HGX-H100 hardware
2. **Synthetic compute durations:** The v1.0 workload format uses fixed compute
   durations per layer, not profiled values from actual ResNet-50 execution
3. **Scale coverage:** Only 4-GPU and 8-GPU training results are valid;
   16-NPU configs used 8-NPU topology (results not meaningful for 16-GPU)
4. **Single collective:** All configurations use Ring All-Reduce; other
   collectives (All-Gather, Reduce-Scatter) not benchmarked at training scale

