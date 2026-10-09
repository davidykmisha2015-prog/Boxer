import flet as ft
import utils
import urllib.request
import json
import subprocess
import threading
from pathlib import Path

ACCENT = "#6C72FF"
BG = "#17171C"
BORDER = "#4A4D8F"
CARD_BG = "#1E1E26"
CARD_SELECTED = "#262738"


def main(page: ft.Page):
    page.title = "Boxer"
    page.bgcolor = BG
    page.padding = 0
    page.theme_mode = ft.ThemeMode.DARK

    selected_container = None

    # Верхня фіолетова панель
    header = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.ALL_INBOX, color="white", size=28),
                ft.Text("Boxer", size=32, weight=ft.FontWeight.BOLD, color="white"),
            ],
            spacing=12,
        ),
        bgcolor=ACCENT,
        padding=ft.Padding.symmetric(horizontal=20, vertical=15),
        width=float("inf"),
    )

    # Вкладки
    btn_containers = ft.TextButton(utils.t("tab_containers"), icon=ft.Icons.INVENTORY_2, style=ft.ButtonStyle(color=ACCENT))
    btn_help = ft.TextButton(utils.t("tab_help"), icon=ft.Icons.HELP_OUTLINE, style=ft.ButtonStyle(color=ft.Colors.GREY_400))
    btn_settings = ft.TextButton(utils.t("tab_settings"), icon=ft.Icons.SETTINGS, style=ft.ButtonStyle(color=ft.Colors.GREY_400))
    tabs = ft.Row([btn_containers, btn_help, btn_settings])

    # Кнопка створення
    create_btn = ft.FilledButton(
        utils.t("btn_create"),
        icon=ft.Icons.ADD,
        style=ft.ButtonStyle(bgcolor=ACCENT, color="white"),
    )

    top_row = ft.Row(
        [tabs, create_btn],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # Список контейнерів
    containers_list = ft.ListView(expand=True, spacing=10)

    # Нижня панель дій для вибраного контейнера
    selected_info = ft.Text(
        utils.t("select_container"),
        color=ft.Colors.GREY_500,
        size=13,
    )
    terminal_btn = ft.FilledButton(
        utils.t("btn_terminal"),
        icon=ft.Icons.TERMINAL,
        style=ft.ButtonStyle(bgcolor="#2D2D3A", color="white"),
        visible=False,
    )
    packages_btn = ft.FilledButton(
        utils.t("btn_packages"),
        icon=ft.Icons.EXTENSION,
        style=ft.ButtonStyle(bgcolor="#4CAF50", color="white"),
        visible=False,
    )
    folder_btn = ft.FilledButton(
        utils.t("btn_folder"),
        icon=ft.Icons.FOLDER_OPEN,
        style=ft.ButtonStyle(bgcolor=ACCENT, color="white"),
        visible=False,
    )
    delete_btn = ft.IconButton(
        icon=ft.Icons.DELETE_OUTLINE,
        icon_color=ft.Colors.RED_400,
        tooltip=utils.t("btn_delete"),
        visible=False,
    )

    action_bar = ft.Container(
        content=ft.Row(
            [
                ft.Row([selected_info], expand=True),
                ft.Row([packages_btn, terminal_btn, folder_btn, delete_btn], spacing=8),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor="#1E1E26",
        padding=ft.Padding.symmetric(horizontal=15, vertical=10),
        border_radius=8,
        border=ft.Border.all(1, BORDER),
    )

    def update_action_bar():
        nonlocal selected_container
        if selected_container:
            name = selected_container.get("name", "")
            lang = selected_container.get("language", "")
            path = selected_container.get("path", "")
            selected_info.value = utils.t("selected", name=name, lang=lang)
            selected_info.color = "white"
            selected_info.weight = ft.FontWeight.BOLD

            terminal_btn.visible = True
            terminal_btn.on_click = lambda e, p=path: utils.open_in_terminal(p)
            
            if lang == "Python":
                packages_btn.visible = True
                packages_btn.on_click = lambda e, p=path: open_packages_dialog(p)
            else:
                packages_btn.visible = False


            folder_btn.visible = True
            folder_btn.on_click = lambda e, p=path: utils.open_in_folder(p)

            delete_btn.visible = True
            delete_btn.on_click = lambda e, n=name: on_delete_container(n)
        else:
            selected_info.value = utils.t("select_container")
            selected_info.color = ft.Colors.GREY_500
            selected_info.weight = ft.FontWeight.NORMAL
            packages_btn.visible = False
            terminal_btn.visible = False
            folder_btn.visible = False
            delete_btn.visible = False

    # === Package Manager ===
    def open_packages_dialog(path):
        pkg_search_input = ft.TextField(label=utils.t("pkg_search_label"), expand=True, on_submit=lambda e: search_pkg())
        pkg_info_col = ft.Column(visible=False, spacing=10)
        pkg_log_output = ft.ListView(height=100, auto_scroll=True, visible=False)
        current_pkg_name = ""
        
        def search_pkg():
            pkg_name = pkg_search_input.value.strip()
            if not pkg_name: return
            
            pkg_info_col.visible = False
            pkg_log_output.visible = False
            page.update()
            
            try:
                url = f"https://pypi.org/pypi/{pkg_name}/json"
                req = urllib.request.Request(url, headers={'User-Agent': 'Boxer'})
                with urllib.request.urlopen(req) as response:
                    data = json.loads(response.read().decode())
                    info = data.get("info", {})
                    
                    nonlocal current_pkg_name
                    current_pkg_name = info.get("name", pkg_name)
                    
                    pkg_info_col.controls = [
                        ft.Text(f"{info.get('name')} (v{info.get('version')})", weight=ft.FontWeight.BOLD, size=16),
                        ft.Text(info.get("summary", utils.t("pkg_no_desc")), color=ft.Colors.GREY_400, italic=True),
                        ft.FilledButton(utils.t("btn_install_pkg"), icon=ft.Icons.DOWNLOAD, on_click=install_pkg, style=ft.ButtonStyle(bgcolor=ACCENT))
                    ]
                    pkg_info_col.visible = True
            except Exception as e:
                pkg_info_col.controls = [ft.Text(utils.t("pkg_not_found", pkg_name=pkg_name), color=ft.Colors.RED_400)]
                pkg_info_col.visible = True
            page.update()

        def install_pkg(e):
            if not current_pkg_name: return
            pkg_log_output.visible = True
            pkg_log_output.controls.clear()
            pkg_log_output.controls.append(ft.Text(utils.t("pkg_installing", pkg_name=current_pkg_name), color=ft.Colors.YELLOW_400))
            page.update()
            
            import platform
            if platform.system() == "Windows":
                venv_python = Path(path) / ".venv" / "Scripts" / "python.exe"
            else:
                venv_python = Path(path) / ".venv" / "bin" / "python3"
            
            def _run_install():
                if not venv_python.exists():
                    pkg_log_output.controls.append(ft.Text(f"Помилка: venv не знайдено! ({venv_python})", color=ft.Colors.RED_400))
                    page.update()
                    return
                try:
                    proc = subprocess.Popen(
                        [str(venv_python), "-m", "pip", "install", current_pkg_name],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True
                    )
                    for line in iter(proc.stdout.readline, ''):
                        if line:
                            pkg_log_output.controls.append(ft.Text(line.strip(), size=11, font_family="monospace"))
                            page.update()
                    proc.wait()
                    if proc.returncode == 0:
                        pkg_log_output.controls.append(ft.Text(utils.t("pkg_install_success"), color=ft.Colors.GREEN_400, weight=ft.FontWeight.BOLD))
                    else:
                        pkg_log_output.controls.append(ft.Text(utils.t("pkg_install_error"), color=ft.Colors.RED_400, weight=ft.FontWeight.BOLD))
                except Exception as ex:
                    pkg_log_output.controls.append(ft.Text(f"Помилка: {ex}", color=ft.Colors.RED_400))
                page.update()
                
            threading.Thread(target=_run_install, daemon=True).start()

        search_btn = ft.IconButton(icon=ft.Icons.SEARCH, on_click=lambda e: search_pkg())
        
        dialog = ft.AlertDialog(
            bgcolor=CARD_BG,
            shape=ft.RoundedRectangleBorder(radius=12),
            title=ft.Text(utils.t("packages_dialog_title")),
            content=ft.Container(
                content=ft.Column([
                    ft.Row([pkg_search_input, search_btn]),
                    ft.Divider(color=BORDER),
                    pkg_info_col,
                    pkg_log_output
                ], tight=True),
                width=450,
            ),
            actions=[
                ft.TextButton(
                    utils.t("btn_close"),
                    on_click=lambda e: page.pop_dialog(),
                    style=ft.ButtonStyle(color=ft.Colors.GREY_400)
                )
            ]
        )
        page.show_dialog(dialog)

    def select_container(item):
        nonlocal selected_container
        selected_container = item
        refresh_list()
        update_action_bar()
        page.update()

    def on_delete_container(name):
        """Показує діалог підтвердження з вибором — видалити лише зі списку або з файлами."""
        nonlocal selected_container

        def do_delete(remove_files: bool):
            nonlocal selected_container
            utils.delete_container(name, remove_files=remove_files)
            if selected_container and selected_container.get("name") == name:
                selected_container = None
            page.pop_dialog()
            refresh_list()
            update_action_bar()
            page.update()

        confirm_dialog = ft.AlertDialog(
            bgcolor=CARD_BG,
            shape=ft.RoundedRectangleBorder(radius=12),
            title=ft.Text(utils.t("delete_title", name=name)),
            content=ft.Text(
                utils.t("delete_desc"),
                size=14,
            ),
            actions=[
                ft.TextButton(
                    utils.t("btn_cancel"),
                    on_click=lambda e: page.pop_dialog(),
                    style=ft.ButtonStyle(color=ft.Colors.GREY_400)
                ),
                ft.TextButton(
                    utils.t("btn_list_only"),
                    on_click=lambda e: do_delete(False),
                    style=ft.ButtonStyle(color=ACCENT)
                ),
                ft.FilledButton(
                    utils.t("btn_with_files"),
                    on_click=lambda e: do_delete(True),
                    style=ft.ButtonStyle(bgcolor=ft.Colors.RED_700, color="white"),
                ),
            ],
        )
        page.show_dialog(confirm_dialog)

    def build_container_card(item):
        is_selected = (
            selected_container is not None
            and selected_container.get("name") == item.get("name")
        )
        path = item.get("path", "")
        return ft.Container(
            content=ft.ListTile(
                leading=ft.Icon(
                    ft.Icons.CHECK_CIRCLE if is_selected else ft.Icons.DEVELOPER_BOARD,
                    color=ACCENT if is_selected else ft.Colors.GREY_400,
                ),
                title=ft.Text(item.get("name", ""), weight=ft.FontWeight.W_600),
                subtitle=ft.Text(
                    f"{item.get('language', '')} • {path}",
                    size=12,
                    color=ft.Colors.GREY_400,
                ),
                trailing=ft.IconButton(
                    icon=ft.Icons.FOLDER_OPEN,
                    tooltip=utils.t("btn_folder"),
                    icon_color=ACCENT if is_selected else ft.Colors.GREY_400,
                    on_click=lambda e, p=path: utils.open_in_folder(p),
                ),
                on_click=lambda e, it=item: select_container(it),
            ),
            border=ft.Border.all(2 if is_selected else 1, ACCENT if is_selected else BORDER),
            border_radius=8,
            bgcolor=CARD_SELECTED if is_selected else CARD_BG,
            padding=ft.Padding.symmetric(horizontal=5, vertical=2),
        )

    def refresh_list():
        containers_list.controls.clear()
        if not utils.containers:
            containers_list.controls.append(
                ft.Container(
                    content=ft.Text(
                        utils.t("empty_list"),
                        color=ft.Colors.GREY_500,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    padding=20,
                    alignment=ft.Alignment.CENTER,
                )
            )
        else:
            for item in utils.containers:
                containers_list.controls.append(build_container_card(item))

    name_field = ft.TextField(
        label=utils.t("container_name"),
        label_style=ft.TextStyle(color=ft.Colors.GREY_400),
        color="white",
        bgcolor="#12121A",
        border=ft.OutlineInputBorder(
            border_radius=ft.BorderRadius.all(8),
            side=ft.BorderSide(color=BORDER),
        ),
        focused_border_color=ACCENT,
        cursor_color=ACCENT,
        prefix_icon=ft.Icons.INVENTORY_2_OUTLINED,
    )
    lang_dropdown = ft.Dropdown(
        label=utils.t("language"),
        label_style=ft.TextStyle(color=ft.Colors.GREY_400),
        value="Python",
        options=[ft.DropdownOption(lang) for lang in utils.LANGUAGE_TEMPLATES.keys()],
        color="white",
        bgcolor="#12121A",
        border_color=BORDER,
        focused_border_color=ACCENT,
        border_radius=8,
    )

    def close_dialog(e):
        name_field.value = ""
        name_field.error_text = None
        page.pop_dialog()

    def create_container(e):
        name = name_field.value.strip()
        if not name:
            name_field.error_text = utils.t("err_enter_name")
            page.update()
            return

        # Перевірка на дублікат назви
        if any(c.get("name") == name for c in utils.containers):
            name_field.error_text = utils.t("err_duplicate")
            page.update()
            return

        try:
            new_item = utils.add_container(name, lang_dropdown.value)
        except Exception as ex:
            name_field.error_text = str(ex)
            page.update()
            return
            
        nonlocal selected_container
        selected_container = new_item
        name_field.value = ""
        name_field.error_text = None
        page.pop_dialog()
        refresh_list()
        update_action_bar()
        page.update()

    def open_dialog(e):
        page.show_dialog(dialog)

    dialog = ft.AlertDialog(
        bgcolor=CARD_BG,
        shape=ft.RoundedRectangleBorder(radius=12),
        title=ft.Row(
            [
                ft.Container(
                    content=ft.Icon(ft.Icons.ADD_BOX_ROUNDED, color="white", size=20),
                    bgcolor=ACCENT,
                    border_radius=8,
                    padding=6,
                ),
                ft.Text(
                    utils.t("new_container"),
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color="white",
                ),
            ],
            spacing=12,
        ),
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Divider(color=BORDER, height=1),
                    name_field,
                    lang_dropdown,
                ],
                spacing=14,
                tight=True,
            ),
            width=360,
            padding=ft.Padding.only(top=8),
        ),
        actions=[
            ft.TextButton(
                "Скасувати",
                on_click=close_dialog,
                style=ft.ButtonStyle(color=ft.Colors.GREY_400),
            ),
            ft.FilledButton(
                "Створити",
                icon=ft.Icons.ADD,
                on_click=create_container,
                style=ft.ButtonStyle(bgcolor=ACCENT, color="white"),
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    create_btn.on_click = open_dialog

    list_box = ft.Container(
        content=containers_list,
        expand=True,
        border=ft.Border.all(1, BORDER),
        padding=15,
        border_radius=8,
    )

    containers_view = ft.Column([list_box, action_bar], expand=True, spacing=15)
    
    help_view = ft.Column([
        ft.Container(
            content=ft.Column([
                ft.Text(utils.t("about_boxer"), size=28, weight=ft.FontWeight.BOLD, color="white"),
                ft.Text(utils.t("about_desc"), size=16, color=ft.Colors.GREY_400),
                ft.Divider(color=BORDER, height=30),
                ft.Text(utils.t("support_author"), size=20, weight=ft.FontWeight.BOLD, color="white"),
                ft.Text(utils.t("support_text"), size=14, color=ft.Colors.GREY_400),
                ft.Container(height=10),
                ft.FilledButton(
                    utils.t("btn_kofi"),
                    icon=ft.Icons.LOCAL_CAFE,
                    url="https://ko-fi.com/romixcaca",
                    style=ft.ButtonStyle(
                        bgcolor="#FFDD00",
                        color="black",
                        padding=20,
                    )
                )
            ], spacing=10),
            padding=30,
            expand=True,
        )
    ], expand=True)

    
    def change_language(e):
        utils.set_lang(e.control.value)
        page.controls.clear()
        main(page)

    lang_dropdown_settings = ft.Dropdown(
        label=utils.t("language_select"),
        options=[
            ft.DropdownOption("uk", "Українська"),
            ft.DropdownOption("en", "English"),
            ft.DropdownOption("de", "Deutsch"),
            ft.DropdownOption("pl", "Polski")
        ],
        value=utils.get_lang(),
        on_select=change_language,
        color="white",
        bgcolor="#12121A",
        border_color=BORDER,
        focused_border_color=ACCENT,
        border_radius=8,
    )

    settings_view = ft.Column([
        ft.Container(
            content=ft.Column([
                ft.Text(utils.t("settings_title"), size=28, weight=ft.FontWeight.BOLD, color="white"),
                ft.Divider(color=BORDER, height=30),
                lang_dropdown_settings,
            ], spacing=10),
            padding=30,
            expand=True,
        )
    ], expand=True)

    view_container = ft.Container(

        content=containers_view,
        expand=True
    )

    def switch_tab(e):
        btn_containers.style = ft.ButtonStyle(color=ACCENT if e.control == btn_containers else ft.Colors.GREY_400)
        btn_help.style = ft.ButtonStyle(color=ACCENT if e.control == btn_help else ft.Colors.GREY_400)
        btn_settings.style = ft.ButtonStyle(color=ACCENT if e.control == btn_settings else ft.Colors.GREY_400)
        
        if e.control == btn_containers:
            view_container.content = containers_view
            create_btn.visible = True
        elif e.control == btn_help:
            view_container.content = help_view
            create_btn.visible = False
        elif e.control == btn_settings:
            view_container.content = settings_view
            create_btn.visible = False
            
        page.update()

    btn_containers.on_click = switch_tab
    btn_help.on_click = switch_tab
    btn_settings.on_click = switch_tab

    body = ft.Container(
        content=ft.Column([top_row, view_container], expand=True, spacing=15),
        padding=15,
        expand=True,
    )

    # Ініціалізація списку та панелі дій
    refresh_list()
    update_action_bar()

    page.add(ft.Column([header, body], expand=True, spacing=0))


if __name__ == "__main__":
    ft.run(main)
