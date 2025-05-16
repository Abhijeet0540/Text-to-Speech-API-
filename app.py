"""
Entry point for the Render deployment.
This file imports the Flask application from coqui_tts_fallback.py.
"""

# Import the Flask application from coqui_tts_fallback.py
from coqui_tts_fallback import app

# This is required for Gunicorn to find the app
if __name__ == '__main__':
    app.run()
