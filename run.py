import os

from flaskblog import create_app

app = create_app()

if __name__ == "__main__":
    # Set FLASK_DEBUG=1 locally to enable the debugger and auto-reload.
    # Never enable the debugger in production (it allows code execution).
    app.run(host='0.0.0.0', debug=os.environ.get('FLASK_DEBUG', '0') == '1')
