#!/usr/bin/env python3
"""Vercel entrypoint for Streamlit app."""
import subprocess
import sys

if __name__ == "__main__":
    # Run Streamlit app
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"])
