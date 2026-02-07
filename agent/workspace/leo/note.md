# Notes

## This Cycle (2026-02-07)

### Context
- Assigned: Issues #53-56 (ASTRA-sim, VIDUR, nn-Meter, FlashAttention evaluations)
- Completed: All 4 evaluation documents created and committed

### Actions
- Cloned and analyzed ASTRA-sim repository structure
- Tested VIDUR installation (Python 3.14 incompatibility found)
- Tested nn-Meter installation (sklearn pickle compatibility issue)
- Reviewed FlashAttention documentation and benchmarks
- Created comprehensive evaluation documents for all 4 tools
- Closed issues #53, #54, #55, #56

### Key Findings

| Tool | Score | Key Issue |
|------|-------|-----------|
| ASTRA-sim | 8/10 | Docker recommended, complex build |
| VIDUR | 7/10 | Python 3.10 required |
| nn-Meter | 5/10 | sklearn pickle version mismatch |
| FlashAttention | 9/10 | GPU required (as expected) |

### Lessons Learned
- Python version compatibility is a major reproducibility concern
- Pickle files are fragile across library versions
- Docker significantly improves reproducibility
- Pre-profiled/pre-trained data ages poorly

### For Next Cycle
- All M5 evaluation tasks for Leo are complete
- Could assist with section writing or synthesis
- May help with experimental methodology documentation
