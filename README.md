# 🕰️ Chroniq

![License](https://img.shields.io/github/license/yourusername/chroniq?style=flat-square)
![Python Version](https://img.shields.io/badge/python-3.11%2B-blue?style=flat-square)
![Build](https://img.shields.io/badge/tests-passing-brightgreen?style=flat-square)
![Made with ❤️](https://img.shields.io/badge/made%20with-%E2%9D%A4-red?style=flat-square)

> Chroniq is your intelligent, beginner-friendly versioning and changelog assistant. Built with ❤️ for developers who want clean version control without the headache.

---

## ✨ Features

- 🔖 **Semantic Versioning (SemVer)** out of the box (patch, minor, major)
- 📝 **Markdown changelog** management with timestamped entries
- 💬 **Interactive CLI** with rich prompts and emoji feedback
- ⚙️ **Custom config** via `.chroniq.toml` or `.chroniqrc.json`
- 🔧 **Safe version bumping** with optional changelog entry
- ✅ **100% test coverage** — built and tested like a pro

---

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

## 🛠 CLI Commands

| Command               | Description                              |
|----------------------|------------------------------------------|
| `chroniq init`       | Creates `version.txt` and `CHANGELOG.md` |
| `chroniq bump [lvl]` | Bumps version and prompts for changelog  |
| `chroniq version`    | Shows current version                    |
| `chroniq log`        | Displays recent changelog entries        |

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
