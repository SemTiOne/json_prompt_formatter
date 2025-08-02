# Contributing to JSON Prompt Formatter

Thank you for your interest in contributing to JSON Prompt Formatter! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Types of Contributions Welcome

- **Bug Reports**: Found a bug? Let us know!
- **Feature Requests**: Have an idea for improvement?
- **Code Contributions**: Bug fixes, new features, performance improvements
- **Documentation**: Improve docs, add examples, write tutorials
- **Templates**: Create new specialized templates
- **Testing**: Add tests, improve test coverage

## 🚀 Getting Started

### 1. Development Environment Setup

```bash
# Clone the repository
git clone https://github.com/SemTiOne/json_prompt_formatter.git
cd json_prompt_formatter

# Set up development environment
make dev-setup

# Or manually:
pip install -e .
```

### 2. Understanding the Codebase

**Core Files:**
- `formatter.py` - Main formatting logic
- `json_to_jsonl.py` - JSON to JSONL conversion utility
- `templates/` - Template collection
- `prompts/` - Example prompts

**Key Functions:**
- `format_prompts()` - Core formatting functionality
- `read_template()` - Template loading and validation
- `save_json()`/`save_jsonl()` - Output generation

### 3. Running Tests and Examples

```bash
# Run quick functionality test
make quick-test

# Generate examples
make examples

# Run interactive demo
make demo

# Run full test suite
make full-test
```

## 📝 Contribution Guidelines

### Bug Reports

When reporting bugs, please include:

1. **Clear description** of the issue
2. **Steps to reproduce** the problem
3. **Expected vs actual behavior**
4. **Environment details** (Python version, OS)
5. **Sample files** that trigger the bug (if applicable)

**Bug Report Template:**
```markdown
## Bug Description
Brief description of the bug

## Steps to Reproduce
1. Run command: `python formatter.py -p file.txt -t template.json`
2. Expected: Should create JSON file
3. Actual: Error message appears

## Environment
- Python version: 3.9.0
- OS: macOS 12.0
- JSON Prompt Formatter version: 1.0.0

## Additional Context
Any other relevant information
```

### Feature Requests

For feature requests, please describe:

1. **The problem** you're trying to solve
2. **Proposed solution** or feature
3. **Use cases** where this would be helpful
4. **Alternative solutions** you've considered

### Code Contributions

#### Code Style

- **Python Style**: Follow PEP 8 guidelines
- **Line Length**: Maximum 100 characters
- **Imports**: Group standard library, third-party, and local imports
- **Documentation**: Add docstrings for new functions/classes

```python
def example_function(param1: str, param2: int) -> bool:
    """
    Brief description of what the function does.
    
    Args:
        param1: Description of parameter
        param2: Description of parameter
    
    Returns:
        Description of return value
    """
    pass
```

#### Code Quality Tools

```bash
# Format code
make format

# Check code style
make lint

# Check all dependencies
make check-deps
```

#### Testing

- Add tests for new functionality
- Ensure existing tests pass
- Test edge cases and error conditions

```bash
# Run tests
make test

# Test your changes
make quick-test
```

### Template Contributions

#### Creating New Templates

Templates should follow this structure:

```json
{
  "id": "template_name_{{timestamp}}",
  "template_version": "1.0",
  "persona": {
    "role": "Professional Role",
    "expertise": "Area of expertise",
    "experience_level": "Experience level",
    "specializations": ["skill1", "skill2"]
  },
  "system_instruction": "Detailed role description...",
  "task_instruction": "Specific task instructions...",
  "conversation": [
    {
      "role": "system",
      "content": "System prompt..."
    },
    {
      "role": "user", 
      "content": "{{prompt}}"
    }
  ],
  "expected_output": {
    "prompt": "{{prompt}}",
    "analysis": "Analysis structure...",
    "solution": "Solution format..."
  },
  "metadata": {
    "category": "branding",
    "difficulty": "intermediate",
    "estimated_time": "10-15 minutes",
    "tags": ["relevant", "tags"]
  }
}
```

#### Template Quality Standards

- **Clear persona definition** with specific expertise
- **Detailed instructions** for consistent output
- **Structured expected output** with multiple sections
- **Professional metadata** including difficulty and tags
- **Tested with sample prompts** to ensure quality

### Documentation Contributions

#### Areas for Documentation

- **User guides** for specific use cases
- **API documentation** for programmatic usage
- **Tutorial content** for beginners
- **Advanced examples** for power users
- **Integration guides** with other tools

#### Documentation Style

- Use clear, concise language
- Include practical examples
- Provide step-by-step instructions
- Add screenshots/diagrams where helpful

## 🔄 Development Workflow

### 1. Fork and Clone

```bash
# Fork on GitHub, then clone your fork
git clone https://github.com/SemTiOne/json_prompt_formatter.git
cd json_prompt_formatter
```

### 2. Create Feature Branch

```bash
# Create branch for your feature
git checkout -b feature/amazing-new-feature

# Or for bug fixes
git checkout -b fix/bug-description
```

### 3. Make Changes

- Write your code/documentation
- Add tests if applicable
- Update documentation
- Test your changes

### 4. Commit Changes

```bash
# Stage your changes
git add .

# Commit with descriptive message
git commit -m "Add amazing new feature

- Implement feature X
- Add tests for feature X  
- Update documentation"
```

### 5. Submit Pull Request

- Push to your fork
- Create pull request on GitHub
- Describe your changes clearly
- Link any related issues

### Pull Request Guidelines

**Good Pull Request:**
- **Clear title** describing the change
- **Detailed description** of what was changed and why
- **Links to related issues** if applicable
- **Screenshots** for UI changes
- **Testing notes** on how you tested the changes

**Pull Request Template:**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Ran existing tests
- [ ] Added new tests
- [ ] Tested manually

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
```

## 🏗️ Project Structure

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

## 🐛 Common Development Issues

### Issue: Import errors during development
**Solution:** Install in development mode: `pip install -e .`

### Issue: Tests not found
**Solution:** Install pytest: `pip install pytest`

### Issue: Build fails
**Solution:** Clean and rebuild: `make clean && make build`

### Issue: Template validation errors
**Solution:** Check JSON syntax and required placeholders

## 🏆 Recognition

Contributors will be:
- Added to contributors list in README
- Mentioned in release notes
- Given credit in relevant documentation

## 📞 Getting Help

- **Questions**: Open a GitHub Discussion
- **Bugs**: Create an Issue with bug template
- **Features**: Create an Issue with feature template
- **General Chat**: Join our community discussions

## 📜 Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Assume positive intent

### Unacceptable Behavior

- Harassment or discrimination
- Inappropriate or offensive content
- Spam or self-promotion
- Disrupting community discussions

### Enforcement

Violations will result in warnings, temporary bans, or permanent bans depending on severity.

---

Thank you for contributing to JSON Prompt Formatter! Your efforts help make this tool better for everyone. 🎉