import json
import shutil
import subprocess
import sys
from pathlib import Path

# Підтримка PyInstaller (щоб дані зберігалися поруч із exe, а не в тимчасовій папці)
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent

DATA_FILE = BASE_DIR / "containers.json"
SETTINGS_FILE = BASE_DIR / "settings.json"
BOXES_DIR = BASE_DIR / "boxes"
BOXES_DIR.mkdir(parents=True, exist_ok=True)

def load_settings():
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"lang": "uk"}

def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)

SETTINGS = load_settings()

def get_lang():
    return SETTINGS.get("lang", "uk")

def set_lang(lang_code):
    SETTINGS["lang"] = lang_code
    save_settings(SETTINGS)

TRANSLATIONS = {
    "uk": {
        "tab_containers": "Контейнери",
        "tab_help": "Допомога",
        "tab_settings": "Налаштування",
        "btn_create": "Створити",
        "select_container": "Оберіть контейнер зі списку",
        "btn_terminal": "Термінал",
        "btn_packages": "Пакети",
        "btn_folder": "Відкрити папку",
        "btn_delete": "Видалити контейнер",
        "selected": "Обрано: {name} ({lang})",
        "packages_dialog_title": "Управління пакетами (PyPI)",
        "pkg_search_label": "Назва пакету (напр. requests)",
        "pkg_no_desc": "Немає опису",
        "btn_install_pkg": "Встановити пакет",
        "pkg_not_found": "Пакет '{pkg_name}' не знайдено на PyPI.",
        "pkg_installing": "Встановлення {pkg_name}...",
        "pkg_install_success": "✅ Успішно встановлено!",
        "pkg_install_error": "❌ Помилка встановлення.",
        "btn_close": "Закрити",
        "delete_title": "Видалити «{name}»?",
        "delete_desc": "Видалити контейнер тільки зі списку,\nчи також фізичну папку з усіма файлами?",
        "btn_cancel": "Скасувати",
        "btn_list_only": "Тільки зі списку",
        "btn_with_files": "З файлами",
        "empty_list": "Поки немає жодного контейнера. Натисніть «Створити», щоб додати!",
        "container_name": "Назва контейнера",
        "language": "Мова",
        "err_enter_name": "Введи назву",
        "err_duplicate": "Контейнер із такою назвою вже існує",
        "new_container": "Новий контейнер",
        "about_boxer": "Про Boxer",
        "about_desc": "Легкий менеджер ізольованих середовищ для розробки. Створюйте пісочниці для Python, Go та Java в один клік.",
        "support_author": "Support the Author",
        "support_text": "Listen, I can do my project for free(as i do now) but... Can you support me on Ko-fi pls?\nIf you support me, I can buy a new box of tea!",
        "btn_kofi": "Support me on Ko-fi ☕",
        "settings_title": "Налаштування",
        "language_select": "Оберіть мову інтерфейсу",
        "cli_exists": "❌ Помилка: Контейнер '{name}' вже існує.",
        "cli_created": "✅ Успішно створено контейнер '{name}' з шаблоном {lang} у папці:\n   {path}",
        "cli_list_empty": "📭 Немає жодного контейнера.",
        "cli_list_header": "📦 Список контейнерів:",
        "cli_deleted_all": "🗑️  Контейнер '{name}' та його файли успішно видалено.",
        "cli_deleted_list": "🗑️  Контейнер '{name}' видалено зі списку (файли збережено).",
        "cli_not_found": "❌ Контейнер '{name}' не знайдено.",
        "cli_opened": "📂 Відкрито папку контейнера: {path}",
        "cli_folder_not_found": "⚠️  Робоча папка не знайдена: {path}",
    },
    "en": {
        "tab_containers": "Containers",
        "tab_help": "Help",
        "tab_settings": "Settings",
        "btn_create": "Create",
        "select_container": "Select a container from the list",
        "btn_terminal": "Terminal",
        "btn_packages": "Packages",
        "btn_folder": "Open Folder",
        "btn_delete": "Delete Container",
        "selected": "Selected: {name} ({lang})",
        "packages_dialog_title": "Package Manager (PyPI)",
        "pkg_search_label": "Package name (e.g. requests)",
        "pkg_no_desc": "No description",
        "btn_install_pkg": "Install Package",
        "pkg_not_found": "Package '{pkg_name}' not found on PyPI.",
        "pkg_installing": "Installing {pkg_name}...",
        "pkg_install_success": "✅ Successfully installed!",
        "pkg_install_error": "❌ Installation error.",
        "btn_close": "Close",
        "delete_title": "Delete «{name}»?",
        "delete_desc": "Delete the container only from the list,\nor also the physical folder with all files?",
        "btn_cancel": "Cancel",
        "btn_list_only": "List only",
        "btn_with_files": "With files",
        "empty_list": "No containers yet. Click «Create» to add one!",
        "container_name": "Container Name",
        "language": "Language",
        "err_enter_name": "Enter a name",
        "err_duplicate": "A container with this name already exists",
        "new_container": "New Container",
        "about_boxer": "About Boxer",
        "about_desc": "A lightweight manager for isolated development environments. Create sandboxes for Python, Go, and Java in one click.",
        "support_author": "Support the Author",
        "support_text": "Listen, I can do my project for free(as i do now) but... Can you support me on Ko-fi pls?\nIf you support me, I can buy a new box of tea!",
        "btn_kofi": "Support me on Ko-fi ☕",
        "settings_title": "Settings",
        "language_select": "Select interface language",
        "cli_exists": "❌ Error: Container '{name}' already exists.",
        "cli_created": "✅ Successfully created container '{name}' with {lang} template in:\n   {path}",
        "cli_list_empty": "📭 No containers found.",
        "cli_list_header": "📦 Container list:",
        "cli_deleted_all": "🗑️  Container '{name}' and its files were successfully deleted.",
        "cli_deleted_list": "🗑️  Container '{name}' deleted from the list (files kept).",
        "cli_not_found": "❌ Container '{name}' not found.",
        "cli_opened": "📂 Opened container folder: {path}",
        "cli_folder_not_found": "⚠️  Working folder not found: {path}",
    },
    "de": {
        "tab_containers": "Container",
        "tab_help": "Hilfe",
        "tab_settings": "Einstellungen",
        "btn_create": "Erstellen",
        "select_container": "Wählen Sie einen Container",
        "btn_terminal": "Terminal",
        "btn_packages": "Pakete",
        "btn_folder": "Ordner öffnen",
        "btn_delete": "Container löschen",
        "selected": "Ausgewählt: {name} ({lang})",
        "packages_dialog_title": "Paketmanager (PyPI)",
        "pkg_search_label": "Paketname (z.B. requests)",
        "pkg_no_desc": "Keine Beschreibung",
        "btn_install_pkg": "Paket installieren",
        "pkg_not_found": "Paket '{pkg_name}' nicht auf PyPI gefunden.",
        "pkg_installing": "Installiere {pkg_name}...",
        "pkg_install_success": "✅ Erfolgreich installiert!",
        "pkg_install_error": "❌ Installationsfehler.",
        "btn_close": "Schließen",
        "delete_title": "«{name}» löschen?",
        "delete_desc": "Container nur aus der Liste löschen\noder auch den physischen Ordner mit allen Dateien?",
        "btn_cancel": "Abbrechen",
        "btn_list_only": "Nur Liste",
        "btn_with_files": "Mit Dateien",
        "empty_list": "Noch keine Container. Klicken Sie auf «Erstellen»!",
        "container_name": "Containername",
        "language": "Sprache",
        "err_enter_name": "Name eingeben",
        "err_duplicate": "Ein Container mit diesem Namen existiert bereits",
        "new_container": "Neuer Container",
        "about_boxer": "Über Boxer",
        "about_desc": "Ein leichtgewichtiger Manager für isolierte Entwicklungsumgebungen. Erstellen Sie Sandboxes für Python, Go und Java mit einem Klick.",
        "support_author": "Support the Author",
        "support_text": "Listen, I can do my project for free(as i do now) but... Can you support me on Ko-fi pls?\nIf you support me, I can buy a new box of tea!",
        "btn_kofi": "Support me on Ko-fi ☕",
        "settings_title": "Einstellungen",
        "language_select": "Sprache auswählen",
        "cli_exists": "❌ Fehler: Container '{name}' existiert bereits.",
        "cli_created": "✅ Container '{name}' mit {lang} Vorlage erfolgreich erstellt in:\n   {path}",
        "cli_list_empty": "📭 Keine Container gefunden.",
        "cli_list_header": "📦 Containerliste:",
        "cli_deleted_all": "🗑️  Container '{name}' und seine Dateien erfolgreich gelöscht.",
        "cli_deleted_list": "🗑️  Container '{name}' aus Liste gelöscht (Dateien behalten).",
        "cli_not_found": "❌ Container '{name}' nicht gefunden.",
        "cli_opened": "📂 Containerordner geöffnet: {path}",
        "cli_folder_not_found": "⚠️  Arbeitsordner nicht gefunden: {path}",
    },
    "pl": {
        "tab_containers": "Kontenery",
        "tab_help": "Pomoc",
        "tab_settings": "Ustawienia",
        "btn_create": "Utwórz",
        "select_container": "Wybierz kontener z listy",
        "btn_terminal": "Terminal",
        "btn_packages": "Pakiety",
        "btn_folder": "Otwórz folder",
        "btn_delete": "Usuń kontener",
        "selected": "Wybrano: {name} ({lang})",
        "packages_dialog_title": "Menedżer pakietów (PyPI)",
        "pkg_search_label": "Nazwa pakietu (np. requests)",
        "pkg_no_desc": "Brak opisu",
        "btn_install_pkg": "Zainstaluj pakiet",
        "pkg_not_found": "Pakiet '{pkg_name}' nie znaleziony w PyPI.",
        "pkg_installing": "Instalowanie {pkg_name}...",
        "pkg_install_success": "✅ Pomyślnie zainstalowano!",
        "pkg_install_error": "❌ Błąd instalacji.",
        "btn_close": "Zamknij",
        "delete_title": "Usunąć «{name}»?",
        "delete_desc": "Usunąć kontener tylko z listy,\nczy także fizyczny folder ze wszystkimi plikami?",
        "btn_cancel": "Anuluj",
        "btn_list_only": "Tylko z listy",
        "btn_with_files": "Z plikami",
        "empty_list": "Brak kontenerów. Kliknij «Utwórz», aby dodać!",
        "container_name": "Nazwa kontenera",
        "language": "Język",
        "err_enter_name": "Wprowadź nazwę",
        "err_duplicate": "Kontener o tej nazwie już istnieje",
        "new_container": "Nowy kontener",
        "about_boxer": "O Boxer",
        "about_desc": "Lekki menedżer izolowanych środowisk programistycznych. Twórz piaskownice dla Python, Go i Java jednym kliknięciem.",
        "support_author": "Support the Author",
        "support_text": "Listen, I can do my project for free(as i do now) but... Can you support me on Ko-fi pls?\nIf you support me, I can buy a new box of tea!",
        "btn_kofi": "Support me on Ko-fi ☕",
        "settings_title": "Ustawienia",
        "language_select": "Wybierz język interfejsu",
        "cli_exists": "❌ Błąd: Kontener '{name}' już istnieje.",
        "cli_created": "✅ Pomyślnie utworzono kontener '{name}' z szablonem {lang} w:\n   {path}",
        "cli_list_empty": "📭 Nie znaleziono kontenerów.",
        "cli_list_header": "📦 Lista kontenerów:",
        "cli_deleted_all": "🗑️  Kontener '{name}' i jego pliki zostały pomyślnie usunięte.",
        "cli_deleted_list": "🗑️  Kontener '{name}' usunięty z listy (pliki zachowane).",
        "cli_not_found": "❌ Nie znaleziono kontenera '{name}'.",
        "cli_opened": "📂 Otwarto folder kontenera: {path}",
        "cli_folder_not_found": "⚠️  Nie znaleziono folderu roboczego: {path}",
    }
}

