# 📜 Changelog  

_All notable changes to this project will be documented here._  
> “Chroniq doesn’t track time. It defines it.” ⏳

---

## [0.9.0] - 2025-04-19  

🧰 **Developer Config Toolkit** (Codename: `Config Mastery`)  

- Introduced `chroniq config set`, `get`, `list`, and `delete` with full profile support  
- ✅ Config changes persist across CLI invocations using `.chroniq.toml`  
- 🔐 Config loader now returns `(merged_config, active_profile)` safely  
- 🛡️ Fully passed config fallback, merge, deletion, and overwrite tests  
- ✨ `chroniq audit` now uses Hyper Audit Mode with professional diagnostics  
- 🔍 Added `--strict` flag and `.chroniq.toml` fallback enforcement  
- 📂 Added `log_dir`, `version_file`, and `changelog_file` path support in config  
- 🧪 All 19 tests passing — system stable  

> _"Chroniq no longer reads your config… it understands it."_

---

## [0.8.0] - 2025-04-16  

🪪 **Identity Phase**  

- 🧪 Introduced `chroniq audit` command for version/changelog diagnostics  
- 🎛️ Added `.chroniq.toml` as a persistent user config store  
- 🧱 Defined internal `DEFAULT_CONFIG` for safe fallbacks  
- 🎯 Audit system supports changelog version matching and SemVer parsing  

> _"Chroniq has eyes now. It sees your structure."_ 👁️ 👄 👁️

---

## [0.7.0] - 2025-04-15  

🔄 **Rollback Ready**  

- ⏪ Added `chroniq rollback` to revert version.txt and changelog safely  
- 🧹 Removes latest changelog entry and restores `.version.bak`  
- 🧪 Multiple rollback scenarios tested (missing changelog, version-only, etc.)  
- 🛡️ Introduced resilience checks for corrupted or missing backups  

> _"Time is a loop. Rewind it anytime."_ 🔁

---

## [0.6.0] - 2025-04-14  

🎙️ **Prompt Intelligence**  

- 🧠 Added `chroniq prompt` (planned) to interactively build changelog entries  
- 📝 Smart formatting rules for changelog consistency  
- 🔍 Internally refactored version bumpers with better logging and detection  

> _"Chroniq doesn’t just bump versions. It tells you why."_ ✍️

---

## [0.5.0] - 2025-04-13  

🔖 **SemVer Supreme**  

- 🧪 Introduced prerelease bumping: `alpha`, `beta`, `rc` support  
- 1.2.3 → 1.2.3-alpha.1 → 1.2.3-alpha.2 …  
- 🧠 `SemVer` class supports `.from_string()` and `.bump_prerelease()`  
- ⛔ Invalid bump attempts now raise clear exceptions  

> _"Chroniq’s versions now have moods."_ 😤😎😱

---

## [0.4.0] - 2025-04-12  

🧱 **Project Reset Protocol**  

- 🧹 `chroniq reset` cleans up version + changelog for fresh starts  
- 🛠️ Introduced `--version` and `--dev` flags for CLI entrypoint  
- 📊 Modular logger integration: system and activity logs separated  
- 🧪 Initial test suite scaffolded and partially automated  

> _"Sometimes, to build forward, you reset backward."_ 🧼

---

## [0.3.0] - 2025-04-11  

📓 **Changelog Genesis**  

- ✍️ Automatic changelog writing after each bump  
- 🧠 Changelog prompts support one-line and multi-line entries  
- 🧾 Customizable entry templates planned  

> _"Chroniq remembers. Even when you forget."_ 📝

---

## [0.2.0] - 2025-04-10  

⚙️ **Bump Protocols**  

- 🚀 Introduced `bump patch`, `bump minor`, and `bump major`  
- 🛠️ `version.txt` updated with SemVer compliance  
- 🧪 Internal version handling powered by `SemVer` class  

> _"Chroniq starts keeping score."_ 📈

---

## [0.1.0] - 2025-04-08  

🌱 **Initial Release: The Spark**  

- ✨ Bootstrapped Chroniq CLI  
- 📂 Creates `version.txt` and `CHANGELOG.md` on `init`  
- 🧠 Designed to be modular, local-first, and changelog-aware  

> _"It begins with a single version."_ 💡
