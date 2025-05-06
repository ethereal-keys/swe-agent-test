"""
Utility functions for file operations.
"""

import os
from datetime import datetime


def create_test_files(directory: str, num_files: int, lines_per_file: int) -> None:
    """
    Create test files for processing.
    
    Args:
        directory: Directory to create files in
        num_files: Number of files to create
        lines_per_file: Number of lines in each file
    """
    os.makedirs(directory, exist_ok=True)
    
    for i in range(num_files):
        file_path = os.path.join(directory, f"test_file_{i}.txt")
        with open(file_path, 'w') as f:
            for j in range(lines_per_file):
                f.write(f"This is line {j} in file {i}, created at {datetime.now().isoformat()}\n")
    
    print(f"Created {num_files} test files in {directory}")


def verify_output_files(input_dir: str, output_dir: str) -> int:
    """
    Verify that output files match the transformed input files.
    
    Args:
        input_dir: Directory containing input files
        output_dir: Directory containing output files
        
    Returns:
        Number of issues found
    """
    print("\nVerifying output files...")
    input_files = os.listdir(input_dir)
    output_files = os.listdir(output_dir)
    
    print(f"Input files: {len(input_files)}")
    print(f"Output files: {len(output_files)}")
    
    # Check file contents
    issues_found = 0
    for input_file in input_files:
        output_file = f"processed_{input_file}"
        
        if output_file not in output_files:
            print(f"Missing output file: {output_file}")
            issues_found += 1
            continue
        
        # Compare line counts
        input_path = os.path.join(input_dir, input_file)
        output_path = os.path.join(output_dir, output_file)
        
        with open(input_path, 'r') as f_in:
            input_lines = f_in.readlines()
        
        with open(output_path, 'r') as f_out:
            output_lines = f_out.readlines()
        
        if len(input_lines) != len(output_lines):
            print(f"Line count mismatch for {input_file}: Input={len(input_lines)}, Output={len(output_lines)}")
            issues_found += 1
            continue
        
        # Check content (allowing for the transformation)
        content_mismatch = False
        for i, (in_line, out_line) in enumerate(zip(input_lines, output_lines)):
            if out_line != in_line.upper():
                print(f"Content mismatch in {input_file} at line {i}")
                content_mismatch = True
                break
        
        if content_mismatch:
            issues_found += 1
    
    if issues_found == 0:
        print("All files processed correctly!")
    else:
        print(f"Found issues in {issues_found} files")
        
    return issues_found
