# Changelog

## [1.1.1] - 2026-10-08 (Mid Update)

### 🌟 What's New
* **Full PowerShell Support (Windows):** `boxer setup` and `boxer use` commands now natively support Windows PowerShell.
  * `boxer setup` automatically locates your `$PROFILE` and integrates Boxer.
  * `boxer use <name>` instantly activates the virtual environment (venv) directly in the current PowerShell terminal using `Invoke-Expression` (matching the Linux experience).

### 🐛 Bug Fixes
* **`flet_desktop` missing on Windows:** Switched the GUI packaging system from bare PyInstaller to the official `flet pack`. This permanently resolves the "No module named 'flet_desktop'" error when launching the `.exe` file.
* **CLI Build Failure:** Fixed a syntax error (unterminated string literal) in the code that was breaking the `boxer.exe` compilation in GitHub Actions.

### ⚙️ Misc
* Project version bumped to `1.1.1`.
