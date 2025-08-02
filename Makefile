# JSON Prompt Formatter - Makefile
# Convenient commands for development and deployment

.PHONY: help install clean test build deploy demo examples lint format check-deps

# Default target
help:
	@echo "JSON Prompt Formatter - Available Commands"
	@echo "=========================================="
	@echo ""
	@echo "Development:"
	@echo "  install      Install package in development mode"
	@echo "  clean        Clean build artifacts and cache files"
	@echo "  test         Run tests (if available)"
	@echo "  lint         Run code linting"
	@echo "  format       Format code with black"
	@echo "  check-deps   Check for required dependencies"
	@echo ""
	@echo "Building & Deployment:"
	@echo "  build        Build distribution packages"
	@echo "  deploy-test  Deploy to Test PyPI"
	@echo "  deploy       Deploy to PyPI (production)"
	@echo "  check        Check package integrity"
	@echo ""
	@echo "Examples & Demo:"
	@echo "  demo         Run interactive demo"
	@echo "  examples     Generate example outputs"
	@echo "  quick-test   Quick functionality test"
	@echo ""
	@echo "Usage Examples:"
	@echo "  make install && make demo"
	@echo "  make examples"
	@echo "  make build && make deploy-test"

# Development commands
install:
	@echo "📦 Installing package in development mode..."
	pip install -e .
	@echo "✅ Installation complete"

clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf outputs/*.json
	rm -rf outputs/*.jsonl
	rm -rf examples/temp_demo/
	@echo "✅ Clean complete"

test:
	@echo "🧪 Running tests..."
	@if [ -d "tests" ]; then \
		python -m pytest tests/ -v; \
	else \
		echo "ℹ️  No tests directory found. Running quick functionality test..."; \
		python -c "from formatter import main; print('✅ Formatter module loads correctly')"; \
		python -c "from json_to_jsonl import main; print('✅ JSON to JSONL module loads correctly')"; \
	fi

lint:
	@echo "🔍 Running code linting..."
	@if command -v flake8 >/dev/null 2>&1; then \
		flake8 formatter.py json_to_jsonl.py --max-line-length=100; \
		echo "✅ Linting complete"; \
	else \
		echo "ℹ️  flake8 not installed. Install with: pip install flake8"; \
	fi

format:
	@echo "🎨 Formatting code..."
	@if command -v black >/dev/null 2>&1; then \
		black formatter.py json_to_jsonl.py --line-length=100; \
		echo "✅ Formatting complete"; \
	else \
		echo "ℹ️  black not installed. Install with: pip install black"; \
	fi

check-deps:
	@echo "🔍 Checking dependencies..."
	@python -c "import sys; print(f'Python: {sys.version}')"
	@python -c "import json; print('✅ json module available')"
	@python -c "import pathlib; print('✅ pathlib module available')"
	@python -c "import argparse; print('✅ argparse module available')"
	@echo "✅ All required dependencies available"

# Building and deployment
build: clean
	@echo "📦 Building distribution packages..."
	python setup.py sdist bdist_wheel
	@echo "✅ Build complete"
	@echo "📄 Generated files:"
	@ls -la dist/

check: build
	@echo "🔍 Checking package integrity..."
	@if command -v twine >/dev/null 2>&1; then \
		twine check dist/*; \
		echo "✅ Package check complete"; \
	else \
		echo "ℹ️  twine not installed. Install with: pip install twine"; \
	fi

deploy-test: check
	@echo "🚀 Deploying to Test PyPI..."
	@if command -v twine >/dev/null 2>&1; then \
		twine upload --repository testpypi dist/*; \
		echo "✅ Deployed to Test PyPI"; \
		echo "🔧 Test installation: pip install -i https://test.pypi.org/simple/ json-prompt-formatter"; \
	else \
		echo "❌ twine not installed. Install with: pip install twine"; \
	fi

deploy: check
	@echo "🚀 Deploying to PyPI..."
	@read -p "Are you sure you want to deploy to production PyPI? (y/N): " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		if command -v twine >/dev/null 2>&1; then \
			twine upload dist/*; \
			echo "✅ Deployed to PyPI"; \
			echo "🔧 Installation: pip install json-prompt-formatter"; \
		else \
			echo "❌ twine not installed. Install with: pip install twine"; \
		fi \
	else \
		echo "Deployment cancelled"; \
	fi

# Examples and demo
demo:
	@echo "🎯 Running interactive demo..."
	python examples/demo.py

examples:
	@echo "📝 Generating example outputs..."
	@mkdir -p outputs
	@echo "Generating copywriter examples..."
	python formatter.py -p examples/simple_prompts.txt -t templates/copywriter_template.json -o outputs/copywriter_examples
	@echo "Generating designer examples..."
	python formatter.py -p examples/simple_prompts.txt -t templates/designer_template.json -o outputs/designer_examples
	@echo "Generating OpenAI examples..."
	python formatter.py -p examples/simple_prompts.txt -t templates/openai_template.json -o outputs/openai_examples
	@echo "✅ Example outputs generated in outputs/ directory"

quick-test:
	@echo "⚡ Running quick functionality test..."
	@mkdir -p outputs
	python formatter.py -p examples/simple_prompts.txt -t examples/custom_template.json -o outputs/quick_test
	@if [ -f "outputs/quick_test.json" ] && [ -f "outputs/quick_test.jsonl" ]; then \
		echo "✅ Quick test passed - both JSON and JSONL files created"; \
		echo "📄 JSON file: $$(wc -l < outputs/quick_test.json) lines"; \
		echo "📄 JSONL file: $$(wc -l < outputs/quick_test.jsonl) lines"; \
	else \
		echo "❌ Quick test failed - output files not created"; \
		exit 1; \
	fi

# Comprehensive workflow commands
dev-setup: install check-deps
	@echo "🔧 Development environment setup complete"
	@echo "Next steps:"
	@echo "  make demo     # Run interactive demo"
	@echo "  make examples # Generate examples"
	@echo "  make test     # Run tests"

full-test: clean install test examples quick-test
	@echo "🎉 Full test suite completed successfully"

release-prep: clean format lint test build check
	@echo "🚀 Release preparation complete"
	@echo "Ready for deployment:"
	@echo "  make deploy-test  # Deploy to Test PyPI"
	@echo "  make deploy       # Deploy to production PyPI"

# Version management
version:
	@echo "📋 Current version information:"
	@python setup.py --version
	@echo "Git tags:"
	@git tag -l | tail -5 || echo "No git tags found"

# Documentation
docs:
	@echo "📚 Opening documentation..."
	@if command -v open >/dev/null 2>&1; then \
		open README.md; \
	elif command -v xdg-open >/dev/null 2>&1; then \
		xdg-open README.md; \
	else \
		echo "📖 View README.md in your editor"; \
	fi