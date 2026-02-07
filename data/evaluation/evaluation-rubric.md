# Evaluation Metrics and Rubric for Third-Party Tool Comparison

This document defines the metrics and scoring rubric for evaluating ML performance modeling tools in our third-party evaluation. The rubric enables systematic, transparent comparison across four dimensions: Accuracy, Ease of Use, Performance, and Extensibility.

---

## Overview

### Evaluation Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Accuracy | 40% | Prediction quality vs ground truth |
| Ease of Use | 25% | Setup complexity and user experience |
| Performance | 20% | Prediction speed and scalability |
| Extensibility | 15% | Ability to add new models/hardware |

### Scoring Scale

All dimensions use a 1-10 scale:
- **9-10**: Exceptional (best in class)
- **7-8**: Good (meets expectations)
- **5-6**: Adequate (usable with limitations)
- **3-4**: Poor (significant issues)
- **1-2**: Unacceptable (fundamental problems)

---

## Dimension 1: Accuracy (40%)

### Definition

How closely do tool predictions match real hardware measurements?

### Metrics

| Metric | Formula | Weight | Interpretation |
|--------|---------|--------|----------------|
| MAPE | mean(abs(pred-actual)/actual) * 100 | 50% | Lower is better |
| Spearman Correlation | rank correlation coefficient | 30% | Higher is better |
| Max Error | max(abs(pred-actual)/actual) * 100 | 20% | Lower is better |

### Ground Truth Establishment

| Workload Category | Ground Truth Method |
|-------------------|-------------------|
| CNN/Transformer | PyTorch profiler, ONNX Runtime |
| Edge Inference | On-device measurement (TFLite) |
| LLM Inference | vLLM/TGI benchmarks |
| Distributed Training | NCCL tests, published results |

**Ground Truth Requirements:**
- Minimum 3 runs per configuration
- Report mean and standard deviation
- Document hardware, software versions
- Control for thermal throttling, background processes

### Scoring Rubric

| Score | MAPE | Correlation | Max Error | Description |
|-------|------|-------------|-----------|-------------|
| 10 | <2% | >0.99 | <5% | Near-perfect predictions |
| 9 | 2-5% | 0.97-0.99 | 5-10% | Excellent accuracy |
| 8 | 5-8% | 0.95-0.97 | 10-15% | Very good accuracy |
| 7 | 8-12% | 0.92-0.95 | 15-20% | Good accuracy |
| 6 | 12-15% | 0.88-0.92 | 20-30% | Acceptable accuracy |
| 5 | 15-20% | 0.83-0.88 | 30-40% | Marginal accuracy |
| 4 | 20-30% | 0.75-0.83 | 40-50% | Poor accuracy |
| 3 | 30-50% | 0.60-0.75 | 50-75% | Very poor accuracy |
| 2 | 50-100% | 0.40-0.60 | 75-100% | Unreliable predictions |
| 1 | >100% | <0.40 | >100% | Predictions unusable |

### Category-Specific Considerations

**Single Operator Predictions:**
- Evaluate per-layer accuracy independently
- Report distribution of errors across layers
- Identify systematic biases (e.g., convolutions overestimated)

**End-to-End Model Predictions:**
- Evaluate total latency/throughput
- Check if errors compound or cancel
- Weight by layer compute fraction

**Scaling Predictions:**
- Evaluate across batch sizes, sequence lengths
- Check extrapolation accuracy beyond training range
- Test parallelism scaling (TP2, TP4, TP8)

---

## Dimension 2: Ease of Use (25%)

### Definition

How accessible is the tool for new users and production deployment?

### Sub-Dimensions

| Sub-Dimension | Weight | Description |
|---------------|--------|-------------|
| Setup Complexity | 35% | Time and effort to first result |
| Documentation Quality | 30% | Clarity and completeness |
| API Design | 20% | Intuitiveness and consistency |
| Error Handling | 15% | Helpful error messages, recovery |

### Scoring Rubric: Setup Complexity (35%)

| Score | Time to First Result | Dependencies | Platform Support |
|-------|---------------------|--------------|------------------|
| 10 | <5 min | pip install only | All platforms |
| 9 | 5-15 min | pip + minimal | Linux, macOS, Windows |
| 8 | 15-30 min | pip + some manual | Linux, macOS |
| 7 | 30-60 min | Docker available | Linux, Docker |
| 6 | 1-2 hours | Docker required | Docker only |
| 5 | 2-4 hours | Build from source | Linux only |
| 4 | 4-8 hours | Complex build | Specific Linux |
| 3 | 1 day | Custom dependencies | With workarounds |
| 2 | 2+ days | Significant debugging | Barely functional |
| 1 | Fails to install | Broken dependencies | Cannot install |

### Scoring Rubric: Documentation Quality (30%)

| Score | Criteria |
|-------|----------|
| 10 | Comprehensive tutorials, API reference, examples for all features, video guides |
| 9 | Complete tutorials, good API docs, many examples |
| 8 | Good tutorials, API reference, adequate examples |
| 7 | Basic tutorials, partial API docs, some examples |
| 6 | README with examples, minimal API docs |
| 5 | README only, examples but no explanation |
| 4 | Sparse README, few examples, outdated docs |
| 3 | Minimal README, no examples |
| 2 | Wrong/misleading documentation |
| 1 | No documentation |

