#!/bin/bash

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Logo
print_logo() {
    echo -e "${CYAN}"
    cat << "EOF"
   ██████╗██╗   ██╗██████╗ ███████╗ ██████╗ ██████╗     ██████╗ ███████╗███████╗███████╗████████╗
  ██╔════╝██║   ██║██╔══██╗██╔════╝██╔═══██╗██╔══██╗    ██╔══██╗██╔════╝██╔════╝██╔════╝╚══██╔══╝
  ██║     ██║   ██║██████╔╝███████╗██║   ██║██████╔╝    ██████╔╝█████╗  ███████╗█████╗     ██║   
  ██║     ██║   ██║██╔══██╗╚════██║██║   ██║██╔══██╗    ██╔══██╗██╔══╝  ╚════██║██╔══╝     ██║   
  ╚██████╗╚██████╔╝██║  ██║███████║╚██████╔╝██║  ██║    ██║  ██║███████╗███████║███████╗   ██║   
   ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝    ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝   ╚═╝   
EOF
    echo -e "${NC}"
    echo -e "${GREEN}🚀 Cursor Reset Tool${NC}"
    echo -e "${CYAN}Reset your Cursor trial with one command${NC}"
    echo ""
}

# Check if running on macOS
check_macos() {
    if [[ "$(uname)" != "Darwin" ]]; then
        echo -e "${RED}❌ Error: This script only works on macOS${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ macOS detected${NC}"
}

# Check if Python 3 is installed
check_python() {
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Error: Python 3 is not installed${NC}"
        echo -e "${YELLOW}Please install Python 3 first${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Python 3 found: $(python3 --version)${NC}"
}

# Download and run the reset script
run_reset() {
    local tmp_script="/tmp/cursor_reset.py"
    local script_url="https://raw.githubusercontent.com/kunnew020/cursor-reset/main/cursor_reset.py"
    
    echo -e "${CYAN}⬇️  Downloading reset script...${NC}"
    if ! curl -fsSL "$script_url" -o "$tmp_script"; then
        echo -e "${RED}❌ Failed to download script${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Script downloaded${NC}"
    echo ""
    echo -e "${YELLOW}⚠️  Important:${NC}"
    echo -e "${YELLOW}   • Make sure Cursor is CLOSED before continuing${NC}"
    echo -e "${YELLOW}   • You will need to enter your admin password${NC}"
    echo -e "${YELLOW}   • Backups will be created automatically${NC}"
    echo ""
    
    # Run with sudo
    echo -e "${CYAN}🔐 Running reset script with admin privileges...${NC}"
    if sudo python3 "$tmp_script"; then
        echo ""
        echo -e "${GREEN}✅ Reset completed successfully!${NC}"
        echo -e "${CYAN}ℹ️  Please restart Cursor to apply changes${NC}"
    else
        echo ""
        echo -e "${RED}❌ Reset failed${NC}"
    fi
    
    # Cleanup
    rm -f "$tmp_script"
}

# Main function
main() {
    print_logo
    check_macos
    check_python
    echo ""
    run_reset
}

# Run main
main

