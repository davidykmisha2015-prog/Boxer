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

## 🛠️ Installation

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

## 🚀 Usage

### Desktop Application (GUI)

To launch the graphical interface, simply run:
```bash
python3 main.py
```

### Command Line Interface (CLI)

Boxer comes with a powerful CLI. You can use it via `cli.py` or the `boxer` bash wrapper.

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

### ⚡ CLI Shell Integration (Boxer Use)

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

## 🌍 Supported Languages

You can change the interface language in the **Settings** tab (GUI). The CLI will automatically adopt the language selected in the GUI.

- 🇬🇧 English
- 🇺🇦 Ukrainian
- 🇩🇪 German
- 🇵🇱 Polish

## ☕ Support the Project

Listen, I can do my project for free (as I do now) but... Can you support me on Ko-fi pls? 
If you support me, I can buy a new box of tea!

[![Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/romixcaca)

## 📄 License

This project is open-source and available under the MIT License.
