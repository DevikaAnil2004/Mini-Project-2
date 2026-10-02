#!/bin/bash

# CricketIQ Setup Script
# This script automates the setup process for local development

set -e

echo "================================================"
echo "   CricketIQ - IPL Analytics Platform"
echo "   Setup Script v1.0"
echo "================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"
echo ""

# Create virtual environment
echo -e "${YELLOW}Creating virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi
echo ""

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install --upgrade pip > /dev/null
pip install -r requirements.txt > /dev/null
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Check MySQL
echo -e "${YELLOW}Checking MySQL installation...${NC}"
if command -v mysql &> /dev/null; then
    echo -e "${GREEN}✓ MySQL is installed${NC}"
else
    echo -e "${RED}✗ MySQL not found. Please install MySQL and try again.${NC}"
    echo "  macOS: brew install mysql"
    echo "  Ubuntu: sudo apt-get install mysql-server"
    exit 1
fi
echo ""

# Ask for database credentials
echo -e "${YELLOW}Database Configuration${NC}"
read -p "MySQL username [root]: " mysql_user
mysql_user=${mysql_user:-root}

read -sp "MySQL password (enter for no password): " mysql_password
echo ""

read -p "MySQL host [localhost]: " mysql_host
mysql_host=${mysql_host:-localhost}

read -p "MySQL port [3306]: " mysql_port
mysql_port=${mysql_port:-3306}

read -p "Database name [cricketiq]: " mysql_database
mysql_database=${mysql_database:-cricketiq}

# Update .env file
echo -e "${YELLOW}Updating .env file...${NC}"
cat > .env << EOF
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=True

# MySQL Configuration
MYSQL_HOST=$mysql_host
MYSQL_USER=$mysql_user
MYSQL_PASSWORD=$mysql_password
MYSQL_PORT=$mysql_port
MYSQL_DATABASE=$mysql_database

# Flask Configuration
SECRET_KEY=dev-secret-key-$(date +%s)
EOF
echo -e "${GREEN}✓ .env file created${NC}"
echo ""

# Create database
echo -e "${YELLOW}Creating MySQL database...${NC}"
if [ -z "$mysql_password" ]; then
    mysql -h "$mysql_host" -P "$mysql_port" -u "$mysql_user" << EOF
CREATE DATABASE IF NOT EXISTS $mysql_database;
EXIT;
EOF
else
    mysql -h "$mysql_host" -P "$mysql_port" -u "$mysql_user" -p"$mysql_password" << EOF
CREATE DATABASE IF NOT EXISTS $mysql_database;
EXIT;
EOF
fi
echo -e "${GREEN}✓ Database created${NC}"
echo ""

# Initialize database with sample data
echo -e "${YELLOW}Initializing database...${NC}"
python init_db.py
echo -e "${GREEN}✓ Database initialized${NC}"
echo ""

# Summary
echo "================================================"
echo -e "${GREEN}Setup Complete!${NC}"
echo "================================================"
echo ""
echo -e "${GREEN}To start the application:${NC}"
echo ""
echo "1. Activate virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Run the Flask app:"
echo "   python app.py"
echo ""
echo "3. Open your browser:"
echo "   http://localhost:5000"
echo ""
echo -e "${YELLOW}Configuration Details:${NC}"
echo "  MySQL Host: $mysql_host"
echo "  MySQL User: $mysql_user"
echo "  Database: $mysql_database"
echo ""
echo "For help, see: README.md or QUICKSTART.md"
echo ""
