"""
Asynchronous file processor that processes multiple files in parallel.
The processor applies a transformation to each line of the input files
and writes the results to output files.
"""

import asyncio
import os
from typing import List, Dict, Set, Optional
from async_io import async_open, async_write_open


class AsyncFileProcessor:
    """Process multiple files asynchronously."""
    
    def __init__(self, input_dir: str, output_dir: str, max_concurrency: int = 5):
        """
        Initialize the processor with input and output directories.
        
        Args:
            input_dir: Directory containing input files
            output_dir: Directory to write processed files
            max_concurrency: Maximum number of files to process concurrently
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.max_concurrency = max_concurrency
        self.processed_files: Set[str] = set()
        self.in_progress: Set[str] = set()
        self.semaphore = asyncio.Semaphore(max_concurrency)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
    
    async def process_files(self, files: List[str]) -> Dict[str, bool]:
        """
        Process a list of files asynchronously.
        
        Args:
            files: List of file paths to process
            
        Returns:
            Dictionary mapping filenames to success status
        """
        tasks = []
        for file_path in files:
            if file_path in self.processed_files:
                print(f"Skipping already processed file: {file_path}")
                continue
                
            if file_path in self.in_progress:
                print(f"Skipping file in progress: {file_path}")
                continue
                
            self.in_progress.add(file_path)
            task = asyncio.create_task(self._process_file(file_path))
            tasks.append(task)
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        outcome = {}
        for file_path, result in zip(files, results):
            if isinstance(result, Exception):
                print(f"Error processing {file_path}: {result}")
                outcome[file_path] = False
            else:
                outcome[file_path] = result
                
        return outcome
    
    async def _process_file(self, file_path: str) -> bool:
        """
        Process a single file.
        
        Args:
            file_path: Path to the input file
            
        Returns:
            True if processing was successful, False otherwise
        """
        try:
            async with self.semaphore:
                base_name = os.path.basename(file_path)
                output_path = os.path.join(self.output_dir, f"processed_{base_name}")
                
                print(f"Starting to process: {file_path}")
                
                # Simulate file reading by chunks to handle large files
                async with async_open(file_path, 'r') as input_file:
                    # BUG: Not using async with for output file, which can lead to truncated outputs
                    output_file = open(output_path, 'w')
                    
                    try:
                        # Process the file line by line
                        async for line in input_file:
                            # Simulate processing delay
                            await asyncio.sleep(0.01)
                            
                            # Apply transformation to the line (uppercase in this case)
                            transformed_line = await self._transform_line(line)
                            
                            # Write the transformed line
                            output_file.write(transformed_line)
                            
                            # BUG: Missing flush() call here which can cause 
                            # data loss if the program crashes
                    finally:
                        # Close the output file
                        output_file.close()
                
                self.processed_files.add(file_path)
                self.in_progress.remove(file_path)
                
                print(f"Finished processing: {file_path}")
                return True
                
        except Exception as e:
            if file_path in self.in_progress:
                self.in_progress.remove(file_path)
            print(f"Error processing {file_path}: {e}")
            return False
    
    async def _transform_line(self, line: str) -> str:
        """
        Transform a line of text.
        
        Args:
            line: Input line
            
        Returns:
            Transformed line
        """
        # This is just a simple transformation for demo purposes
        # In a real application, this could be more complex
        return line.upper()
