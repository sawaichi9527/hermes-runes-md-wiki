# M210 Workspace Seed Verification Relocation

Status: PASS candidate / local validation required
Version line: 0.7.1-dev
Date: 2026-06-08

## Scope

M210 removes milestone verification files from the default runtime workspace Markdown seed.

The `wiki/<workspace slug>/` directory should remain a clean, curated workspace memory skeleton.

Historical milestone verification notes such as `verification-m*.md` are development / release evidence and should live under `dev/wiki-history/<workspace slug>/verification/` instead of the runtime workspace.

## Rationale

`wiki/freelancer/` is only the current demonstration workspace slug on this PC.

The default documented pattern should be `wiki/<workspace slug>/`, not a fixed `freelancer` workspace.

Verification milestone files should not appear as default Markdown memory files under a new workspace seed.

## Expected runtime workspace files

A clean workspace seed should contain files such as:

- `README.md`
- `preferences.md`
- `operating-style.md`
- `local-environment.md`
- `research-sources.md`
- `rss-subscriptions.md`
- `long-term-objectives.md`
- `services.md`
- `decisions.md`
- `forge-inbox/`

It should not include:

- `verification-m*.md`

## Result

Pending local validation / commit.
