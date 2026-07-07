# Darkly — Agent Guide

**42 School web security wargame** — an answer key / write-up collection. 14 challenges, each in its own directory.

## Structure

Every challenge directory follows:
```
<Challenge Name>/
  flag                   # SHA-256 hash (64 hex chars) — the proof of exploit
  Resources/
    README.md            # Vulnerability explanation & step-by-step exploit walkthrough
    *.png                # Optional exploit screenshots
```

## Reading order

- Start with any challenge's `Resources/README.md` — that is the full write-up.
- The `flag` file is the SHA-256 output of the final exploit step.

## What is here / not here

- **Doc-only repo.** No source code, no Docker, no VM, no scripts, no build system, no tests, no CI.
- Flags are SHA-256 hashes, often derived by MD5-cracking then SHA-256'ing the result.
- The `Brute Force` challenge includes `Resources/wordlist.txt` (63 common passwords).
- `Hidden Content2/` has no README — only a `flag`.

## Key facts

- Root README (`README.md`) is a single-line description — all real docs are in per-challenge `Resources/README.md`.
- No Makefile, package.json, docker-compose, or any config files exist.
- Primary author: Mario Steven Rambeloson (`StevenMario`), with contributions from Iarantsoa Evan Rabesandratana.
- `Stocked XSS/` is the wargame's deliberate misspelling of **Stored XSS** (the README inside uses the correct name).
- Some `Resources/` directories contain `.png` exploit screenshots (not every challenge).
- No existing instruction files (`CLAUDE.md`, `.cursorrules`, `opencode.json`, etc.).
