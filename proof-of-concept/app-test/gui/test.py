import flet as ft

def main(page: ft.Page):
    page.title = "Flet counter example of Pigeonism"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor=ft.Colors.GREY_800

    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)
    txt_pigeon = ft.TextField(value="Pigeon forever <333", text_align=ft.TextAlign.RIGHT, width=200, read_only=True)

    gradient = ft.LinearGradient(
        colors=[ft.colors.YELLOW, ft.colors.RED],
        begin=ft.Alignment(-1, -1),
        end=ft.Alignment(1, 1)
    )

    pigeon_img = ft.Container(
        bgcolor=gradient,
        width=400,
        height=400,
        alignment=ft.alignment.center,
        content=ft.Column(
            controls=[
                ft.Text("A threatening and dangerously liberal Pigeon !", size=20, color=ft.colors.BLUE, font_family="Comic Sans MS"),
                ft.Image(src="https://d.newsweek.com/en/full/2239325/pigeon.webp", width=200, height=200)
                ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

    page.add(
        ft.Row(
            [
                pigeon_img,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    page.add(
        ft.Row(
            [
                ft.IconButton(ft.Icons.REMOVE, on_click=minus_click),
                txt_number,
                ft.IconButton(ft.Icons.ADD, on_click=plus_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )
    page.add(
        ft.Row(
            [
                txt_pigeon,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )
    

def run_test():
    ft.app(main)

run_test()