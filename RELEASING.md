# Releasing

Publishing uses PyPI **trusted publishing** (OIDC): no API token is stored; the `publish.yml` workflow authenticates from GitHub when a `v*` tag is pushed.

## One-time setup (manual account actions)

1. Create the public GitHub repo and push: `gh repo create markdown-priority-badges --public --source . --push`
2. On PyPI (https://pypi.org/manage/account/publishing/), add a **pending trusted publisher**: project `markdown-priority-badges`, owner `antoinekh`, repo `markdown-priority-badges`, workflow `publish.yml`, environment `pypi`.
3. In the GitHub repo settings, create an environment named `pypi`.

> Replace `antoinekh` above if the repo lives under a different owner.

## Each release

1. Move the `## Unreleased` entries in `CHANGELOG.md` under a new `## x.y.z` heading and bump `version` in `pyproject.toml`.
2. Commit, then tag and push: `git tag vX.Y.Z && git push origin main vX.Y.Z`. The `publish.yml` workflow builds and uploads to PyPI.
