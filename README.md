# 🔮 Chroniq — Smart Versioning & Changelog CLI

<!-- Core Info -->
![PyPI](https://img.shields.io/pypi/v/chroniq?label=PyPI&logo=pypi&logoColor=white&style=for-the-badge)
![Python](https://img.shields.io/pypi/pyversions/chroniq?label=Python&logo=python&logoColor=white&style=for-the-badge)
![License](https://img.shields.io/github/license/BrandonAustin01/chroniq?style=for-the-badge&logo=open-source-initiative&logoColor=white)
![Downloads](https://img.shields.io/pypi/dm/chroniq?label=Downloads&logo=download&style=for-the-badge)

<!-- Dev & Stability -->
![Build](https://img.shields.io/badge/build-passing-brightgreen?style=for-the-badge&logo=githubactions&logoColor=white)
![Tests](https://img.shields.io/badge/tests-100%25%20passing-success?style=for-the-badge&logo=pytest&logoColor=white)
![Stability](https://img.shields.io/badge/stability-stable-blue?style=for-the-badge)

<!-- Vibes -->
![Made With](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red?style=for-the-badge)
![Chroniq Vibe](https://img.shields.io/badge/dev-first-black?style=for-the-badge)


**Chroniq** is a privacy-first, developer-friendly CLI tool for managing your project's semantic versions and changelogs.  
Built with offline-first principles and human-readable feedback, it keeps your versioning accurate and your history clear.

> _"Because versioning shouldn't feel like a chore."_ 💡

---

## 🚀 Features

- 📌 Semantic versioning with `MAJOR.MINOR.PATCH[-PRERELEASE]`
- 🔁 Safe changelog entries with interactive prompts
- 📦 Pre-release support via `--pre` (e.g. `alpha.1`, `beta`, `rc.2`)
- 🧪 Full test suite with smoke + unit tests
- 🧠 Human-friendly output using `rich`
- ⚙️ Configurable defaults via `.chroniq.toml` or `.chroniqrc.json`
- 🔐 No tracking, no remote APIs — runs fully offline

---

## 🧰 Commands

| Command                | Description                                                  |
|------------------------|--------------------------------------------------------------|
| `chroniq init`         | Initialize `version.txt` and `CHANGELOG.md`                 |
| `chroniq bump [level]` | Bump version by patch, minor, or major                      |
| `chroniq bump --pre`   | Bump pre-release (e.g. `alpha.1 → alpha.2`)                |
| `chroniq log`          | Show recent entries from the changelog                     |
| `chroniq version`      | Show current version                                       |
| `chroniq reset`        | Delete version + changelog files (use with caution)        |

---

## ✏️ Examples

```bash
chroniq bump patch             # Bumps 1.0.0 → 1.0.1
chroniq bump minor             # Bumps 1.0.1 → 1.1.0
chroniq bump major             # Bumps 1.1.0 → 2.0.0
chroniq bump --pre alpha       # Sets pre-release to 2.0.0-alpha.1
chroniq bump --pre beta        # Sets pre-release to 2.0.0-beta.1
chroniq bump --pre rc          # Sets pre-release to 2.0.0-rc.1

## 🚀 Quickstart

```bash
# Install
pip install chroniq  # or: poetry add chroniq

# Initialize changelog and version
chroniq init

# Bump a version (patch/minor/major)
chroniq bump minor

# View the current version
chroniq version

# See latest changelog entries
chroniq log --lines 5
```

---

## ⚙️ Config Options

Create a `.chroniq.toml` in your project root:

```toml
[settings]
default_bump = "patch"
silent = false
```

Or use `.chroniqrc.json`:
```json
{
  "default_bump": "minor",
  "silent": true
}
```

---

## 🧪 Run Tests

```bash
pytest -v
```
```bash
python run_local_tests.py
```

---

## 📦 Packaging & Publishing

```bash
# Build the distribution
poetry build

# Publish (optional)
poetry publish --build
```

---

## 🤝 Contributing
PRs welcome! Please keep it clean, modular, and covered by tests.

---

## 📄 License

[MIT](LICENSE) © Brandon McKinney
