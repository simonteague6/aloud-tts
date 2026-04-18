# aloud-tts Release Status

Last updated: 2026-04-18

## Phase 1 — PyPI package ✅ DONE
- [x] `pyproject.toml` updated (name, URLs, classifiers, keywords)
- [x] First successful PyPI publish (v0.1.0 live at https://pypi.org/project/aloud-tts/)

## Phase 2 — GitHub Actions ✅ DONE
- [x] `release.yml` created (tag-triggered: build → pypi-publish → github-release)
- [x] `test.yml` created (PR quality gate: ruff + pytest on macos-14)
- [x] `pypi-publish` job succeeds
- [ ] `bump-formula` job (commented out — waiting for Phase 3)
- [ ] `py2app-bundle` job (commented out — waiting for Phase 5)

## Phase 3 — Homebrew tap
- [ ] Create repo `simonteague6/homebrew-aloud-tts`
- [ ] Generate resource stanzas (`poet aloud-tts`)
- [ ] Write `Formula/aloud-tts.rb`
- [ ] `brew audit --strict --online aloud-tts`
- [ ] Create `HOMEBREW_TAP_TOKEN` PAT (fine-grained, scoped to tap repo) → add as GitHub repo secret
- [ ] Uncomment `bump-formula` job in `release.yml`

## Phase 4 — install.sh
- [x] Written and committed (uv-based, installs uv if missing, auto-downloads Python 3.12)

## Phase 5 — py2app .app bundle
- [x] `setup_app.py` created
- [ ] Build locally: `uv run --with py2app python setup_app.py py2app`
- [ ] Test `dist/TTS.app` on a second Mac or fresh user account
- [ ] Uncomment `py2app-bundle` job in `release.yml`

## Next up: Phase 3 — Homebrew tap
