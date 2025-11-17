#!/bin/bash
# Laser Tag System Installation

cd "$(dirname "$0")/.."

sudo apt-get update -qq
sudo apt-get install -y -qq python3 python3-pip python3-tk python3-venv > /dev/null 2>&1

python3 -m venv venv
source venv/bin/activate
pip install -q --upgrade pip
pip install -q psycopg2-binary pillow
pip install -q pygame

echo "Installation complete. Run with: source venv/bin/activate && python3 main.py (from main folder)"