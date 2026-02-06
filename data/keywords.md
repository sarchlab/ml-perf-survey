# Search Keywords for ML Performance Models Survey

This document defines the search keywords and strategies for systematic literature discovery.

---

## 1. Primary Keywords

Core terms that directly describe our survey topic.

| Keyword | Rationale |
|---------|-----------|
| neural network performance model | General term for DNN performance prediction |
| DNN performance prediction | Direct match for our survey focus |
| deep learning performance model | Alternative phrasing |
| machine learning latency prediction | Common prediction target |
| inference performance model | Distinguishes from training |
| DNN simulator | Captures simulation-based approaches |
| neural network simulator | Alternative phrasing |
| ML workload characterization | Related to performance understanding |

---

## 2. Modeling Approach Keywords

Terms specific to each modeling methodology.

### Analytical Models
- roofline model neural network
- analytical performance model DNN
- compute bound memory bound deep learning
- operational intensity neural network

### Simulation-Based
- cycle-accurate DNN simulation
- GPU simulator deep learning
- accelerator simulator neural network
- hardware simulation machine learning
- trace-driven simulation DNN

### ML-Based Models
- learned performance model
- neural network cost model
- performance prediction machine learning
- surrogate model DNN
- regression model latency prediction

### Hybrid Approaches
- hybrid performance model deep learning
- analytical ML performance model
- calibrated performance model

---

## 3. Hardware-Specific Keywords

Terms targeting specific hardware platforms.

| Platform | Keywords |
|----------|----------|
| **GPU** | GPU performance model, CUDA kernel performance, cuDNN performance, tensor core performance |
| **TPU** | TPU performance model, TPU inference latency, XLA performance |
| **NPU/Accelerators** | DNN accelerator performance, systolic array performance, custom accelerator modeling, Eyeriss, Simba |
| **Multi-Device** | distributed training performance, multi-GPU scaling, pipeline parallelism performance |
| **FPGA** | FPGA neural network performance, HLS performance model |

---

## 4. Workload-Specific Keywords

Terms for specific ML model types.

| Workload | Keywords |
|----------|----------|
| **CNN** | convolutional neural network performance, CNN inference latency, image model performance |
| **Transformer** | transformer performance model, attention mechanism latency, LLM inference performance, BERT performance, GPT latency |
| **RNN/LSTM** | recurrent neural network performance, LSTM latency model |
| **GNN** | graph neural network performance, GNN inference latency |
| **Operators** | GEMM performance model, convolution performance, matrix multiplication latency |

---

## 5. Boolean Search Combinations

Ready-to-use queries for academic search engines.

### Google Scholar / ACM DL / IEEE Xplore

```
("performance model" OR "performance prediction" OR "latency prediction")
AND ("neural network" OR "deep learning" OR "DNN" OR "machine learning")
```

```
("simulator" OR "simulation")
AND ("neural network" OR "DNN" OR "deep learning" OR "accelerator")
```

```
("roofline" OR "analytical model")
AND ("neural network" OR "deep learning" OR "CNN" OR "transformer")
```

```
("cost model" OR "learned cost model" OR "surrogate model")
AND ("compiler" OR "autotuning" OR "optimization")
AND ("neural network" OR "DNN")
```

### arXiv-Specific

```
cat:cs.LG AND (performance model OR latency prediction)
```

```
cat:cs.AR AND (DNN OR neural network) AND (performance OR latency)
```

```
cat:cs.PF AND (deep learning OR neural network)
```

---

## 6. Venue-Specific Search Strategies

### Architecture Venues (MICRO, ISCA, HPCA, ASPLOS)
Focus on:
- Accelerator design papers (often include performance models)
- Simulation infrastructure papers
- Workload characterization studies
- Memory system optimization for DNNs

Suggested queries:
```
site:dl.acm.org "MICRO" ("DNN" OR "neural network") ("performance" OR "latency" OR "simulator")
```

### ML Systems Venues (MLSys, OSDI, SOSP)
Focus on:
- Compiler cost models (TVM, XLA, Halide)
- AutoML and NAS performance predictors
- Distributed training performance models

Suggested queries:
```
site:proceedings.mlsys.org "performance model" OR "cost model" OR "latency prediction"
```

### ML Venues (NeurIPS, ICML, ICLR)
Focus on:
- Hardware-aware neural architecture search
- Efficient inference techniques with performance analysis
- Learned index structures and performance

Suggested queries:
```
site:papers.nips.cc "hardware-aware" AND ("performance" OR "latency")
```

---

## 7. Seminal Papers (Pre-2020)

Key foundational works to include regardless of date:

| Paper/System | Year | Relevance |
|--------------|------|-----------|
| Roofline Model | 2009 | Foundational analytical model |
| Timeloop/Accelergy | 2019 | Influential accelerator modeling |
| MAESTRO | 2019 | DNN dataflow cost model |
| Halide autoscheduler | 2019 | Learned cost model for scheduling |
| nn-Meter | 2021 | Reference for learned latency prediction |

---

## 8. Exclusion Criteria

Avoid papers that are:
- Pure algorithmic improvements without performance modeling
- Training-only focus (unless transferable to inference)
- Application papers without generalizable performance insights
- Benchmark suites without modeling components

---

## Usage Notes

1. Start with broad primary keywords, then narrow by venue
2. For each venue search, scan first 100 results by relevance
3. Use citation tracking (both forward and backward) for key papers
4. Flag preprints and check for published versions
5. Prioritize papers with reproducible artifacts
