# Abliteration notes (high‑level)

## Feasibility on your hardware
- Your RTX 6000 Pro + 2× RTX 6000 Ada are more than sufficient for small‑to‑mid fine‑tunes and weight‑editing workflows.
- The main constraints are the **method**, **data quality**, and **evaluation**, not raw compute.

## What “abliteration” usually means
- A targeted fine‑tune or weight‑editing process that *removes or suppresses* specific behaviors, values, or response styles.
- Often implemented as:
  - LoRA fine‑tuning on counter‑examples.
  - Preference optimization (DPO/ORPO) using curated comparisons.
  - Direct weight edits on specific layers/heads (more experimental).

## Suggested safe path (later)
1. **Define goals precisely**
   - What behaviors are undesirable? Provide concrete examples.
   - What behaviors are desired? Provide concrete examples.
2. **Create a small, high‑quality dataset**
   - Pairs of prompts + preferred responses (and explicitly *rejected* responses if using preference training).
3. **Use a reversible method first**
   - Start with LoRA so changes are easy to rollback.
4. **Evaluate with a fixed test set**
   - Before/after comparisons, including “edge cases.”
5. **Iterate**
   - Add counter‑examples for any regressions.

## Practical risks to watch
- **Over‑correction**: Removing a behavior can damage legitimate reasoning.
- **Bias drift**: A narrow dataset can unintentionally push values to extremes.
- **General capability loss**: Overfitting to a narrow style may reduce helpfulness.

## Where this fits in Kindred2
- If/when you decide to create an “abliteration” stage, it should be a discrete step **after** baseline alignment (your calibration + synthetic Q&A).
- Keep artifacts separated: base model, alignment LoRA, ablation/abliteration LoRA.

## Next steps if you want to proceed later
- I can draft a reproducible pipeline with:
  - dataset schema
  - training config
  - eval harness
  - rollback strategy
