from web_server import WebServer
from keyboard import KeyboardSender
import os

server = WebServer()
keyboard = KeyboardSender()

# Helper function for login validation ---
def require_login(client_ip):
    if not server.auth_sessions.get(client_ip, False):
        return "<h1>403 Forbidden</h1><p>Please <a href='/'>login</a></p>"
    return None

# Webserver routes
@server.route("/", method="GET")
def login_page(path, form_data, client_ip):
    return """<h1>Login</h1>
<form method="POST" action="/login">
Username: <input name="user_name" /><br>
Password: <input name="user_password" type="password" /><br>
<input type="submit" value="Login" />
</form>"""

@server.route("/login", method="POST")
def login_submit(path, form_data, client_ip):
    try:
        if server.too_many_attempts(client_ip):
            return "<h1>Too many failed attempts</h1><p>Try again later.</p>"

        submitted_user = form_data.get("user_name", "")
        submitted_pass = form_data.get("user_password", "")
        if submitted_user == os.getenv("WEB_USER") and submitted_pass == os.getenv("WEB_PASSWORD"):
            server.auth_ip(client_ip)
            server.reset_attempts(client_ip)
            return """<meta http-equiv="refresh" content="0;url=/form" />"""

        return "<h1>Login failed</h1><p><a href='/'>Try again</a></p>"
    except Exception as e:
        print(f"login_submit error: {e}")
        return "<h1>Error</h1><p>Unexpected error occurred.</p>"

@server.route("/form", method="GET")
def form_page(path, form_data, client_ip):
    try:
        auth_check = require_login(client_ip)
        if auth_check:
            return auth_check

        special_keys_html = ''.join(
            f'<li><strong>{k}</strong> - {keyboard.SPECIAL_KEYS[k]["description"]}</li>'
            for k in sorted(keyboard.SPECIAL_KEYS, key=lambda k:keyboard.SPECIAL_KEYS[k]['order'])
        )

        return f"""
            <h1>Send Keystrokes</h1>
            <form method="POST" action="/submit">
                <input type="text" name="input_text" />
                <input type="submit" />
            </form>
            <h2>Special Keyboard Keys</h2>
            <p>Use the following special words to send keyboard keys:</p>
            <ul>
                {special_keys_html}
            </ul>
            <h2>Chording Keys</h2>
            <p>Use the <strong>+</strong> symbol to join keys, e.g. <strong>CTRL+ALT+DEL</strong></p>
            <h2>Special Characters</h2>
            <p>To send the <strong>+</strong> symbol itself, type <strong>PLUS</strong>.</p>
        """

    except Exception as e:
        print(f"form_page error: {e}")
        return "<h1>Error</h1>"

@server.route("/submit", method="POST")
def handle_keystroke(path, form_data, client_ip=None):
    try:
        auth_check = require_login(client_ip)
        if auth_check:
            return auth_check

        message = form_data.get("input_text", "")
        if message:
            keyboard.send(message)
            return f"<h1>Sent!</h1><p>Sent: {message}</p><a href='/form'>Back</a>"
        return "<h1>No input</h1><a href='/form'>Back</a>"
    except Exception as e:
        print(f"handle_keystroke error: {e}")
        return "<h1>Error</h1>"

# Start webserver
try:
    server.start()
except Exception as e:
    print(f"Fatal error in server.start(): {e}")