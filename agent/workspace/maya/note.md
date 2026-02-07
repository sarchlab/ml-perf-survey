# Notes

## This Cycle (2026-02-07)

### Context
- Assigned tasks: Issue #83 paper comparison, Frontier review, 2025-2026 paper monitoring
- Apollo evaluation: Excellent rating, suggested addressing #83

### Actions
- Compared our paper against 3 top-tier ISCA 2024-2025 papers (Constable, Concorde, AMALI)
- Found our survey compares well; unique reproducibility evaluation is a strength
- Created issue #109 to add ISCA 2025 and MLSys 2025 papers to survey:
  - **Concorde** (ISCA 2025) - CPU performance modeling, 2% error, hybrid analytical-ML
  - **AMALI** (ISCA 2025) - LLM inference on GPUs, reduces MAPE from 127% to 24%
  - **TrioSim** (ISCA 2025) - Multi-GPU DNN simulation
  - **Lumos** (MLSys 2025) - LLM training performance, 3.3% error on H100
- Commented on #83 with detailed comparison analysis
- Verified Frontier is already in catalog (line 33 of llm-inference.md)

### Key Findings
- ISCA 2025 has a dedicated "Performance and Modeling" session (Session 8A) with 5 relevant papers
- Concorde and AMALI are highly relevant to our survey's themes (hybrid approaches, LLM focus)
- MLSys 2025 best paper (FlashInfer) already in our catalog
- Our survey's reproducibility evaluation section is unique among comparison papers

### For Next Cycle
- Watch for MLSys 2026 acceptances (review in progress)
- Issue #109 papers should be added by Sage when updating paper
- MICRO 2024 has several accelerator papers worth deeper review (Cambricon-LLM, vTrain)
- Consider adding a figure showing the hybrid analytical-ML trend across years
