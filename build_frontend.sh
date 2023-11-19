#!/bin/sh
set -e
cd frontend && npm install && npm run build && cd ..
rm -rf chessai/frontend-dist || true
mv frontend/out chessai/frontend-dist
