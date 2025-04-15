# ✅ Chroniq 0.9.0 TODO

## 🚀 Planned Features

### 🧭 CLI Help Enhancements
- [ ] Add `chroniq help` command (styled, not just alias)
- [ ] Group help output by category: Core, Config, Audit, Versioning
- [ ] Support `chroniq help <command>` for extended descriptions
- [ ] Add fuzzy command detection (`chroniq bum` → suggest `bump`)
- [ ] Rich panel output for help commands (via `rich.panel` or `rich.table`)

### 🧠 Changelog Intelligence
- [ ] Optional preview diffs before changelog removal in rollback
- [ ] Detect unreleased versions not in changelog

### 🔒 Safety + Integrity
- [ ] Automatic backup before each `bump`
- [ ] Validate presence and integrity of `.version.bak`

### 🛠️ Developer Tools
- [ ] `chroniq init --force` to reset everything
- [ ] Start planning `chroniq doctor` diagnostic tool (checks for missing files, logs, config issues)

---
