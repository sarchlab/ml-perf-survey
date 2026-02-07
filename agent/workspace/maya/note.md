# Notes

## This Cycle (2026-02-07)

### Context
- Primary tasks #114, #117, #118 blocked pending page limit check (#120)
- Sage hasn't completed #120 yet
- Crit completed final review (#113) - paper ready for M9

### Actions
- Scouted for new papers from recently held conferences
- Checked ISCA 2026 - still in review (Round 2 reviews due Feb 13, decisions in March)
- Checked MLSys 2026 - conference in May, papers not yet announced
- Found 7 relevant papers from PPoPP 2026 and CGO 2026 (Sydney, Jan 31 - Feb 4):
  - **Laser** - Layer-level scheduling for multi-SLO LLM serving, 1.67x+ throughput
  - **JanusQuant** - 2-bit KV cache quantization for long-context inference
  - **High-Throughput 3-bit LLM Inference** - Non-uniform quantization
  - **COCCL** - Compression-aware collective communication, 1.24x training throughput
  - **HelixPipe** - Attention parallel pipeline parallelism, 26% speedup on long sequences
  - **CoV** - LLM-based compiler verification chain
  - **Tawa** - Automated warp specialization, 1.1x over cuBLAS
- Created issue #121 to queue PPoPP 2026 and CGO 2026 papers

### Key Findings
- PPoPP 2026 has strong LLM systems content (serving, training, quantization)
- CGO 2026 includes LLM-assisted compilation research
- Both conferences held same week as HPCA 2026 (Sydney)

### Applied Evaluation Feedback
- Added relevance assessment (HIGH/MEDIUM/LOW) to paper proposals per Apollo feedback

### For Next Cycle
- Monitor for ISCA 2026 accepted paper announcements (expected March)
- Tasks #114, #117, #118, #121 all queued pending page budget
