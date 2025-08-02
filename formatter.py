import argparse
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
import sys


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def read_prompts(prompt_file: str) -> List[str]:
    """Read prompts from a .txt file, one per line."""
    prompt_path = Path(prompt_file)
    
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
    
    try:
        with open(prompt_path, 'r', encoding='utf-8') as file:
            prompts = [line.strip() for line in file if line.strip()]
        
        if not prompts:
            raise ValueError(f"No valid prompts found in {prompt_file}")
        
        logger.info(f"Read {len(prompts)} prompts from {prompt_file}")
        return prompts
    
    except Exception as e:
        raise RuntimeError(f"Error reading prompts from {prompt_file}: {e}")


def read_template(template_file: str) -> Dict[str, Any]:
    """Read the JSON template file."""
    template_path = Path(template_file)
    
    if not template_path.exists():
        raise FileNotFoundError(f"Template file not found: {template_file}")
    
    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            template = json.load(file)
        
        logger.info(f"Loaded template from {template_file}")
        return template
    
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in template file {template_file}: {e}")
    except Exception as e:
        raise RuntimeError(f"Error reading template from {template_file}: {e}")


def replace_placeholder_in_value(value: Any, placeholder: str, replacement: str) -> Any:
    """Recursively replace placeholder in any value (string, dict, list, etc.)."""
    if isinstance(value, str):
        return value.replace(placeholder, replacement)
    elif isinstance(value, dict):
        return {k: replace_placeholder_in_value(v, placeholder, replacement) for k, v in value.items()}
    elif isinstance(value, list):
        return [replace_placeholder_in_value(item, placeholder, replacement) for item in value]
    else:
        return value


def format_prompts(prompts: List[str], template: Dict[str, Any], placeholder: str) -> List[Dict[str, Any]]:
    """Replace the placeholder in the template with each prompt."""
    formatted = []
    
    for i, prompt in enumerate(prompts, 1):
        try:
            # Deep copy and replace placeholders recursively
            formatted_item = replace_placeholder_in_value(template, placeholder, prompt)
            formatted.append(formatted_item)
            
        except Exception as e:
            logger.warning(f"Error formatting prompt {i}: {e}")
            continue
    
    logger.info(f"Successfully formatted {len(formatted)} prompts")
    return formatted


def save_json(data: List[Dict[str, Any]], output_file: str) -> None:
    """Save the list of formatted prompts as a JSON file."""
    output_path = Path(output_file)
    
    try:
        # Create parent directories if they don't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        
        logger.info(f"Saved JSON output to {output_file}")
    
    except Exception as e:
        raise RuntimeError(f"Error saving JSON to {output_file}: {e}")


def save_jsonl(data: List[Dict[str, Any]], output_file: str) -> None:
    """Save the list of formatted prompts as a JSONL file."""
    output_path = Path(output_file)
    
    try:
        # Create parent directories if they don't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as file:
            for item in data:
                json.dump(item, file, ensure_ascii=False)
                file.write('\n')
        
        logger.info(f"Saved JSONL output to {output_file}")
    
    except Exception as e:
        raise RuntimeError(f"Error saving JSONL to {output_file}: {e}")


def parse_output_path(output_arg: str) -> tuple[str, str]:
    """Parse the output argument to extract directory and base name."""
    if not output_arg:
        return "", ""
    
    output_path = Path(output_arg)
    
    # If the output_arg contains a directory path, extract it
    if len(output_path.parts) > 1:
        output_dir = str(output_path.parent)
        base_name = output_path.stem  # Get name without extension
    else:
        output_dir = ""
        # Remove any extension from the base name
        base_name = Path(output_arg).stem
    
    return output_dir, base_name


def generate_output_filenames(base_name: str, prompts_file: str, template_file: str) -> tuple[str, str]:
    """Generate output filenames based on input files."""
    prompts_stem = Path(prompts_file).stem
    template_stem = Path(template_file).stem.replace('_template', '').replace(' template', '')
    
    if base_name:
        json_file = f"{base_name}.json"
        jsonl_file = f"{base_name}.jsonl"
    else:
        json_file = f"formatted_{prompts_stem}_{template_stem}.json"
        jsonl_file = f"formatted_{prompts_stem}_{template_stem}.jsonl"
    
    return json_file, jsonl_file


def validate_template_has_placeholder(template: Dict[str, Any], placeholder: str) -> bool:
    """Check if the template contains the placeholder."""
    template_str = json.dumps(template)
    return placeholder in template_str


def main():
    parser = argparse.ArgumentParser(
        description="Format prompts using a JSON template and output both JSON and JSONL formats.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -p prompts/branding_prompts.txt -t templates/copywriter_template.json -o formatted_copywriter
  %(prog)s -p prompts/branding_prompts.txt -t templates/openai_template.json --placeholder "{{PROMPT}}"
  %(prog)s -p prompts/branding_prompts.txt -t templates/founder_template.json --json-only
        """
    )
    
    parser.add_argument(
        "--prompt", "-p", 
        required=True, 
        help="Path to prompt .txt file"
    )
    parser.add_argument(
        "--template", "-t", 
        required=True, 
        help="Path to template .json file"
    )
    parser.add_argument(
        "--output", "-o", 
        help="Base name for output files (without extension). If not provided, auto-generated from input filenames"
    )
    parser.add_argument(
        "--placeholder", 
        default="{{prompt}}", 
        help="Placeholder to replace in the template (default: %(default)s)"
    )
    parser.add_argument(
        "--json-only", 
        action="store_true", 
        help="Only output JSON format (skip JSONL)"
    )
    parser.add_argument(
        "--jsonl-only", 
        action="store_true", 
        help="Only output JSONL format (skip JSON)"
    )
    parser.add_argument(
        "--output-dir", 
        default="outputs", 
        help="Output directory (default: %(default)s)"
    )
    parser.add_argument(
        "--verbose", "-v", 
        action="store_true", 
        help="Enable verbose logging"
    )

    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Validate conflicting arguments
    if args.json_only and args.jsonl_only:
        logger.error("Cannot specify both --json-only and --jsonl-only")
        sys.exit(1)
    
    try:
        # Read input files
        prompts = read_prompts(args.prompt)
        template = read_template(args.template)
        
        # Validate template contains placeholder
        if not validate_template_has_placeholder(template, args.placeholder):
            logger.warning(f"Template does not contain placeholder '{args.placeholder}'. "
                         f"Prompts will not be substituted.")
        
        # Format prompts
        formatted = format_prompts(prompts, template, args.placeholder)
        
        if not formatted:
            logger.error("No prompts were successfully formatted")
            sys.exit(1)
        
        # Parse output path to handle directory and base name
        custom_output_dir, base_name = parse_output_path(args.output)
        
        # Use custom output directory if provided, otherwise use default
        if custom_output_dir:
            output_dir = Path(custom_output_dir)
        else:
            output_dir = Path(args.output_dir)
        
        # Ensure output directory exists
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate output filenames
        json_file, jsonl_file = generate_output_filenames(base_name, args.prompt, args.template)
        
        # Create full paths
        json_path = output_dir / json_file
        jsonl_path = output_dir / jsonl_file
        
        # Save files based on arguments
        files_created = []
        
        if not args.jsonl_only:
            save_json(formatted, str(json_path))
            files_created.append(str(json_path))
        
        if not args.json_only:
            save_jsonl(formatted, str(jsonl_path))
            files_created.append(str(jsonl_path))
        
        # Success message
        print(f"Successfully formatted {len(formatted)} prompts")
        print(f"Created files: {', '.join(files_created)}")
    
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()