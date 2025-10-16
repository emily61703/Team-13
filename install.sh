#!/bin/bash
# Simple installation script for Laser Tag System

echo "=========================================="
echo "Laser Tag System - Simple Installation"
echo "=========================================="
echo ""

# Update package list
echo "Updating package list..."
sudo apt-get update
echo ""

# Install system packages
echo "Installing system packages..."
sudo apt-get install -y python3 python3-pip python3-tk python3-venv postgresql postgresql-contrib
echo "System packages installed."
echo ""

# Start PostgreSQL
echo "Starting PostgreSQL service..."
sudo systemctl start postgresql
sudo systemctl enable postgresql
echo "PostgreSQL started."
echo ""

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
echo "Virtual environment created."
echo ""

# Activate virtual environment and install Python packages
echo "Installing Python packages..."
source venv/bin/activate
pip install --upgrade pip
pip install psycopg2-binary pillow
echo "Python packages installed."
echo ""

echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Setup the database by running: sudo -u postgres psql"
echo "   Then run these commands:"
echo "   CREATE DATABASE photon;"
echo "   CREATE USER student;"
echo "   GRANT ALL PRIVILEGES ON DATABASE photon TO student;"
echo "   \\c photon"
echo "   CREATE TABLE players (id INTEGER PRIMARY KEY, codename VARCHAR(255) NOT NULL);"
echo "   GRANT ALL PRIVILEGES ON TABLE players TO student;"
echo "   \\q"
echo ""
echo "2. Add logo.jpg to the project directory"
echo ""
echo "3. Run the application:"
echo "   source venv/bin/activate"
echo "   python3 main.py"
echo ""