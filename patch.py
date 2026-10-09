import re

with open("cli.py", "r", encoding="utf-8") as f:
    content = f.read()

# Modify cmd_use
new_cmd_use = """def cmd_use(args):
    \"\"\"Активує Python-середовище контейнера у поточному терміналі.\"\"\"
    name = args.name.strip()
    box = next((c for c in utils.containers if c.get("name") == name), None)

    if not box:
        if sys.stdout.isatty():
            print(utils.t("cli_not_found", name=name))
            print(f"   Перевір список: boxer list")
        else:
            print(f"echo '❌ Boxer: контейнер \\'{name}\\' не знайдено.' >&2; false")
        sys.exit(1)

    lang = box.get("language", "Python")
    if lang != "Python":
        msg = f"⚠️  'boxer use' працює лише з Python-контейнерами. '{name}' — це {lang}."
        if sys.stdout.isatty():
            print(msg)
        else:
            print(f"echo '{msg}' >&2; false")
        sys.exit(1)

    path = box.get("path")
    if not path or not Path(path).exists():
        msg = f"⚠️  Папка контейнера не знайдена: {path}"
        if sys.stdout.isatty():
            print(msg)
        else:
            print(f"echo '{msg}' >&2; false")
        sys.exit(1)

    import platform
    is_win = platform.system() == "Windows"
    if is_win:
        venv_activate = Path(path) / ".venv" / "Scripts" / "Activate.ps1"
    else:
        venv_activate = Path(path) / ".venv" / "bin" / "activate"

    if not venv_activate.exists():
        if sys.stdout.isatty():
            print(f"⚠️  У контейнері '{name}' немає venv.")
            print(f"   Створи його:")
            print(f"   python -m venv {path}/.venv")
        else:
            print(f"echo '⚠️  Boxer: у контейнері \\'{name}\\' немає venv.' >&2; false")
        sys.exit(1)

    if is_win:
        commands = [
            f'. "{venv_activate}"',
            f'Write-Host "🐍 Boxer: активовано Python з контейнера \\"{name}\\""',
        ]
        setup_cmd = "boxer setup ; . $PROFILE"
        eval_cmd = f'Invoke-Expression (boxer use {name})'
    else:
        commands = [
            f'source "{venv_activate}"',
            f'echo "🐍 Boxer: активовано Python з контейнера \\"{name}\\""',
        ]
        setup_cmd = "boxer setup && source ~/.bashrc"
        eval_cmd = f'eval "$(boxer use {name})"'

    if sys.stdout.isatty():
        print(f"⚠️  'boxer use' потребує shell-інтеграції для активації середовища.")
        print(f"")
        print(f"   Встанови одним рядком:")
        print(f"   {setup_cmd}")
        print(f"")
        print(f"   Або одразу виконай:")
        print(f'   {eval_cmd}')
    else:
        print("\n".join(commands))
"""

# Modify cmd_setup
new_cmd_setup = """def cmd_setup(args):
    \"\"\"Встановлює boxer shell-функцію для підтримки 'boxer use' (Bash/Zsh/PowerShell).\"\"\"
    boxer_bin = str(Path(__file__).parent / "boxer")
    if getattr(sys, 'frozen', False):
        boxer_bin = str(Path(sys.executable))
    elif "__compiled__" in globals():
        boxer_bin = str(Path(sys.argv[0]).resolve())

    import platform
    is_win = platform.system() == "Windows"
    
    marker = "# >>> boxer shell integration >>>"
    end_marker = "# <<< boxer shell integration <<<"

    if is_win:
        import subprocess
        try:
            res = subprocess.run(["powershell", "-NoProfile", "-Command", "[System.Console]::Write($PROFILE)"], capture_output=True, text=True)
            rc_file = Path(res.stdout.strip())
        except Exception:
            rc_file = Path.home() / "Documents" / "WindowsPowerShell" / "Microsoft.PowerShell_profile.ps1"
        
        rc_file.parent.mkdir(parents=True, exist_ok=True)
        function_code = f\"\"\"
{marker}
function boxer {{
    if ($args.Count -gt 0 -and $args[0] -eq "use") {{
        $out = & "{boxer_bin}" $args
        if ($LASTEXITCODE -eq 0) {{
            Invoke-Expression $out
        }} else {{
            Write-Host $out
        }}
    }} else {{
        & "{boxer_bin}" $args
    }}
}}
{end_marker}
\"\"\"
        reload_cmd = ". $PROFILE"
    else:
        shell = os.environ.get("SHELL", "/bin/bash")
        if "zsh" in shell:
            rc_file = Path.home() / ".zshrc"
        else:
            rc_file = Path.home() / ".bashrc"
        
        function_code = f\"\"\"
{marker}
boxer() {{
    if [ "$1" = "use" ]; then
        local _out _rc
        _out="$("{boxer_bin}" "$@" 2>&1)"
        _rc=$?
        [ $_rc -eq 0 ] && eval "$_out" || {{ echo "$_out" >&2; return $_rc; }}
    else
        "{boxer_bin}" "$@"
    fi
}}
{end_marker}
\"\"\"
        reload_cmd = f"source {rc_file}"

    content = rc_file.read_text(encoding="utf-8") if rc_file.exists() else ""
    if marker in content:
        print(f"✅ Boxer shell-інтеграція вже встановлена у {rc_file}")
        print(f"   Щоб оновити — видали блок між маркерами та запусти знову.")
        return

    with open(rc_file, "a", encoding="utf-8") as f:
        f.write(function_code)

    print(f"✅ Shell-функцію boxer() додано до {rc_file}")
    print(f"")
    print(f"🔄 Активуй зміни:")
    print(f"   {reload_cmd}")
    print(f"")
    print(f"🚀 Тепер команда 'boxer use <назва>' буде активувати .venv у поточному терміналі!")
"""

# Replace cmd_use and cmd_setup using regex
content = re.sub(r'def cmd_use\(args\):.*?(?=\ndef cmd_setup\(args\):)', new_cmd_use + "\n\n", content, flags=re.DOTALL)
content = re.sub(r'def cmd_setup\(args\):.*?(?=\ndef main\(\):)', new_cmd_setup + "\n\n", content, flags=re.DOTALL)

with open("cli.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Patched successfully!")
