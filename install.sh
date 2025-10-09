#!/bin/bash
# This script sets up the Python environment and PostgreSQL database

set -e  # Exit on error

echo "=========================================="
echo "Laser Tag System Installation"
echo "=========================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running on Linux/Mac
if [[ "$OSTYPE" != "linux-gnu"* ]] && [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${YELLOW}Warning: This script is designed for Linux/Mac. Windows users should use install.bat${NC}"
fi

# Check for Python 3
echo "Checking for Python 3..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}Found Python $PYTHON_VERSION${NC}"
echo ""

# Check for PostgreSQL
echo "Checking for PostgreSQL..."
if ! command -v psql &> /dev/null; then
    echo -e "${RED}Error: PostgreSQL is not installed.${NC}"
    echo "Please install PostgreSQL and try again."
    echo "Ubuntu/Debian: sudo apt-get install postgresql postgresql-contrib"
    echo "Mac (Homebrew): brew install postgresql"
    exit 1
fi

PSQL_VERSION=$(psql --version | cut -d' ' -f3)
echo -e "${GREEN}Found PostgreSQL $PSQL_VERSION${NC}"
echo ""

# Create virtual environment
echo "Creating Python virtual environment..."
if [ -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment already exists. Skipping creation.${NC}"
else
    python3 -m venv venv
    echo -e "${GREEN}Virtual environment created.${NC}"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
echo ""

# Install Python dependencies
echo "Installing Python dependencies..."
pip install psycopg2-binary pillow
echo -e "${GREEN}Python dependencies installed.${NC}"
echo ""

# Setup PostgreSQL database
echo "Setting up PostgreSQL database..."
echo -e "${YELLOW}This will create a database named 'photon' with user 'student'${NC}"
read -p "Continue? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Check if database exists
    if sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw photon; then
        echo -e "${YELLOW}Database 'photon' already exists.${NC}"
        read -p "Drop and recreate? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            sudo -u postgres psql -c "DROP DATABASE photon;"
            echo "Database dropped."
        else
            echo "Keeping existing database."
        fi
    fi
    
    # Create database if it doesn't exist
    if ! sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw photon; then
        sudo -u postgres psql -c "CREATE DATABASE photon;"
        echo -e "${GREEN}Database 'photon' created.${NC}"
    fi
    
    # Check if user exists
    if sudo -u postgres psql -t -c "SELECT 1 FROM pg_roles WHERE rolname='student'" | grep -q 1; then
        echo -e "${YELLOW}User 'student' already exists.${NC}"
    else
        sudo -u postgres psql -c "CREATE USER student;"
        echo -e "${GREEN}User 'student' created.${NC}"
    fi
    
    # Grant privileges
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE photon TO student;"
    echo -e "${GREEN}Privileges granted.${NC}"
    
    # Create players table
    echo "Creating players table..."
    sudo -u postgres psql -d photon -c "
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY,
        codename VARCHAR(255) NOT NULL
    );"
    
    # Grant table privileges to student
    sudo -u postgres psql -d photon -c "GRANT ALL PRIVILEGES ON TABLE players TO student;"
    
    echo -e "${GREEN}Players table created.${NC}"
else
    echo -e "${YELLOW}Skipping database setup.${NC}"
fi
echo ""

# Check for logo.jpg
echo "Checking for logo.jpg..."
if [ ! -f "logo.jpg" ]; then
    echo -e "${YELLOW}Warning: logo.jpg not found in current directory.${NC}"
    echo "The application requires logo.jpg for the splash screen."
    echo "Please add logo.jpg to the project directory before running."
fi
echo ""

# Create requirements.txt for future reference
echo "Creating requirements.txt..."
cat > requirements.txt << EOF
psycopg2-binary>=2.9.0
pillow>=10.0.0
EOF
echo -e "${GREEN}requirements.txt created.${NC}"
echo ""

# Create run script
echo "Creating run script..."
cat > run.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
python3 main.py
EOF
chmod +x run.sh
echo -e "${GREEN}run.sh created.${NC}"
echo ""

echo "=========================================="
echo -e "${GREEN}Installation Complete!${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Make sure logo.jpg is in the project directory"
echo "2. Run the application with: ./run.sh"
echo "   Or manually: source venv/bin/activate && python3 main.py"
echo ""
echo "To start the UDP server (for testing):"
echo "   source venv/bin/activate && python3 udpserver.py"
echo ""
echo "Database Info:"
echo "   Database: photon"
echo "   User: student"
echo "   Connect: psql -U student -d photon"
echo ""