import flet as ft
from flet.auth.providers import GoogleOAuthProvider
from decouple import config

client_id = config('client_id')
client_secret = config('client_secret')

def main(page: ft.Page):
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
    page.title = "Google OAuth Example"
    page.window.height = 300
    page.window.width = 300

    def logingoogle(e):
        try:
            page.login(provider)
        except Exception as ex:
            print(f"Login failed: {ex}")
            resulttxt.controls.append(ft.Text(f"Login failed: {ex}"))
            resulttxt.update()

    def on_login(e):
        print("User Info:", page.auth.user)
        resulttxt.controls.append(
            ft.Column([
                ft.Text(f"name: {page.auth.user.get('name')}"),
                ft.Text(f"email: {page.auth.user.get('email')}"),
                ft.Text(f"id: {page.auth.user.id}"),
                ft.Text(f"access token: {page.auth.token.access_token}")
            ])
        )
        resulttxt.update()

    appbar = ft.AppBar(
        leading= ft.Image(
                        src=f"logo.png",
                        width=100,
                        height=100,
                        fit=ft.ImageFit.CONTAIN),
        bgcolor="rgba(79,86,97,1)",
        actions=[
            ft.IconButton(icon=ft.icons.LOGIN, on_click=logingoogle)
        ]
    )


    provider = GoogleOAuthProvider(
        client_id=client_id,
        client_secret=client_secret,
        redirect_url="http://localhost:8550/oauth_callback"  # Same port as app
    )

    resulttxt = ft.Column()

    # Check for OAuth redirect query parameters
    try:
        auth_code = page.query["code"]  # Access the 'code' parameter directly
        print(f"Authorization Code Received: {auth_code}")
        # Process the authorization code to exchange for tokens if needed
        resulttxt.controls.append(ft.Text("Login Successful!"))
        resulttxt.update()
    except:
        # If no 'code' parameter exists, it's a normal page load
        pass

    page.on_login = on_login
    page.add(appbar,
        resulttxt
    )

ft.app(target=main, port=8550, view=ft.AppView.WEB_BROWSER)