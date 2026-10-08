#!/usr/bin/env python3
import argparse
import os
import sys
from pathlib import Path

# Додаємо поточну директорію для імпорту utils
sys.path.insert(0, str(Path(__file__).parent))
import utils


def cmd_add(args):
    name = args.name.strip()
    if not name:
        print("❌ Помилка: назва контейнера не може бути порожньою.")
        sys.exit(1)

    if any(c.get("name") == name for c in utils.containers):
        print(f"⚠️  Контейнер із назвою '{name}' вже існує!")
        sys.exit(1)

    lang = args.lang or "Python"
    if lang not in utils.LANGUAGE_TEMPLATES:
        available = ", ".join(utils.LANGUAGE_TEMPLATES.keys())
        print(f"❌ Невідома мова '{lang}'. Доступні: {available}")
        sys.exit(1)

    new_box = utils.add_container(name, lang)
    print(f"✅ Контейнер '{name}' [{lang}] успішно створено!")
    print(f"📁 Шлях: {new_box.get('path')}")


def cmd_list(args):
    containers = utils.load_containers()
    if not containers:
        print("ℹ️  Немає жодного створеного контейнера.")
        return

    print(f"📦 Список контейнерів ({len(containers)}):")
    for idx, c in enumerate(containers, 1):
        name = c.get("name", "unnamed")
        lang = c.get("language", "Unknown")
        path = c.get("path", "")
        venv_mark = " 🐍venv" if path and (Path(path) / ".venv").exists() else ""
        print(f"  {idx}. {name} [{lang}]{venv_mark} -> {path}")


def cmd_remove(args):
    name = args.name.strip()
    if not any(c.get("name") == name for c in utils.containers):
        print(utils.t("cli_not_found", name=name))
        sys.exit(1)

    utils.delete_container(name, remove_files=args.remove_files)
    if args.remove_files:
        print(utils.t("cli_deleted_all", name=name))
    else:
        print(utils.t("cli_deleted_list", name=name))


def cmd_open(args):
    name = args.name.strip()
    box = next((c for c in utils.containers if c.get("name") == name), None)
    if not box:
        print(utils.t("cli_not_found", name=name))
        sys.exit(1)

    path = box.get("path")
    if path and Path(path).exists():
        utils.open_in_folder(path)
        print(utils.t("cli_opened", path=path))
    else:
        print(utils.t("cli_folder_not_found", path=path))


def cmd_use(args):
    """Активує Python-середовище контейнера у поточному терміналі."""
    name = args.name.strip()
    box = next((c for c in utils.containers if c.get("name") == name), None)

    if not box:
        if sys.stdout.isatty():
            print(utils.t("cli_not_found", name=name))
            print(f"   Перевір список: boxer list")
        else:
            print(f"echo '❌ Boxer: контейнер \'{name}\' не знайдено.' >&2; false")
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
            print(f"echo '⚠️  Boxer: у контейнері \'{name}\' немає venv.' >&2; false")
        sys.exit(1)

    if is_win:
        commands = [
            f'. "{venv_activate}"',
            f'Write-Host "🐍 Boxer: активовано Python з контейнера \"{name}\""',
        ]
        setup_cmd = "boxer setup ; . $PROFILE"
        eval_cmd = f'Invoke-Expression (boxer use {name})'
    else:
        commands = [
            f'source "{venv_activate}"',
            f'echo "🐍 Boxer: активовано Python з контейнера \"{name}\""',
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
        print("
".join(commands))



def cmd_setup(args):
    """Встановлює boxer shell-функцію для підтримки 'boxer use' (Bash/Zsh/PowerShell)."""
    boxer_bin = str(Path(__file__).parent / "boxer")
    if getattr(sys, 'frozen', False):
        boxer_bin = str(Path(sys.executable))

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
        function_code = f"""
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
"""
        reload_cmd = ". $PROFILE"
    else:
        shell = os.environ.get("SHELL", "/bin/bash")
        if "zsh" in shell:
            rc_file = Path.home() / ".zshrc"
        else:
            rc_file = Path.home() / ".bashrc"
        
        function_code = f"""
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
"""
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



def main():
    parser = argparse.ArgumentParser(
        prog="boxer",
        description="Boxer CLI — керування контейнерами",
    )
    subparsers = parser.add_subparsers(dest="command", help="Доступні команди")

    # boxer add <name> [--lang Python]
    p_add = subparsers.add_parser("add", help="Створити новий контейнер")
    p_add.add_argument("name", help="Назва нового контейнера")
    p_add.add_argument(
        "--lang",
        default="Python",
        help=(
            "Мова контейнера. Доступні: "
            + ", ".join(utils.LANGUAGE_TEMPLATES.keys())
            + " (за замовчуванням: Python)"
        ),
    )
    p_add.set_defaults(func=cmd_add)

    # boxer list / ls
    p_list = subparsers.add_parser("list", aliases=["ls"], help="Список усіх контейнерів")
    p_list.set_defaults(func=cmd_list)

    # boxer remove / rm
    p_rm = subparsers.add_parser("remove", aliases=["rm"], help="Видалити контейнер")
    p_rm.add_argument("name", help="Назва контейнера для видалення")
    p_rm.add_argument(
        "--remove-files", "-r",
        action="store_true",
        help="Також видалити фізичну папку з файлами контейнера",
    )
    p_rm.set_defaults(func=cmd_remove)

    # boxer open
    p_open = subparsers.add_parser("open", help="Відкрити папку контейнера у файловому менеджері")
    p_open.add_argument("name", help="Назва контейнера")
    p_open.set_defaults(func=cmd_open)

    # boxer use
    p_use = subparsers.add_parser(
        "use",
        help="Перейти до контейнера у поточному терміналі (потребує: boxer setup)",
    )
    p_use.add_argument("name", help="Назва контейнера")
    p_use.set_defaults(func=cmd_use)

    # boxer setup
    p_setup = subparsers.add_parser(
        "setup",
        help="Встановити shell-інтеграцію для команди 'boxer use'",
    )
    p_setup.set_defaults(func=cmd_setup)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
