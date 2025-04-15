# 🧾 Chroniq Changelog

All notable changes to this project are tracked here in **Pro Mode**.
Chroniq follows [Semantic Versioning](https://semver.org/) and uses `version.txt` and `CHANGELOG.md` for local tracking.

---

## [0.8.0] - 2025-04-16
### 🚀 Highlights
- ✅ Completed rollback test suite (100% coverage)
- 🧱 Core.py now includes rollback logic cleanly
- 🧪 Verified changelog + version restoration with CLI and unittest

**Added**
- `perform_rollback()` refactored from CLI to `core.py`
- CLI `rollback` command now delegates cleanly to helper
- 5-case `test_rollback.py` with full rollback coverage

---

## [0.7.0] - 2025-04-15
### 🧠 Hyper Audit Mode + Config Awareness

**Added**
- `chroniq audit` with intelligent diagnostics
- `--strict` flag to enforce heading formats
- Config awareness via `.chroniq.toml`
- Profile fallback logic and file path verification

---

## [0.6.0] - 2025-04-14
### 🔧 CLI + Config Setters

**Added**
- `chroniq config set <key> <value> [--profile dev]`
- `chroniq config-show` to display active merged config

**Improved**
- Nested dot notation support
- Type inference (bool/int)
- Profile-aware editing

---

## [0.5.0] - 2025-04-13
### 🛠️ Structured Logging

**Added**
- `chroniq.logger` with:
  - `system_log` (internal)
  - `activity_log` (user-facing)
- Auto-creates `data/logs/`
- Split between critical + activity logs

---

## [0.4.0] - 2025-04-12
### 🧠 Prerelease & Semantic Intelligence

**Features**
- Auto-incrementing prerelease tags: `alpha.1 → alpha.2`
- `SemVer` upgraded with:
  - Robust parsing
  - Strict validation
  - Manual `--pre` override

**Improved**
- Clean fallback logic
- Safe write protection

---

## [0.3.0] - 2025-04-11
### 🧪 Smoke Testing + Preview

**Added**
- `chroniq test --smoke`
- `chroniq changelog-preview` with styled preview
- Init creates version + changelog if missing

---

## [0.2.0] - 2025-04-10
### 📂 Bootstrapping Support

**Added**
- Default config fallback
- Top-level heading detection in CHANGELOG
- Profile awareness in config logic

---

## [0.1.0] - 2025-04-09
### 🎉 Initial Release

**Features**
- `chroniq bump` with patch, minor, major, prerelease
- `version.txt` + `CHANGELOG.md` driven semver
- Pretty CLI output with emoji + `rich`
