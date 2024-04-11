import subprocess
import sys
import flet as ft


def troca_tema(e):
    # Alterna entre os temas claro e escuro
    e.page.theme_mode = (
        ft.ThemeMode.DARK if e.page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
    )
    # Atualiza o ícone do AppBar com base no tema atual
    if e.page.theme_mode == ft.ThemeMode.DARK:
        e.page.appbar.actions[0].icon = ft.icons.DARK_MODE_OUTLINED
    else:
        e.page.appbar.actions[0].icon = ft.icons.WB_SUNNY_OUTLINED
    e.page.update()


def main(page: ft.Page):
    page.title = "SpotiPy"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.DOWNLOAD),
        leading_width=40,
        title=ft.Text("SpotiPy Downloader"),
        center_title=False,
        bgcolor=ft.colors.GREEN_900,
        actions=[
            ft.IconButton(ft.icons.WB_SUNNY_OUTLINED, on_click=troca_tema),
            ft.IconButton(ft.icons.INFO, on_click=lambda e: abrir_dialogo_info(e))
        ],

    )

    # Função para abrir o diálogo de informações
    def abrir_dialogo_info(e):
        dlg_info = ft.AlertDialog(
            title=ft.Text("Informações do Projeto"),
            content=ft.Text("Desenvolvedor: Alison santos", size=16)
        )
        page.dialog = dlg_info
        dlg_info.open = True
        page.update()

    def radiogroup_changed(e):
        global check
        r.value = f"Selecionado: {e.control.value}"
        check = e.control.value

        if e.control.value == "Playlist":
            msc.label = "Link da Playlist"
        else:
            msc.label = "Link da Música"
        page.update()

    def baixar_musica(e):
        url_spotify = msc.value
        destino = fold.value
        if not url_spotify.strip() or not destino.strip():
            r.value = "Por favor, insira o link e o caminho da pasta."
            page.update()
            return
        try:
            if check:
                r.value = "Realizando Download..."
                progress_bar = ft.ProgressBar()
                page.add(progress_bar)
                page.update()
                print("Executando")
                subprocess.check_call(
                    [sys.executable, "-m", "spotdl", "--output", destino, url_spotify])
                print("Execução finalizada!")
                progress_bar.value = 100
                page.update()
                r.value = "Download concluído."
                page.update()
        except Exception as e:
            r.value = ft.Text("Erro encontrado: " + str(e), color=ft.colors.RED)
            page.update()

    def limpa_campos(e):
        msc.value = ""
        fold.value = ""
        r.value = ""
        page.update()

    r = ft.Text()
    t = ft.Text()
    msc = ft.TextField(label="Link de Música", icon=ft.icons.MUSIC_NOTE)
    fold = ft.TextField(label="Destino", icon=ft.icons.FOLDER_SPECIAL)
    b = ft.ElevatedButton(text="Baixar", on_click=baixar_musica)
    reset = ft.ElevatedButton(text="Limpar campos", on_click=limpa_campos)

    cg = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="Música", label="Música", label_position=ft.LabelPosition.LEFT),
        ft.Radio(value="Playlist", label="Playlist", label_position=ft.LabelPosition.LEFT)
    ]), on_change=radiogroup_changed)

    page.add(ft.Column([
        r,
        ft.Row([(ft.Text("Bem-vindo ao SpotiPy Downloader!", size=24, weight=ft.FontWeight.BOLD))
                ], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([(ft.Text("Use este aplicativo para baixar músicas do Spotify.", size=18))
                ], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([ft.Text("Escolha um tipo:"), cg], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([msc, fold, b, reset], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([r, t], alignment=ft.MainAxisAlignment.CENTER)
    ], alignment=ft.MainAxisAlignment.CENTER))


ft.app(target=main)