### Scoring Rubric: API Design (20%)

| Score | Criteria |
|-------|----------|
| 10 | Intuitive, consistent, IDE support, type hints, great defaults |
| 9 | Clear API, good naming, reasonable defaults |
| 8 | Usable API, some inconsistencies, adequate defaults |
| 7 | Functional API, learning curve, configuration heavy |
| 6 | Complex API, many required parameters |
| 5 | Confusing API, trial-and-error needed |
| 4 | Inconsistent API, undocumented behavior |
| 3 | Cumbersome API, manual file editing required |
| 2 | Nearly unusable API, significant workarounds |
| 1 | No programmatic API |

### Scoring Rubric: Error Handling (15%)

| Score | Criteria |
|-------|----------|
| 10 | Clear error messages, suggestions for fixes, graceful degradation |
| 9 | Informative errors, points to issue location |
| 8 | Helpful errors for common issues |
| 7 | Basic error messages, identifiable cause |
| 6 | Generic errors, some debugging needed |
| 5 | Cryptic errors, stack traces |
| 4 | Silent failures, inconsistent behavior |
| 3 | Crashes without useful info |
| 2 | Corrupts state on error |
| 1 | Unrecoverable failures |

---

## Dimension 3: Performance (20%)

### Definition

How fast and scalable is the tool for practical use cases?

### Sub-Dimensions

| Sub-Dimension | Weight | Description |
|---------------|--------|-------------|
| Prediction Speed | 50% | Time per prediction |
| Scalability | 30% | Performance on large workloads |
| Resource Efficiency | 20% | Memory and CPU usage |

### Scoring Rubric: Prediction Speed (50%)

For single-layer prediction latency:

| Score | Time per Prediction | Use Case |
|-------|-------------------|----------|
| 10 | <1 ms | Real-time NAS integration |
| 9 | 1-10 ms | Fast NAS loops |
| 8 | 10-100 ms | Interactive exploration |
| 7 | 100 ms - 1 s | Batch evaluation |
| 6 | 1-10 s | Offline analysis |
| 5 | 10-60 s | Single model evaluation |
| 4 | 1-10 min | Occasional use |
| 3 | 10-60 min | Research only |
| 2 | 1+ hour | Impractical |
| 1 | >1 day | Unusable |

For end-to-end model (e.g., ResNet-50):

| Score | Time per Model | Description |
|-------|---------------|-------------|
| 10 | <100 ms | Suitable for NAS |
| 9 | 100 ms - 1 s | Fast iteration |
| 8 | 1-10 s | Interactive |
| 7 | 10-60 s | Batch friendly |
| 6 | 1-5 min | Acceptable |
| 5 | 5-15 min | Slow but usable |
| 4 | 15-60 min | Impractical for exploration |
| 3 | 1-4 hours | Research only |
| 2 | 4-24 hours | Very slow |
| 1 | >1 day | Unusable |

### Scoring Rubric: Scalability (30%)

| Score | Criteria |
|-------|----------|
| 10 | Linear scaling, 1000+ layers, distributed support |
| 9 | Near-linear scaling, handles large models easily |
| 8 | Good scaling, occasional slowdown on very large models |
| 7 | Adequate scaling, noticeable slowdown on large models |
| 6 | Moderate scaling, struggles with 100+ layer models |
| 5 | Poor scaling, practical limit ~50 layers |
| 4 | Significant bottlenecks, limit ~20 layers |
| 3 | Does not scale, only small models |
| 2 | Crashes on medium models |
| 1 | Only toy examples work |

### Scoring Rubric: Resource Efficiency (20%)

| Score | Peak RAM | CPU Usage | Description |
|-------|----------|-----------|-------------|
| 10 | <500 MB | <1 core | Minimal footprint |
| 9 | 500 MB - 1 GB | 1-2 cores | Light resource use |
| 8 | 1-2 GB | 2-4 cores | Moderate use |
| 7 | 2-4 GB | 4-8 cores | Acceptable |
| 6 | 4-8 GB | 8-16 cores | Heavy use |
| 5 | 8-16 GB | 16+ cores | Resource intensive |
| 4 | 16-32 GB | - | Requires workstation |
| 3 | 32-64 GB | - | Requires server |
| 2 | 64-128 GB | - | HPC only |
| 1 | >128 GB | - | Impractical |

---

## Dimension 4: Extensibility (15%)

### Definition

How easily can users extend the tool to new models, operators, or hardware?

### Sub-Dimensions

| Sub-Dimension | Weight | Description |
|---------------|--------|-------------|
| Adding New Models | 40% | Effort to add unsupported models |
| Adding New Hardware | 40% | Effort to add new accelerators |
| Customization | 20% | Ability to modify internals |

### Scoring Rubric: Adding New Models (40%)

