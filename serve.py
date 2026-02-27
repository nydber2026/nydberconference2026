"""
serve.py — Local development server for the conference website template.

Usage:
    python serve.py          # Serves on http://localhost:8000
    python serve.py 9000     # Serves on http://localhost:9000

This script uses Python's built-in HTTP server — no packages to install.
It serves all files in the current directory, so run it from the project root.
"""

import http.server
import socketserver
import sys
import os
import webbrowser


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Default port if none is provided on the command line.
DEFAULT_PORT = 8000

# Read an optional port argument, e.g. `python serve.py 9000`.
port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT

# The directory to serve — always the folder that contains this script,
# regardless of where you run it from.
serve_dir = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------------------
# Request handler
# ---------------------------------------------------------------------------

class Handler(http.server.SimpleHTTPRequestHandler):
    """
    Extends the standard handler to:
      - Serve files from the project root (not the shell's cwd).
      - Suppress the per-request log lines that clutter the terminal.
        Remove the `log_message` override below if you want them back.
    """

    def __init__(self, *args, **kwargs):
        # `directory` tells SimpleHTTPRequestHandler which folder to serve.
        super().__init__(*args, directory=serve_dir, **kwargs)

    def log_message(self, format, *args):
        # Uncomment the line below to see every request logged to stdout.
        # super().log_message(format, *args)
        pass


# ---------------------------------------------------------------------------
# Start the server
# ---------------------------------------------------------------------------

# Allow quick restarts without "Address already in use" errors.
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", port), Handler) as httpd:
    url = f"http://localhost:{port}"
    print(f"Serving at {url}")
    print("Press Ctrl+C to stop.\n")

    # Open the site in the default browser automatically.
    webbrowser.open(url)

    try:
        # Block forever, handling one request at a time.
        httpd.serve_forever()
    except KeyboardInterrupt:
        # Ctrl+C is the normal way to stop; exit cleanly without a traceback.
        print("\nServer stopped.")