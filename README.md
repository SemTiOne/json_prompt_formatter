# 🚀 JSON Prompt Formatter

A professional CLI and Python tool for converting text prompts into structured JSON/JSONL formats using customizable templates. Perfect for AI/ML workflows, API integrations, and batch processing of prompts.

## ✨ Features

- **🖥️ CLI Interface**: Easy-to-use command-line interface for developers
- **🔄 Batch Processing**: Convert multiple prompts at once
- **📋 Multiple Templates**: 7 professional templates included
- **🎯 Custom Placeholders**: Use any placeholder format
- **📁 Dual Output**: Generate both JSON and JSONL formats
- **⚡ Fast Processing**: Handle 1000+ prompts efficiently
- **🛡️ Error Handling**: Comprehensive validation and error reporting
- **🌍 Unicode Support**: Full support for international characters
- **📦 PyPI Package**: Install globally with pip

## 📦 Installation

### Option 1: Install from PyPI (Recommended)
```bash
pip install json-prompt-formatter
```

### Option 2: Install from Source
```bash
# Clone the repository
git clone https://github.com/SemTiOne/json_prompt_formatter.git
cd json_prompt_formatter

# Install in development mode
pip install -e .
```

### Requirements
- Python 3.8+
- No external dependencies required

## 🚀 Quick Start

### CLI Usage (New!)
```bash
# Format a single prompt
json-prompt-formatter format "Create a marketing campaign for sustainable fashion" -t marketer

# Process a file
json-prompt-formatter file prompts/branding_prompts.txt -t copywriter -o my_output.json

# List available templates
json-prompt-formatter templates

# Show usage examples
json-prompt-formatter examples

# Short alias also works
jpf format "Design a minimalist logo" -t designer
```

### Python Script Usage (Original)
```bash
python formatter.py -p prompts/branding_prompts.txt -t templates/openai_template.json -o my_formatted_prompts
```

## 🎯 CLI Commands

### Core Commands

**Format a single prompt:**
```bash
json-prompt-formatter format "Your prompt text here" -t template_name [-o output_file]
```

**Process a file:**
```bash
json-prompt-formatter file input_file.txt -t template_name [-o output_file]
```

**Batch process directory:**
```bash
json-prompt-formatter batch ./input_dir ./output_dir -t template_name
```

**List available templates:**
```bash
json-prompt-formatter templates
```

**Show examples:**
```bash
json-prompt-formatter examples
```

### CLI Examples

```bash
# Single prompt formatting
json-prompt-formatter format "Create a tagline for an AI startup" -t marketer

# File processing with output
json-prompt-formatter file prompts/marketing.txt -t copywriter -o campaign_prompts.json

# Batch processing
json-prompt-formatter batch ./prompts ./outputs -t designer

# Using short alias
jpf format "Design a mobile app interface" -t product_designer -o design_brief.json
```

## 📋 Available Templates

**OpenAI Template** (`openai`) - Complete branding analysis with structured JSON response for OpenAI ChatGPT API integration.

**Copywriter Template** (`copywriter`) - Professional copywriting prompts optimized for marketing and advertising content creation.

**Designer Template** (`designer`) - Design-focused prompt structure for visual identity, branding, and creative design work.

**Marketer Template** (`marketer`) - Marketing campaign and strategy prompts for comprehensive marketing planning and execution.

**Founder Template** (`founder`) - Business strategy and startup prompts tailored for entrepreneurship and business development.

**Product Designer Template** (`product_designer`) - UX/UI and product development prompts focused on user experience and interface design.

**Prompt Engineer Template** (`prompt_engineer`) - Advanced prompt optimization and engineering for sophisticated AI interactions.

## 🔧 Development Commands (Makefile)

```bash
# Development setup
make install          # Install package in development mode
make clean           # Clean build artifacts
make test            # Run tests

# Examples and demo
make demo            # Run interactive demo
make examples        # Generate example outputs
make quick-test      # Quick functionality test

# Building and deployment
make build           # Build distribution packages
make deploy-test     # Deploy to Test PyPI
make deploy          # Deploy to PyPI (production)
```

