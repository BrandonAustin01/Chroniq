# 🧾 Changelog

All notable changes to **Chroniq** will be documented in this file.  
This project adheres to [Semantic Versioning](https://semver.org).

---

## 🧪 [0.1.2] — *2025-04-14*

> **Final Pre-Release** — Full test pass & CLI resilience

### ✅ Fixed

- 🧮 **Version parsing** now properly rejects invalid formats like `01.02.03` and `1.2.3\n`
- 🧪 **Unit test coverage** completed — all tests now pass
- 🛠️ **Config fallback tests** reworked using real filesystem mocks
- 🧱 **CLI log test** now captures actual terminal output with rich formatting intact

### 🎯 Enhanced

- 🧪 Combined test runner now runs both **smoke tests** and **unit tests**
- 💬 CLI output cleaned up to better support assertions and logging buffers

---

## 🔧 [0.1.1] — *2025-04-13*

> **Patch Release** — Bugfixes & Unicode compatibility

### ✅ Fixed

- 🧱 **UnicodeEncodeError** crash on Windows terminals using legacy encodings (e.g. `cp1252`)
- 🧠 CLI `Console()` crash due to deprecated `encoding` kwarg (now removed)

### ♻️ Refactored

- 🧩 Re-integrated `supports_unicode()` and `emoji()` utility functions for emoji-safe CLI output
- 🛠️ Rebuilt CLI to be fully compatible with modern and legacy shells

### 🎨 Improved

- 🎛️ Rich styling added across all CLI commands using `rich.Panel`
- 🧪 CLI now consistently renders changelogs and version info with emoji-safe fallback logic

---

## 🚀 [0.1.0] — *2025-04-12*

> **Initial Release** — Functional MVP

### ✨ Added

- 📦 Semantic versioning engine (`SemVer`) with `load`, `bump`, `save`, and `from_string` support
- 🔧 Dual-mode config loader: `.chroniq.toml` (preferred) and `.chroniqrc.json` (fallback)
- 🧾 Auto-initialization of `version.txt` and `CHANGELOG.md` via `chroniq init`
- 💬 Emoji-aware CLI with rich output and prompt-safe fallbacks
- 🧪 CLI tools: `chroniq init`, `bump`, `version`, `log`, `reset`

---