| Score | Criteria |
|-------|----------|
| 10 | Automatic import from PyTorch/ONNX, no manual work |
| 9 | Simple configuration file, <10 min for new model |
| 8 | Configuration + minor scripting, <1 hour |
| 7 | Moderate effort, 1-4 hours for new model |
| 6 | Significant effort, 4-8 hours, some expertise needed |
| 5 | Major effort, 1-2 days, deep tool knowledge required |
| 4 | Very difficult, 2-5 days, requires modifying source |
| 3 | Extremely difficult, 1+ week of work |
| 2 | Impractical, fundamental architecture limitations |
| 1 | Not possible without forking |

### Scoring Rubric: Adding New Hardware (40%)

| Score | Criteria |
|-------|----------|
| 10 | Parameter files only, documented process |
| 9 | Config files + calibration data, <1 day |
| 8 | Config + measurements, 1-3 days |
| 7 | Moderate characterization, 3-7 days |
| 6 | Significant characterization, 1-2 weeks |
| 5 | Major effort, 2-4 weeks, hardware access required |
| 4 | Very difficult, 1-2 months |
| 3 | Requires source modification, months of work |
| 2 | Fundamental redesign needed |
| 1 | Not possible |

### Scoring Rubric: Customization (20%)

| Score | Criteria |
|-------|----------|
| 10 | Modular design, plugin system, comprehensive hooks |
| 9 | Well-documented internals, easy to modify |
| 8 | Clean codebase, reasonable to extend |
| 7 | Understandable code, some effort to modify |
| 6 | Complex but documented, significant effort |
| 5 | Complex, undocumented, reverse engineering needed |
| 4 | Monolithic, very difficult to modify |
| 3 | Obfuscated or unmaintainable code |
| 2 | Closed source, limited customization |
| 1 | Fully closed, no customization possible |

---

## Composite Score Calculation

### Formula

```
Overall Score = (0.40 * Accuracy) + (0.25 * Ease_of_Use) +
                (0.20 * Performance) + (0.15 * Extensibility)
```

### Sub-Score Calculations

**Accuracy:**
```
Accuracy = (0.50 * MAPE_Score) + (0.30 * Correlation_Score) + (0.20 * MaxError_Score)
```

**Ease of Use:**
```
Ease_of_Use = (0.35 * Setup) + (0.30 * Docs) + (0.20 * API) + (0.15 * Errors)
```

**Performance:**
```
Performance = (0.50 * Speed) + (0.30 * Scalability) + (0.20 * Efficiency)
```

**Extensibility:**
```
Extensibility = (0.40 * NewModels) + (0.40 * NewHardware) + (0.20 * Customization)
```

---

## Evaluation Process

### Phase 1: Accuracy Evaluation

1. Run benchmark suite (see benchmark-suite.md)
2. Collect predictions for all applicable workloads
3. Compare against ground truth measurements
4. Compute MAPE, correlation, max error
5. Score according to rubric

### Phase 2: Ease of Use Evaluation

1. Fresh installation from documentation
2. Time to first working example
3. Review documentation completeness
4. Test API with common use cases
5. Trigger and evaluate error handling

### Phase 3: Performance Evaluation

1. Benchmark prediction times (3+ runs)
2. Test with models of increasing size
3. Monitor resource usage during execution
4. Score speed, scalability, efficiency

### Phase 4: Extensibility Evaluation

1. Attempt to add a new model not in examples
2. Review process for adding new hardware
3. Examine codebase structure and modularity
4. Score based on effort and documentation

---

## Reporting Format

### Per-Tool Report

```markdown
## [Tool Name] Evaluation

### Summary
| Dimension | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Accuracy | X.X | 40% | X.X |
| Ease of Use | X.X | 25% | X.X |
| Performance | X.X | 20% | X.X |
| Extensibility | X.X | 15% | X.X |
| **Overall** | | | **X.X** |

### Accuracy Details
- MAPE: X.X% (Score: X)
- Correlation: X.XX (Score: X)
- Max Error: X.X% (Score: X)

### Strengths
- [List key strengths]

### Limitations
- [List key limitations]

### Recommendations
- [Use cases where tool excels]
- [When to consider alternatives]
```

### Comparison Table

| Tool | Accuracy | Ease of Use | Performance | Extensibility | Overall |
|------|----------|-------------|-------------|---------------|---------|
| Tool A | X.X | X.X | X.X | X.X | X.X |
| Tool B | X.X | X.X | X.X | X.X | X.X |
| ... | ... | ... | ... | ... | ... |

---

## Addressing Prior Feedback

This rubric addresses the following gaps identified in previous reviews:

1. **Quantitative synthesis**: MAPE, correlation, and max error provide concrete numbers for comparing accuracy across tools.

2. **Transparent methodology**: All scoring criteria are explicit and reproducible.

3. **Multi-dimensional comparison**: Beyond accuracy, evaluates practical concerns (ease of use, performance, extensibility).

4. **Ground truth establishment**: Clear process for obtaining reference measurements.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-07 | Initial rubric |

---

*Document by Leo | ML Performance Survey Project*
