#!/bin/bash
# run_tests.sh - Automated test runner for the Dash application

# Set strict mode: exit on error, undefined variables are errors, pipeline failures are caught
set -euo pipefail

# Define color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}  Soul Foods Dash App - Test Runner${NC}"
echo -e "${YELLOW}========================================${NC}"

# Step 1: Activate the virtual environment
echo -e "\n${YELLOW}[1/3] Activating virtual environment...${NC}"

# Check if .venv exists
if [ ! -d ".venv" ]; then
    echo -e "${RED}ERROR: Virtual environment (.venv) not found!${NC}"
    echo "Please create it first with: python -m venv .venv"
    exit 1
fi

# Activate the virtual environment (works on both Git Bash and Unix)
if [ -f ".venv/Scripts/activate" ]; then
    # Windows (Git Bash)
    source .venv/Scripts/activate
elif [ -f ".venv/bin/activate" ]; then
    # Unix / Linux / macOS
    source .venv/bin/activate
else
    echo -e "${RED}ERROR: Could not find activation script!${NC}"
    exit 1
fi

# Verify activation
if [ -z "${VIRTUAL_ENV:-}" ]; then
    echo -e "${RED}ERROR: Failed to activate virtual environment!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Virtual environment activated: ${VIRTUAL_ENV}${NC}"

# Step 2: Run the test suite
echo -e "\n${YELLOW}[2/3] Running test suite...${NC}"

# Run pytest with verbose output
if python -m pytest test_app.py -v --tb=short; then
    echo -e "\n${GREEN}✓ All tests passed!${NC}"
    TEST_RESULT=0
else
    TEST_RESULT=$?
    echo -e "\n${RED}✗ Some tests failed!${NC}"
fi

# Step 3: Return appropriate exit code
echo -e "\n${YELLOW}[3/3] Test run completed with exit code: ${TEST_RESULT}${NC}"

if [ $TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  ✅ All tests passed successfully!${NC}"
    echo -e "${GREEN}========================================${NC}"
else
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}  ❌ Tests failed. Please check the output above.${NC}"
    echo -e "${RED}========================================${NC}"
fi

# Deactivate virtual environment (optional, but good practice)
deactivate 2>/dev/null || true

exit $TEST_RESULT