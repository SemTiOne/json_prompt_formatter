#!/usr/bin/env python3

import argparse
import sys
import os
from pathlib import Path
import subprocess
import json

def run_formatter(prompt_file, template_file, output_file):
    """Run the existing formatter.py with given parameters."""
    cmd = [
        sys.executable, 
        "formatter.py", 
        "-p", prompt_file,
        "-t", template_file,
        "-o", output_file
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def create_temp_prompt_file(prompt_text):
    """Create a temporary prompt file."""
    temp_file = Path("temp_prompt.txt")
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(prompt_text)
    return str(temp_file)

def main():
    parser = argparse.ArgumentParser(
        prog='json-prompt-formatter',
        description='CLI wrapper for JSON Prompt Formatter'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Format command
    format_parser = subparsers.add_parser('format', help='Format a single prompt')
    format_parser.add_argument('prompt', help='Prompt text to format')
    format_parser.add_argument('-t', '--template', default='openai', 
                              help='Template name (default: openai)')
    format_parser.add_argument('-o', '--output', help='Output file')
    
    # File command  
    file_parser = subparsers.add_parser('file', help='Format from file')
    file_parser.add_argument('input', help='Input prompt file')
    file_parser.add_argument('-t', '--template', default='openai')
    file_parser.add_argument('-o', '--output', help='Output file')
    
    # Templates command
    subparsers.add_parser('templates', help='List available templates')
    
    # Examples command
    subparsers.add_parser('examples', help='Show examples')
    
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    args = parser.parse_args()
    
    if args.command == 'format':
        # Create temp prompt file
        temp_prompt = create_temp_prompt_file(args.prompt)
        
        # Get template path
        template_path = f"templates/{args.template}_template.json"
        if not Path(template_path).exists():
            print(f"❌ Template not found: {template_path}")
            print("Available templates:")
            for t in Path("templates").glob("*_template.json"):
                name = t.stem.replace("_template", "")
                print(f"  • {name}")
            return
        
        # Set output base name (without extension)
        if args.output:
            output_base = Path(args.output).stem  # Remove any extension the user provided
        else:
            output_base = "formatted_output"
        
        # Run formatter
        success, message = run_formatter(temp_prompt, template_path, f"outputs/{output_base}")
        
        if success:
            print(f"✅ Formatted successfully!")
            
            # Show output or save to file
            json_file = f"outputs/{output_base}.json"
            if Path(json_file).exists():
                if args.output:
                    # Copy to specified output with correct extension
                    import shutil
                    output_file = args.output if args.output.endswith('.json') else f"{args.output}.json"
                    shutil.copy(json_file, output_file)
                    print(f"📄 Saved to: {output_file}")
                else:
                    # Print to stdout
                    with open(json_file, 'r') as f:
                        print(f.read())
        else:
            print(f"❌ Error: {message}")
        
        # Clean up temp file
        Path(temp_prompt).unlink(missing_ok=True)
    
    elif args.command == 'file':
        if not Path(args.input).exists():
            print(f"❌ Input file not found: {args.input}")
            return
        
        template_path = f"templates/{args.template}_template.json"
        if not Path(template_path).exists():
            print(f"❌ Template not found: {template_path}")
            return
        
        # Get the base name without extension for internal processing
        if args.output:
            output_base = Path(args.output).stem  # Remove any extension the user provided
        else:
            output_base = Path(args.input).stem
        
        success, message = run_formatter(args.input, template_path, f"outputs/{output_base}")
        
        if success:
            print(f"✅ File processed successfully!")
            if args.output:
                import shutil
                source_file = f"outputs/{output_base}.json"
                # Make sure output has .json extension
                output_file = args.output if args.output.endswith('.json') else f"{args.output}.json"
                shutil.copy(source_file, output_file)
                print(f"📄 Saved to: {args.output}")
        else:
            print(f"❌ Error: {message}")
    
    elif args.command == 'templates':
        print("📋 Available templates:")
        templates_dir = Path("templates")
        if templates_dir.exists():
            for template_file in templates_dir.glob("*_template.json"):
                name = template_file.stem.replace("_template", "")
                print(f"  • {name}")
        else:
            print("❌ Templates directory not found")
    
    elif args.command == 'examples':
        print("""
🎯 Usage Examples:

Format a single prompt:
  json-prompt-formatter format "Create a marketing campaign for eco-friendly products" -t marketer

Process a file:
  json-prompt-formatter file prompts/branding_prompts.txt -t copywriter -o my_output.json

List available templates:
  json-prompt-formatter templates

Using with your existing Makefile:
  make install          # Install the CLI
  make demo            # Run interactive demo
  make examples        # Generate example outputs
  make quick-test      # Test functionality
        """)

if __name__ == '__main__':
    main()