## 📊 Input/Output Examples

### Input Example (`prompts/sample.txt`)
```
Create a tagline for a tech startup
Write a product description for smart headphones
Develop a brand story for an eco-friendly company
```

### CLI Command
```bash
json-prompt-formatter file prompts/sample.txt -t openai -o branded_prompts.json
```

### Output Example (`branded_prompts.json`)
```json
[
  {
    "model": "gpt-4o",
    "temperature": 0.7,
    "max_tokens": 1500,
    "response_format": { "type": "json_object" },
    "messages": [
      {
        "role": "system",
        "content": "You are a world-class branding expert with 15+ years of experience..."
      },
      {
        "role": "user", 
        "content": "Create a tagline for a tech startup\n\nPlease respond with a comprehensive branding analysis..."
      }
    ],
    "metadata": {
      "template_version": "2.0",
      "category": "branding",
      "api_provider": "openai",
      "tags": ["openai", "api", "branding", "structured-output"]
    }
  }
]
```

## 🎯 Advanced Usage

### Python Script Usage
```bash
# Basic formatting
python formatter.py -p prompts/branding_prompts.txt -t templates/copywriter_template.json -o copywriter_prompts

# Custom output directory
python formatter.py -p prompts/my_prompts.txt -t templates/openai_template.json --output-dir results -o formatted_data

# Custom placeholder
python formatter.py -p prompts/my_prompts.txt -t templates/custom_template.json -o custom_output --placeholder "{{CUSTOM_PROMPT}}"

# Verbose logging
python formatter.py -p prompts/my_prompts.txt -t templates/openai_template.json -o debug_output --verbose
```

### Batch Processing All Templates
```bash
# CLI approach
for template in openai copywriter designer marketer founder product_designer prompt_engineer; do
    json-prompt-formatter file prompts/branding_prompts.txt -t "$template" -o "output_$template.json"
done

# Python script approach
for template in templates/*.json; do
    template_name=$(basename "$template" .json)
    python formatter.py -p prompts/branding_prompts.txt -t "$template" -o "output_$template_name"
done
```

## 📁 Project Structure

```
json_prompt_formatter/
├── 📄 README.md                        # This file
├── 📄 LICENSE                          # MIT license
├── 📄 CONTRIBUTING.md                  # Contribution guidelines
├── 📄 CHANGELOG.md                     # Version history
├── 📄 setup.py                         # Package configuration
├── 📄 requirements.txt                 # Dependencies
├── 📄 Makefile                         # Dev commands
├── 📄 .gitignore                       # Git exclusions
├── 📄 MANIFEST.in                      # Package files
├── 📄 package.json                     # Node.js package config
├── 🐍 __main__.py                      # Main entry point
├── 🐍 formatter.py                     # Main formatting tool
├── 🐍 json_to_jsonl.py                 # Format converter
├── 🐍 deploy.py                        # Deployment script
├── 📁 templates/                       # 7 professional templates
│   ├── openai_template.json            # OpenAI API with branding expertise
│   ├── copywriter_template.json        # Marketing copywriting
│   ├── designer_template.json          # Design & visual identity
│   ├── marketer_template.json          # Marketing strategy
│   ├── founder_template.json           # Entrepreneurship & business
│   ├── product_designer_template.json  # Product design & UX/UI
│   └── prompt_engineer_template.json   # Advanced prompt engineering
├── 📁 prompts/                         # Sample prompt collections
│   └── branding_prompts.txt            # 75+ branding prompts
├── 📁 examples/                        # Usage examples & demos
└── 📁 outputs/                         # Generated files (created automatically)
```

## ⚙️ CLI Options

```bash
json-prompt-formatter [COMMAND] [OPTIONS]

Commands:
  format      Format a single prompt
  file        Process prompts from a file
  batch       Process multiple files in a directory
  templates   List available templates
  examples    Show usage examples

Global Options:
  --help      Show help message
  --version   Show version information

Format/File Options:
  -t, --template NAME    Template to use (default: openai)
  -o, --output FILE      Output file path
```

