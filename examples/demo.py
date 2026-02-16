#!/usr/bin/env python3

"""
Demo script showing how to use JSON Prompt Formatter programmatically
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import our modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from formatter import format_prompts, read_prompts, read_template, save_json, save_jsonl
from formatter import convert_json_to_jsonl


def demo_basic_usage():
    """Demonstrate basic formatting functionality."""
    print("🎯 Demo: Basic Prompt Formatting")
    print("=" * 40)
    
    # Sample prompts
    prompts = [
        "Write a tagline for a coffee shop that emphasizes quality and community.",
        "Create a brand name for a fitness app targeting busy professionals.",
        "Develop a mission statement for a sustainable packaging company."
    ]
    
    # Simple template
    template = {
        "role": "You are a creative branding expert.",
        "instruction": "Provide strategic and creative branding solutions.",
        "prompt": "{{prompt}}",
        "expected_format": {
            "analysis": "Brief analysis of the challenge",
            "solution": "Your creative solution",
            "rationale": "Why this solution works"
        }
    }
    
    # Format prompts
    formatted = format_prompts(prompts, template, "{{prompt}}")
    
    print(f"✅ Formatted {len(formatted)} prompts")
    print("\nSample formatted prompt:")
    print("-" * 30)
    import json
    print(json.dumps(formatted[0], indent=2))
    
    return formatted


def demo_file_operations():
    """Demonstrate file-based operations."""
    print("\n🎯 Demo: File Operations")
    print("=" * 40)
    
    # Create temporary files for demo
    demo_dir = Path("examples/temp_demo")
    demo_dir.mkdir(exist_ok=True)
    
    # Create sample prompt file
    prompt_file = demo_dir / "demo_prompts.txt"
    with open(prompt_file, 'w') as f:
        f.write("Create a catchy slogan for an eco-friendly startup.\n")
        f.write("Design a logo concept for a local bakery.\n")
        f.write("Write a mission statement for a tech nonprofit.\n")
    
    # Create sample template file
    template_file = demo_dir / "demo_template.json"
    template_data = {
        "persona": "Brand Strategist",
        "task": "Analyze and solve the branding challenge",
        "prompt": "{{prompt}}",
        "output": {
            "strategy": "Strategic approach",
            "creative": "Creative solution",
            "implementation": "How to implement"
        }
    }
    
    with open(template_file, 'w') as f:
        import json
        json.dump(template_data, f, indent=2)
    
    # Read and process files
    prompts = read_prompts(str(prompt_file))
    template = read_template(str(template_file))
    formatted = format_prompts(prompts, template, "{{prompt}}")
    
    # Save outputs
    json_output = demo_dir / "output.json"
    jsonl_output = demo_dir / "output.jsonl"
    
    save_json(formatted, str(json_output))
    save_jsonl(formatted, str(jsonl_output))
    
    print(f"✅ Processed {len(prompts)} prompts from file")
    print(f"📄 Created: {json_output}")
    print(f"📄 Created: {jsonl_output}")
    
    # Demo JSON to JSONL conversion
    json_only_file = demo_dir / "json_only.json"
    save_json(formatted, str(json_only_file))
    
    converted_file = convert_json_to_jsonl(str(json_only_file))
    print(f"🔄 Converted: {json_only_file} → {converted_file}")
    
    return demo_dir


def demo_template_variations():
    """Demonstrate different template structures."""
    print("\n🎯 Demo: Template Variations")
    print("=" * 40)
    
    # Different template styles
    templates = {
        "simple": {
            "prompt": "{{prompt}}",
            "response": "Your answer here"
        },
        
        "structured": {
            "task": "{{prompt}}",
            "analysis": {
                "challenge": "What needs to be solved",
                "approach": "How to approach it"
            },
            "solution": {
                "primary": "Main solution",
                "alternatives": "Other options"
            }
        },
        
        "conversation": {
            "messages": [
                {"role": "system", "content": "You are a branding expert."},
                {"role": "user", "content": "{{prompt}}"}
            ]
        }
    }
    
    sample_prompt = "Create a brand identity for a sustainable fashion startup."
    
    for template_name, template in templates.items():
        formatted = format_prompts([sample_prompt], template, "{{prompt}}")
        print(f"\n📋 {template_name.title()} Template Result:")
        print("-" * 30)
        import json
        print(json.dumps(formatted[0], indent=2)[:200] + "...")


def demo_advanced_features():
    """Demonstrate advanced features and customizations."""
    print("\n🎯 Demo: Advanced Features")
    print("=" * 40)
    
    # Custom placeholder
    template_with_custom_placeholder = {
        "brand_challenge": "{{CHALLENGE}}",
        "creative_brief": {
            "objective": "Solve this challenge: {{CHALLENGE}}",
            "approach": "Strategic and creative solution needed"
        }
    }
    
    prompts = ["Develop messaging for a B2B SaaS product"]
    formatted = format_prompts(prompts, template_with_custom_placeholder, "{{CHALLENGE}}")
    
    print("✅ Custom placeholder demo:")
    import json
    print(json.dumps(formatted[0], indent=2))
    
    # Nested placeholder replacement
    complex_template = {
        "project": {
            "brief": "{{prompt}}",
            "requirements": [
                "Address this challenge: {{prompt}}",
                "Provide strategic thinking for: {{prompt}}"
            ],
            "deliverables": {
                "primary": "Solution for {{prompt}}",
                "secondary": "Implementation plan for {{prompt}}"
            }
        }
    }
    
    formatted_complex = format_prompts(prompts, complex_template, "{{prompt}}")
    print("\n✅ Nested replacement demo:")
    print(json.dumps(formatted_complex[0], indent=2))


def cleanup_demo_files(demo_dir):
    """Clean up demo files."""
    if demo_dir.exists():
        import shutil
        shutil.rmtree(demo_dir)
        print(f"\n🧹 Cleaned up demo files: {demo_dir}")


def main():
    """Run all demos."""
    print("🚀 JSON Prompt Formatter - Interactive Demo")
    print("=" * 50)
    
    try:
        # Run demos
        demo_basic_usage()
        demo_dir = demo_file_operations()
        demo_template_variations()
        demo_advanced_features()
        
        print("\n🎉 Demo completed successfully!")
        print("\nTo use the formatter from command line:")
        print("python formatter.py -p prompts/branding_prompts.txt -t templates/copywriter_template.json")
        print("\nTo convert JSON to JSONL:")
        print("python json_to_jsonl.py examples/sample_output.json")
        
        # Ask if user wants to keep demo files
        keep_files = input(f"\nKeep demo files in {demo_dir}? (y/N): ")
        if keep_files.lower() != 'y':
            cleanup_demo_files(demo_dir)
    
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
