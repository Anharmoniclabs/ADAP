# Contributing

Changes must preserve the frozen audit trail and clearly distinguish a new
analysis from the completed September 14, 2026 run.

1. Create a branch and document any analytic choice before examining its outcome.
2. Never overwrite frozen tables silently; use a new output name or version.
3. Keep third-party data under `data/` and follow `data/README.md`.
4. Run `make audit` before opening a pull request.
5. If results change, update the receipt, findings, limitations, and report together.

Bug fixes that affect a scientific result should include a short amendment stating
what changed, why it changed, and which outputs were affected.

