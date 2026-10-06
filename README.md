![Boxer Banner](banner.png)

# 📦 Boxer

**Boxer** is a lightweight, blazing-fast manager for isolated development environments. Whether you want to quickly test a script, play around with a new library, or create a disposable sandbox without cluttering your system — Boxer has got your back! 

Create isolated sandboxes for Python, Go, and Java in just one click (or one command).

---

## ✨ Features

- 🖥️ **Beautiful GUI & Powerful CLI**: Work the way you want. Use the intuitive desktop app (powered by Flet) or the fast command-line interface.
- 📦 **Instant Sandboxes**: Set up fresh, isolated project folders for **Python**, **Go**, and **Java** in seconds.
- 🐍 **Built-in Python Venv**: Python containers automatically come with their own virtual environments.
- 📥 **GUI Package Manager**: Search and install packages from PyPI directly from the desktop application.
- 🌐 **Multilingual**: Fully localized in English, Ukrainian, German, and Polish (both GUI and CLI).
- 🚀 **Terminal Integration**: Open your containers instantly in your favorite terminal (Kitty, Gnome Terminal, Alacritty, etc.).

---

## 🛠️ Installation & Setup

You can use Boxer as a pre-compiled standalone executable (recommended) or run it directly from the source code.

### Option A: Using the Pre-compiled Release (Linux)
1. Download the latest `Boxer-Linux-x86_64.tar.gz` from the [Releases](#) page.
2. Extract the archive.
3. Run the application:
   ```bash
   ./boxer_app
   ```
4. *(Optional)* To add Boxer to your application menu with the nice squircle icon, copy the included `.desktop` file to your applications folder:
   ```bash
   cp boxer_app.desktop ~/.local/share/applications/
   ```

### Option B: Running from Source
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/boxer.git
   cd boxer
   ```
2. **Create a virtual environment and install dependencies:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Run the GUI:**
   ```bash
   python3 main.py
   ```

---

## 🚀 Usage

### Desktop Application (GUI)
Just launch `./boxer_app` (or `python3 main.py`) and enjoy the intuitive graphical interface!

### Command Line Interface (CLI)
Boxer comes with a powerful CLI. You can use it via the `cli.py` script or the `boxer` bash wrapper.

**Basic commands:**
```bash
# List all containers
./boxer list

# Create a new container
./boxer add my-test-project --lang Python

# Open a container in your file manager
./boxer open my-test-project

# Delete a container (add -r to remove the physical folder)
./boxer rm my-test-project -r
```

### ⚡ CLI Shell Integration
You can seamlessly activate a container's Python environment directly in your current shell:

1. Install the shell integration (adds a small function to your `.bashrc` / `.zshrc`):
   ```bash
   ./boxer setup
   source ~/.bashrc  # or ~/.zshrc
   ```
2. Activate your environment anywhere:
   ```bash
   boxer use my-test-project
   ```

---

## 🌍 Supported Languages

You can change the interface language in the **Settings** tab (GUI). The CLI will automatically adopt the language selected in the GUI.

- 🇬🇧 English
- 🇺🇦 Ukrainian
- 🇩🇪 German
- 🇵🇱 Polish

---

## ☕ Support the Project

Listen, I can do my project for free (as I do now) but... Can you support me on Ko-fi pls? 
If you support me, I can buy a new box of tea!

[![Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/romixcaca)

## 📄 License

This project is open-source and available under the MIT License.
