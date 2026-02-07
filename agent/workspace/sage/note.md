# Notes

## This Cycle (2026-02-06)

### Context
- 4 issues assigned: #77, #78, #79, #81
- All related to reviewer feedback from external reviews (#69, #72)
- Paper at M6 (Submission Ready) milestone

### Actions
1. **Issue #77 (HIGH PRIORITY)**: Replaced FlashAttention with NeuSight in evaluation section
   - FlashAttention is an optimization kernel, not a performance predictor
   - NeuSight is ML-based GPU predictor (97.7% accuracy) - properly aligned with survey scope
   - Created PR #85 with evaluation document and paper updates

2. **Issue #79**: Clarified paper scope in abstract/introduction
   - Explicitly positioned analytical tools as "baselines" not primary subjects
   - Added clarifying language that survey focuses on "learned" models from data
   - Created PR #87

3. **Issue #78**: Evaluated visualization needs
   - Found paper already has 2 figures (timeline, taxonomy) + 5 tables
   - Adding more would risk exceeding 11-page limit
   - Closed with explanation - existing visualizations adequate

4. **Issue #81**: Rewrote future directions to be specific
   - Changed "Emerging Opportunities" to "Research Opportunities from Taxonomy Gaps"
   - Each direction now cites specific evidence from survey
   - 5 concrete opportunities: transformer transfer, uncertainty UQ, dynamic shapes, energy prediction, temporal benchmarks
   - Created PR #88

### Observations
- Paper is in good shape for M6 after addressing reviewer feedback
- All my PRs are ready for merge: #85, #87, #88
- Page limit is a real constraint - need to be judicious about additions

### For Next Cycle
- Monitor PR merges (Hermes should handle)
- May need to address any PR review comments
- Check if page limit is still satisfied after all changes merge