def t(key, **kwargs):
    lang = get_lang()
    text = TRANSLATIONS.get(lang, TRANSLATIONS["uk"]).get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text

# Шаблони для різних мов програмування
LANGUAGE_TEMPLATES: dict[str, tuple[str, str]] = {
    "Python": ("main.py",   '# Boxer Container: {name}\nprint("Привіт із контейнера {name}!")\n'),
    "Go":     ("main.go",   'package main\n\nimport "fmt"\n\nfunc main() {{\n    fmt.Println("Привіт із контейнера {name}!")\n}}\n'),
    "Java":   ("Main.java", 'public class Main {{\n    public static void main(String[] args) {{\n        System.out.println("Привіт із контейнера {name}!");\n    }}\n}}\n'),
}

def load_containers() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                return []
            updated = False
            for item in data:
                if "path" not in item:
                    box_path = BOXES_DIR / item.get("name", "unnamed")
                    box_path.mkdir(parents=True, exist_ok=True)
                    item["path"] = str(box_path)
                    updated = True
            if updated:
                save_containers(data)
            return data
    except (json.JSONDecodeError, OSError):
        return []

def save_containers(data: list[dict] = None) -> None:
    global containers
    if data is not None:
        containers = data
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(containers, f, ensure_ascii=False, indent=4)

