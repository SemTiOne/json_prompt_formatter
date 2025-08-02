#!/usr/bin/env python3

from setuptools import setup
import os

# Read README for long description
def read_readme():
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return "JSON Prompt Formatter - CLI tool for formatting prompts using JSON templates"

# Read requirements
def read_requirements():
    try:
        with open("requirements.txt", "r", encoding="utf-8") as fh:
            return [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        return []

setup(
    name="json-prompt-formatter",
    version="1.0.0",
    author="SemTiOne",
    author_email="emphyst80@gmail.com",
    description="CLI tool for formatting prompts using JSON templates for different use cases",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/SemTiOne/json_prompt_formatter",
    project_urls={
        "Bug Tracker": "https://github.com/SemTiOne/json_prompt_formatter/issues",
        "Documentation": "https://github.com/SemTiOne/json_prompt_formatter#readme",
        "Source Code": "https://github.com/SemTiOne/json_prompt_formatter",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: JSON",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    # Use py_modules for individual .py files in root directory
    py_modules=["cli", "formatter", "json_to_jsonl"],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
            "build>=0.7",
            "twine>=3.0",
        ],
    },
    # Point directly to the cli.py file and its main function
    entry_points={
        "console_scripts": [
            "json-prompt-formatter=cli:main",
            "jpf=cli:main",
        ],
    },
    # Include data files
    data_files=[
        ("templates", ["templates/openai_template.json", 
                      "templates/copywriter_template.json",
                      "templates/designer_template.json", 
                      "templates/marketer_template.json",
                      "templates/founder_template.json",
                      "templates/product_designer_template.json",
                      "templates/prompt_engineer_template.json"]),
        ("prompts", ["prompts/branding_prompts.txt"]),
    ],
    include_package_data=True,
    keywords=[
        "prompt-engineering",
        "json",
        "cli",
        "ai",
        "chatgpt",
        "openai",
        "formatting",
        "templates",
        "automation",
        "prompt-templates",
        "developer-tools",
    ],
    zip_safe=False,
)