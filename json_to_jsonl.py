import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Union


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def validate_json_file(file_path: str) -> None:
    """Validate that the file exists and has a .json extension."""
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if path.suffix.lower() != '.json':
        logger.warning(f"File does not have .json extension: {file_path}")


def load_json_data(input_path: str) -> List[Dict[str, Any]]:
    """Load and validate JSON data from file."""
    try:
        with open(input_path, "r", encoding="utf-8") as infile:
            data = json.load(infile)
        
        logger.info(f"Successfully loaded JSON from {input_path}")
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON in {input_path}: {e}")
    except Exception as e:
        raise RuntimeError(f"Error reading file {input_path}: {e}")
    
    # Validate data structure
    if not isinstance(data, list):
        raise ValueError(f"Input JSON must be a list of objects, got {type(data).__name__}")
    
    if not data:
        raise ValueError("Input JSON list is empty")
    
    # Check if all items are JSON-serializable objects
    for i, item in enumerate(data):
        try:
            json.dumps(item)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Item at index {i} is not JSON-serializable: {e}")
    
    logger.info(f"Validated {len(data)} items in JSON array")
    return data


def generate_output_path(input_path: str, output_path: str = None, output_dir: str = None) -> str:
    """Generate the output file path."""
    input_path_obj = Path(input_path)
    
    if output_path:
        output_path_obj = Path(output_path)
        # If no extension provided, add .jsonl
        if not output_path_obj.suffix:
            output_path_obj = output_path_obj.with_suffix('.jsonl')
    else:
        # Auto-generate output filename
        output_path_obj = input_path_obj.with_suffix('.jsonl')
    
    # Apply output directory if specified
    if output_dir:
        output_dir_path = Path(output_dir)
        output_dir_path.mkdir(parents=True, exist_ok=True)
        output_path_obj = output_dir_path / output_path_obj.name
    
    return str(output_path_obj)


def convert_json_to_jsonl(input_path: str, output_path: str = None, output_dir: str = None, 
                         overwrite: bool = False, validate_output: bool = True) -> str:
    """
    Convert JSON file to JSONL format.
    
    Args:
        input_path: Path to input JSON file
        output_path: Path for output JSONL file (optional)
        output_dir: Directory for output file (optional)
        overwrite: Whether to overwrite existing output file
        validate_output: Whether to validate the output file after creation
    
    Returns:
        Path to the created JSONL file
    """
    # Validate input
    validate_json_file(input_path)
    
    # Load and validate JSON data
    data = load_json_data(input_path)
    
    # Generate output path
    final_output_path = generate_output_path(input_path, output_path, output_dir)
    
    # Check if output file exists
    if Path(final_output_path).exists() and not overwrite:
        raise FileExistsError(f"Output file already exists: {final_output_path}. Use --overwrite to replace it.")
    
    # Create output directory if needed
    output_path_obj = Path(final_output_path)
    output_path_obj.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert to JSONL
    try:
        with open(final_output_path, "w", encoding="utf-8") as outfile:
            for i, item in enumerate(data):
                try:
                    json_line = json.dumps(item, ensure_ascii=False, separators=(',', ':'))
                    outfile.write(json_line + "\n")
                except Exception as e:
                    logger.error(f"Error serializing item {i}: {e}")
                    raise
        
        logger.info(f"Successfully wrote {len(data)} lines to {final_output_path}")
        
    except Exception as e:
        # Clean up partial file on error
        if Path(final_output_path).exists():
            Path(final_output_path).unlink()
        raise RuntimeError(f"Error writing to {final_output_path}: {e}")
    
    # Validate output file
    if validate_output:
        validate_jsonl_output(final_output_path, len(data))
    
    return final_output_path


def validate_jsonl_output(output_path: str, expected_lines: int) -> None:
    """Validate that the JSONL output was created correctly."""
    try:
        with open(output_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if len(lines) != expected_lines:
            raise ValueError(f"Output validation failed: expected {expected_lines} lines, got {len(lines)}")
        
        # Validate each line is valid JSON
        for i, line in enumerate(lines):
            try:
                json.loads(line.strip())
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON at line {i+1}: {e}")
        
        logger.debug(f"Output validation successful: {len(lines)} valid JSON lines")
        
    except Exception as e:
        logger.warning(f"Output validation failed: {e}")


def convert_multiple_files(input_files: List[str], output_dir: str = None, 
                          overwrite: bool = False) -> List[str]:
    """Convert multiple JSON files to JSONL format."""
    converted_files = []
    failed_files = []
    
    for input_file in input_files:
        try:
            output_file = convert_json_to_jsonl(
                input_file, 
                output_dir=output_dir, 
                overwrite=overwrite
            )
            converted_files.append(output_file)
            logger.info(f"✅ Converted: {input_file} → {output_file}")
        
        except Exception as e:
            logger.error(f"❌ Failed to convert {input_file}: {e}")
            failed_files.append(input_file)
    
    if failed_files:
        logger.warning(f"Failed to convert {len(failed_files)} files: {failed_files}")
    
    return converted_files


def find_json_files(directory: str) -> List[str]:
    """Find all JSON files in a directory."""
    dir_path = Path(directory)
    if not dir_path.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    
    json_files = list(dir_path.glob("*.json"))
    if not json_files:
        raise ValueError(f"No JSON files found in directory: {directory}")
    
    return [str(f) for f in json_files]


def main():
    parser = argparse.ArgumentParser(
        description="Convert JSON files to JSONL (JSON Lines) format.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s file.json                           # Convert single file
  %(prog)s file.json -o output.jsonl           # Custom output name
  %(prog)s file1.json file2.json -d outputs/   # Convert multiple files
  %(prog)s --directory inputs/ -d outputs/     # Convert all JSON files in directory
  %(prog)s file.json --overwrite               # Overwrite existing output
        """
    )
    
    # Input options (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "files", 
        nargs="*", 
        help="JSON file(s) to convert"
    )
    input_group.add_argument(
        "--directory", 
        help="Directory containing JSON files to convert"
    )
    
    # Output options
    parser.add_argument(
        "--output", "-o", 
        help="Output file path (for single file conversion only)"
    )
    parser.add_argument(
        "--output-dir", "-d", 
        help="Output directory for converted files"
    )
    parser.add_argument(
        "--overwrite", 
        action="store_true", 
        help="Overwrite existing output files"
    )
    parser.add_argument(
        "--no-validate", 
        action="store_true", 
        help="Skip output validation"
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
    
    try:
        # Determine input files
        if args.directory:
            input_files = find_json_files(args.directory)
            logger.info(f"Found {len(input_files)} JSON files in {args.directory}")
        else:
            input_files = args.files or []
        
        if not input_files:
            logger.error("No input files specified")
            sys.exit(1)
        
        # Validate arguments
        if len(input_files) > 1 and args.output:
            logger.error("Cannot specify custom output file for multiple input files")
            sys.exit(1)
        
        # Convert files
        if len(input_files) == 1:
            # Single file conversion
            output_file = convert_json_to_jsonl(
                input_files[0],
                output_path=args.output,
                output_dir=args.output_dir,
                overwrite=args.overwrite,
                validate_output=not args.no_validate
            )
            print(f"✅ Converted: {input_files[0]} → {output_file}")
        
        else:
            # Multiple file conversion
            converted_files = convert_multiple_files(
                input_files,
                output_dir=args.output_dir,
                overwrite=args.overwrite
            )
            print(f"✅ Successfully converted {len(converted_files)}/{len(input_files)} files")
            if converted_files:
                print(f"📁 Output files: {', '.join(converted_files)}")
    
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()