containers = load_containers()

def add_container(name: str, language: str) -> dict:
    box_path = BOXES_DIR / name
    box_path.mkdir(parents=True, exist_ok=True)
    if language in LANGUAGE_TEMPLATES:
        filename, template = LANGUAGE_TEMPLATES[language]
        starter_file = box_path / filename
        if not starter_file.exists():
            content = template.format(name=name)
            starter_file.write_text(content, encoding="utf-8")
    if language == "Python":
        venv_path = box_path / ".venv"
        if not venv_path.exists():
            python_exe = sys.executable if Path(sys.executable).exists() else "python3"
            subprocess.run([python_exe, "-m", "venv", str(venv_path)], check=True)
    elif language == "Go":
        mod_file = box_path / "go.mod"
        if not mod_file.exists():
            try:
                subprocess.run(["go", "mod", "init", name], cwd=str(box_path), capture_output=True)
            except FileNotFoundError:
                pass # Якщо Go не встановлено, просто ігноруємо
    item = {"name": name, "language": language, "path": str(box_path)}
    containers.append(item)
    save_containers()
    return item

def delete_container(name: str, remove_files: bool = False) -> bool:
    global containers
    if remove_files:
        box = next((c for c in containers if c.get("name") == name), None)
        if box:
            path = box.get("path")
            if path and Path(path).exists():
                shutil.rmtree(path)
    containers = [c for c in containers if c.get("name") != name]
    save_containers()
    return True

