# Define the Python interpreter and Poetry command
PYTHON := poetry run python
POETRY := poetry run

# Define directories to be checked/formatted
SRC_DIR := .
TEST_DIR := tests

# Run Unit Tests
test:
	@echo "Running tests..."
	$(POETRY) pytest $(TEST_DIR)

# Run Black formatter
format:
	@echo "Running Black..."
	$(POETRY) black $(SRC_DIR) $(TEST_DIR)

# Run Flake8 linter
lint:
	@echo "Running Flake8..."
	$(POETRY) flake8 $(SRC_DIR) $(TEST_DIR)

# Run both Black and Flake8
check: format lint

# Clean up unnecessary files
clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -exec rm -f {} +

publish:
	@echo "Publishing..."
	poetry publish --build

# Help command to list all available commands
help:
	@echo "Available make commands:"
	@echo "  make format   - Run Black to format code"
	@echo "  make lint     - Run Flake8 to lint code"
	@echo "  make check    - Run both Black and Flake8"
	@echo "  make clean    - Clean up __pycache__ and .pyc files"
