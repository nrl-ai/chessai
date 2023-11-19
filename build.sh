#!/bin/bash
set -e

# Remove any existing build artifacts
rm -rf chessai/frontend-dist || true
rm -rf build || true
rm -rf dist || true
rm -rf chessai.egg-info || true
rm -rf frontend/.next || true
rm -rf frontend/dist || true

# Build the frontend
bash build_frontend.sh

# Build the package
python -m build --sdist --wheel .
