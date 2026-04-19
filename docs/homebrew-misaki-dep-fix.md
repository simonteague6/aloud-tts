# Homebrew: misaki[en] dependency problem

## Problem
`misaki[en]` pulled in `spacy-curated-transformers`, which dragged in `torch` (~2GB,
binary-only wheel). Homebrew formulas require sdists for all resources; `torch` has
none, making the formula unbuildable.

## Investigation
- Bare `misaki` installs only `addict + regex` — the `[en]` extra adds the heavy stack.
- `mlx_audio`'s Kokoro pipeline imports `misaki.en` at load time, so some extras are required.
- `misaki/en.py` imports `spacy` directly but never imports `spacy_curated_transformers`.
- Tested: Kokoro generates audio correctly with `spacy` alone — no torch needed.

## Fix
Replace `misaki[en]` in `pyproject.toml` with the minimal explicit deps actually needed:
`misaki`, `num2words`, `phonemizer-fork`, `espeakng-loader`, `spacy`.

## Remaining binary-only packages (no sdist)
`mlx`, `mlx-metal`, `spacy`, `espeakng-loader` — handled via wheel URLs in the formula.