## ⚙️ Python Script Options

```bash
python formatter.py [OPTIONS]

Required Arguments:
  -p, --prompt PATH          Path to prompt .txt file
  -t, --template PATH        Path to template .json file

Optional Arguments:
  -o, --output NAME          Base name for output files
  --output-dir DIR           Output directory (default: outputs)
  --placeholder TEXT         Placeholder to replace (default: {{prompt}})
  --json-only               Only generate JSON format
  --jsonl-only              Only generate JSONL format  
  --verbose, -v             Enable verbose logging
```

## 🔧 Creating Custom Templates

### Template Structure
```json
{
  "messages": [
    {
      "role": "user",
      "content": "{{prompt}}"
    }
  ],
  "temperature": 0.7,
  "max_tokens": 1000
}
```

### Using Custom Templates with CLI
```bash
# Place your template in templates/ directory as my_template.json
json-prompt-formatter format "Test prompt" -t my_template

# Or use full path with Python script
python formatter.py -p prompts.txt -t path/to/custom_template.json -o output
```

## 📊 Performance

- **Speed**: Processes 1000+ prompts in under 10 seconds
- **Memory**: Efficient memory usage for large datasets
- **Scalability**: Tested with 10,000+ prompts
- **Cross-platform**: Works on Windows, macOS, and Linux

## 🐛 Troubleshooting

### CLI Issues

**Command not found:**
```bash
# Reinstall the package
pip uninstall json-prompt-formatter
pip install json-prompt-formatter

# Or use Python directly
python cli.py format "test prompt" -t openai
```

**Template not found:**
```bash
# List available templates
json-prompt-formatter templates

# Use correct template name
json-prompt-formatter format "prompt" -t copywriter  # Not copywriter_template
```

### Common Issues

**Invalid JSON Template Error**
- Check your template JSON syntax at [jsonlint.com](https://jsonlint.com/)

**File Not Found Error**
- Verify file paths are correct
- Use forward slashes or escaped backslashes on Windows

**Unicode Encoding Issues (Windows)**
```bash
chcp 65001
json-prompt-formatter format "prompt with émojis 🚀" -t openai
```

## 🚀 Publishing to PyPI

This package is available on PyPI! To publish updates:

```bash
# Test deployment
make deploy-test

# Production deployment
make deploy
```

## 🤝 Contributing

We welcome contributions! Quick steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with both CLI and Python script
5. Submit a pull request

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

- Built for the AI/ML developer community
- Designed for both CLI and programmatic usage
- Optimized for modern prompt engineering workflows

## 📈 Roadmap

- [x] CLI interface for developers
- [x] PyPI package distribution
- [ ] GUI interface
- [ ] Template validation tool
- [ ] Cloud storage integration
- [ ] Docker containerization
- [ ] Plugin system for custom processors

---

## 💡 Use Cases

### For Developers
```bash
# Quick prompt formatting in development
jpf format "Debug this React component" -t prompt_engineer

# Batch process training data
jpf batch ./training_prompts ./formatted_data -t openai

# CI/CD integration
json-prompt-formatter file prompts.txt -t api_template -o deployment_ready.json
```

### For Content Teams
```bash
# Marketing campaign development
jpf file marketing_briefs.txt -t marketer -o campaign_prompts.json

# Design brief generation
jpf format "Design a modern dashboard" -t designer -o design_brief.json
```

### For Researchers
```bash
# Experiment preparation
jpf batch ./research_prompts ./experiments -t openai

# Evaluation dataset creation
python formatter.py -p evaluation_set.txt -t research_template.json -o eval_data
```

---

**⭐ Star this repository if you find it helpful!**

**🐦 Follow [@SemTiOne](https://github.com/SemTiOne) for updates**

For questions or issues, please [open an issue](https://github.com/SemTiOne/json_prompt_formatter/issues).