def open_in_terminal(directory: str | Path) -> bool:
    dir_path = str(Path(directory).resolve())
    sys_name = platform.system()
    
    if sys_name == "Windows":
        try:
            import os
            os.system(f'start cmd /k "cd /d {dir_path}"')
            return True
        except Exception:
            return False
    elif sys_name == "Darwin":
        try:
            subprocess.Popen(["open", "-a", "Terminal", dir_path])
            return True
        except Exception:
            return False

    terminals = [
        ["kitty", "--directory", dir_path],
        ["gnome-terminal", "--working-directory", dir_path],
        ["ptyxis", "--working-directory", dir_path],
        ["konsole", "--workdir", dir_path],
        ["alacritty", "--working-directory", dir_path],
        ["xfce4-terminal", "--working-directory", dir_path],
        ["x-terminal-emulator", "--working-directory", dir_path],
        ["xterm", "-e", f"cd '{dir_path}' && bash"],
    ]
    for cmd in terminals:
        if shutil.which(cmd[0]):
            try:
                subprocess.Popen(cmd)
                return True
            except OSError:
                continue
    return False

import platform
def open_in_folder(directory: str | Path) -> bool:
    dir_path = str(Path(directory).resolve())
    sys_name = platform.system()
    try:
        if sys_name == "Windows":
            import os
            os.startfile(dir_path)
            return True
        elif sys_name == "Darwin":
            subprocess.Popen(["open", dir_path])
            return True
        else:
            if shutil.which("xdg-open"):
                subprocess.Popen(["xdg-open", dir_path])
                return True
    except Exception:
        pass
    return False
