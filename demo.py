"""A beautiful, fully-working multi-page website powered by Python only."""

from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

import about
import contact
import home
import Login


PORT = 8000


def render_layout(title: str, active: str, content: str) -> str:
    nav_items = [
        ("/", "Home"),
        ("/about", "About"),
        ("/contact", "Contact"),
        ("/login", "Login"),
    ]
    nav_html = "".join(
        f'<a href="{href}" class="{"active" if active == href else ""}">{name}</a>'
        for href, name in nav_items
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{escape(title)} | Python Learning</title>
  <style>
    :root {{
      --bg: #0b1020;
      --card: #121933;
      --text: #ecf0ff;
      --muted: #b4bddc;
      --accent: #7c8cff;
      --accent-2: #4ee1c1;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Inter, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
      color: var(--text);
      background:
        radial-gradient(circle at 20% 10%, rgba(124,140,255,0.25), transparent 30%),
        radial-gradient(circle at 80% 20%, rgba(78,225,193,0.2), transparent 28%),
        var(--bg);
      min-height: 100vh;
    }}
    .container {{ max-width: 1000px; margin: 0 auto; padding: 24px; }}
    nav {{
      position: sticky;
      top: 0;
      backdrop-filter: blur(8px);
      background: rgba(11,16,32,0.65);
      border-bottom: 1px solid rgba(255,255,255,0.08);
      z-index: 10;
    }}
    .nav-inner {{ display: flex; gap: 14px; align-items: center; justify-content: space-between; }}
    .brand {{ font-weight: 700; letter-spacing: 0.5px; }}
    .links a {{
      color: var(--muted);
      text-decoration: none;
      margin-left: 10px;
      padding: 8px 12px;
      border-radius: 10px;
      transition: .2s;
    }}
    .links a:hover, .links a.active {{
      color: white;
      background: rgba(124,140,255,0.25);
    }}
    .hero {{
      margin-top: 28px;
      padding: 28px;
      border-radius: 20px;
      background: linear-gradient(145deg, rgba(124,140,255,0.20), rgba(78,225,193,0.12));
      border: 1px solid rgba(255,255,255,0.12);
      box-shadow: 0 16px 40px rgba(0,0,0,0.28);
    }}
    h1, h2, h3 {{ margin-top: 0; }}
    p {{ color: var(--muted); line-height: 1.65; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-top: 20px; }}
    .card {{
      background: var(--card);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 16px;
      padding: 16px;
    }}
    input {{
      width: 100%;
      margin: 8px 0 14px;
      padding: 10px 12px;
      border-radius: 10px;
      border: 1px solid rgba(255,255,255,0.18);
      background: #0d1430;
      color: white;
    }}
    button {{
      border: none;
      background: linear-gradient(135deg, var(--accent), var(--accent-2));
      color: #091024;
      font-weight: 700;
      padding: 10px 14px;
      border-radius: 10px;
      cursor: pointer;
    }}
    .pill {{
      display: inline-block;
      border-radius: 999px;
      padding: 5px 10px;
      background: rgba(78,225,193,0.20);
      border: 1px solid rgba(78,225,193,0.35);
      color: #bef6ea;
      font-size: 12px;
    }}
  </style>
</head>
<body>
  <nav>
    <div class="container nav-inner">
      <div class="brand">✨ Python Learning</div>
      <div class="links">{nav_html}</div>
    </div>
  </nav>
  <main class="container">
    {content}
  </main>
</body>
</html>
"""


def home_page() -> str:
    cards = "".join(
        f"<div class='card'><h3>{f['icon']} {escape(f['title'])}</h3><p>{escape(f['description'])}</p></div>"
        for f in home.FEATURES
    )
    return f"""
    <section class="hero">
      <span class="pill">Beautiful by default</span>
      <h1>{escape(home.TITLE)}</h1>
      <p>{escape(home.SUBTITLE)}</p>
      <div class="grid">{cards}</div>
    </section>
    """


def about_page() -> str:
    items = "".join(
        f"<div class='card'><h3>{escape(name)}</h3><p>{escape(desc)}</p></div>"
        for name, desc in about.VALUES
    )
    return f"""
    <section class="hero">
      <h1>{escape(about.TITLE)}</h1>
      <p>{escape(about.BODY)}</p>
      <div class="grid">{items}</div>
    </section>
    """


def contact_page() -> str:
    entries = "".join(
        f"<div class='card'><h3>{escape(k)}</h3><p>{escape(v)}</p></div>"
        for k, v in contact.CONTACT_ITEMS
    )
    return f"""
    <section class="hero">
      <h1>{escape(contact.TITLE)}</h1>
      <p>{escape(contact.DESCRIPTION)}</p>
      <div class="grid">{entries}</div>
    </section>
    """


def login_page(message: str = "") -> str:
    banner = f"<p class='pill'>{escape(message)}</p>" if message else ""
    return f"""
    <section class="hero" style="max-width: 560px;">
      <h1>{escape(Login.TITLE)}</h1>
      <p>{escape(Login.DESCRIPTION)}</p>
      {banner}
      <form method="post" action="/login">
        <label>Username</label>
        <input type="text" name="username" placeholder="Enter username" required />
        <label>Password</label>
        <input type="password" name="password" placeholder="At least 6 characters" required />
        <button type="submit">Sign In</button>
      </form>
    </section>
    """


class SiteHandler(BaseHTTPRequestHandler):
    def _send_html(self, html: str, status: int = 200) -> None:
        data = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path

        if path == "/":
            self._send_html(render_layout("Home", "/", home_page()))
        elif path == "/about":
            self._send_html(render_layout("About", "/about", about_page()))
        elif path == "/contact":
            self._send_html(render_layout("Contact", "/contact", contact_page()))
        elif path == "/login":
            self._send_html(render_layout("Login", "/login", login_page()))
        else:
            self._send_html(
                render_layout(
                    "Not Found",
                    "",
                    "<section class='hero'><h1>404</h1><p>The page you requested was not found.</p></section>",
                ),
                status=404,
            )

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path != "/login":
            self._send_html(render_layout("Not Found", "", "<section class='hero'><h1>404</h1></section>"), status=404)
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        payload = self.rfile.read(content_length).decode("utf-8")
        form = parse_qs(payload)
        username = form.get("username", [""])[0]
        password = form.get("password", [""])[0]

        if Login.validate_credentials(username, password):
            message = f"Welcome, {username}! Login accepted."
        else:
            message = "Login failed: username required and password must be at least 6 chars."

        self._send_html(render_layout("Login", "/login", login_page(message)))


def run() -> None:
    server = HTTPServer(("0.0.0.0", PORT), SiteHandler)
    print(f"Server running at http://localhost:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    run()
