import flet as ft

def main(page: ft.Page):
    # Define what happens when the button is clicked
    def show_dialog(event):
        # Create an AlertDialog that acts as a new "window"
        dialog = ft.AlertDialog(
            title=ft.Text("New Window"),
            content=ft.Text("This is the content of the new window."),
            actions=[
                ft.TextButton("Close", on_click=lambda e: close_dialog())
            ]
        )
        
        # Function to close the dialog
        def close_dialog():
            dialog.open = False
            page.update()

        # Open the dialog and update the page
        dialog.open = True
        page.dialog = dialog
        page.update()

    # Create a button that triggers the show_dialog function when clicked
    open_button = ft.ElevatedButton(text="Open Window", on_click=show_dialog)
    
    # Add the button to the page
    page.add(open_button)

# Run the Flet app with the main function as the entry point
ft.app(target=main)
