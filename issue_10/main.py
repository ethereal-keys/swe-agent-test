"""
Main entry point for the async file processor example.
"""

import asyncio
import os
import time
import random
from processing import AsyncFileProcessor
from utils import create_test_files, verify_output_files


async def process_directory(input_dir: str, output_dir: str) -> None:
    """
    Process all files in a directory.
    
    Args:
        input_dir: Input directory
        output_dir: Output directory
    """
    # Get all files in the input directory
    files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    
    # Create processor
    processor = AsyncFileProcessor(input_dir, output_dir)
    
    # Process files
    start_time = time.time()
    results = await processor.process_files(files)
    end_time = time.time()
    
    # Print results
    success_count = sum(1 for success in results.values() if success)
    print(f"\nProcessed {len(results)} files in {end_time - start_time:.2f} seconds")
    print(f"Success: {success_count}, Failed: {len(results) - success_count}")


async def main():
    """Main function to run the example."""
    # Configure random seed for reproducibility
    random.seed(42)
    
    # Create test directories
    input_dir = "test_input"
    output_dir = "test_output"
    
    # Create test files
    create_test_files(input_dir, 10, 100)
    
    # Process files
    await process_directory(input_dir, output_dir)
    
    # Verify output files
    issues_found = verify_output_files(input_dir, output_dir)
    
    # Exit with error code if issues were found
    if issues_found > 0:
        print(f"⚠️ Test failed with {issues_found} issues")
        exit(1)
    else:
        print("✅ Test passed successfully")


if __name__ == "__main__":
    asyncio.run(main())
