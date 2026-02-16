#!/usr/bin/env python3

"""
Deployment script for JSON Prompt Formatter
Automates building, testing, and publishing to PyPI
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path
import argparse


def run_command(command, check=True, cwd=None):
    """Run a shell command and return the result."""
    print(f"🔄 Running: {command}")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=check, 
            capture_output=True, 
            text=True,
            cwd=cwd
        )
        if result.stdout:
            print(f"✅ Output: {result.stdout.strip()}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"❌ Error output: {e.stderr.strip()}")
        return None


def clean_build_artifacts():
    """Clean up build artifacts and cache files."""
    print("🧹 Cleaning build artifacts...")
    
    directories_to_clean = [
        "build/",
        "dist/", 
        "*.egg-info/",
        "__pycache__/",
        ".pytest_cache/",
        ".coverage"
    ]
    
    for pattern in directories_to_clean:
        for path in Path(".").glob(pattern):
            if path.is_dir():
                print(f"   Removing directory: {path}")
                shutil.rmtree(path, ignore_errors=True)
            elif path.is_file():
                print(f"   Removing file: {path}")
                path.unlink(missing_ok=True)
    
    print("✅ Build artifacts cleaned")


def check_requirements():
    """Check if required tools are installed."""
    print("🔍 Checking requirements...")
    
    required_tools = {
        "python": "python --version",
        "pip": "pip --version", 
        "setuptools": "python -c 'import setuptools; print(setuptools.__version__)'",
        "wheel": "python -c 'import wheel; print(wheel.__version__)'",
        "twine": "twine --version"
    }
    
    missing_tools = []
    
    for tool, command in required_tools.items():
        result = run_command(command, check=False)
        if result and result.returncode == 0:
            print(f"   ✅ {tool}: Available")
        else:
            print(f"   ❌ {tool}: Missing")
            missing_tools.append(tool)
    
    if missing_tools:
        print(f"\n❌ Missing required tools: {', '.join(missing_tools)}")
        print("Install missing tools:")
        if "wheel" in missing_tools or "twine" in missing_tools:
            print("   pip install wheel twine")
        return False
    
    print("✅ All requirements satisfied")
    return True


def run_tests():
    """Run tests if available."""
    print("🧪 Running tests...")
    
    if Path("tests").exists():
        result = run_command("python -m pytest tests/ -v", check=False)
        if result and result.returncode == 0:
            print("✅ All tests passed")
            return True
        else:
            print("❌ Some tests failed")
            return False
    else:
        print("ℹ️  No tests directory found, skipping tests")
        return True


def validate_package():
    """Validate the package structure and metadata."""
    print("📋 Validating package...")
    
    required_files = [
        "setup.py",
        "README.md", 
        "LICENSE",
        "requirements.txt",
        "formatter.py",
        "json_to_jsonl.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    # Check if version is set in setup.py
    with open("setup.py", "r") as f:
        content = f.read()
        if 'version="0.0.0"' in content or 'version=""' in content:
            print("❌ Please set a proper version in setup.py")
            return False
        
        if 'author="Your Name"' in content:
            print("⚠️  Warning: Update author information in setup.py")
        
        if 'your.email@example.com' in content:
            print("⚠️  Warning: Update email in setup.py")
    
    print("✅ Package structure validated")
    return True


def build_package():
    """Build the distribution packages."""
    print("📦 Building package...")
    
    # Build source distribution and wheel
    result = run_command("python setup.py sdist bdist_wheel")
    if not result:
        return False
    
    # Check if files were created
    dist_files = list(Path("dist").glob("*"))
    if not dist_files:
        print("❌ No distribution files created")
        return False
    
    print(f"✅ Built {len(dist_files)} distribution files:")
    for file in dist_files:
        print(f"   📄 {file}")
    
    return True


def check_package():
    """Check the built package with twine."""
    print("🔍 Checking package with twine...")
    
    result = run_command("twine check dist/*")
    if not result:
        return False
    
    print("✅ Package checks passed")
    return True


def publish_to_pypi(test=True):
    """Publish package to PyPI."""
    if test:
        print("🚀 Publishing to Test PyPI...")
        repository = "--repository testpypi"
        url = "https://test.pypi.org/project/json-prompt-formatter/"
    else:
        print("🚀 Publishing to PyPI...")
        repository = ""
        url = "https://pypi.org/project/json-prompt-formatter/"
    
    command = f"twine upload {repository} dist/*"
    result = run_command(command)
    
    if result:
        print(f"✅ Successfully published to {'Test ' if test else ''}PyPI!")
        print(f"📦 Package URL: {url}")
        if test:
            print("🔧 To install from Test PyPI:")
            print("   pip install -i https://test.pypi.org/simple/ json-prompt-formatter")
        else:
            print("🔧 To install:")
            print("   pip install json-prompt-formatter")
        return True
    
    return False


def create_git_tag(version):
    """Create a git tag for the release."""
    print(f"🏷️  Creating git tag v{version}...")
    
    # Check if we're in a git repository
    if not Path(".git").exists():
        print("ℹ️  Not a git repository, skipping tag creation")
        return True
    
    # Create and push tag
    commands = [
        f"git tag v{version}",
        f"git push origin v{version}"
    ]
    
    for command in commands:
        result = run_command(command, check=False)
        if not result:
            print(f"⚠️  Failed to execute: {command}")
            return False
    
    print(f"✅ Created and pushed tag v{version}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Deploy JSON Prompt Formatter")
    parser.add_argument("--test", action="store_true", help="Deploy to Test PyPI instead of PyPI")
    parser.add_argument("--skip-tests", action="store_true", help="Skip running tests")
    parser.add_argument("--skip-clean", action="store_true", help="Skip cleaning build artifacts")
    parser.add_argument("--version", help="Version for git tag")
    
    args = parser.parse_args()
    
    print("🚀 JSON Prompt Formatter Deployment Script")
    print("=" * 50)
    
    # Step 1: Clean build artifacts
    if not args.skip_clean:
        clean_build_artifacts()
    
    # Step 2: Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Step 3: Validate package
    if not validate_package():
        sys.exit(1)
    
    # Step 4: Run tests
    if not args.skip_tests:
        if not run_tests():
            response = input("Tests failed. Continue anyway? (y/N): ")
            if response.lower() != 'y':
                sys.exit(1)
    
    # Step 5: Build package
    if not build_package():
        sys.exit(1)
    
    # Step 6: Check package
    if not check_package():
        sys.exit(1)
    
    # Step 7: Confirm publication
    target = "Test PyPI" if args.test else "PyPI"
    response = input(f"Ready to publish to {target}. Continue? (y/N): ")
    if response.lower() != 'y':
        print("Deployment cancelled")
        sys.exit(0)
    
    # Step 8: Publish
    if not publish_to_pypi(test=args.test):
        sys.exit(1)
    
    # Step 9: Create git tag (only for production releases)
    if not args.test and args.version:
        create_git_tag(args.version)
    
    print("\n🎉 Deployment completed successfully!")
    print("Next steps:")
    print("1. Test the installation from PyPI")
    print("2. Update documentation if needed")
    print("3. Announce the release")


if __name__ == "__main__":
    main()
