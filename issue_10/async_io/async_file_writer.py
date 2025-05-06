"""
Asynchronous file I/O utilities for writing files.
"""

import asyncio
from typing import Optional


class AsyncFileWriter:
    """A file-like object wrapper for asynchronous writing."""
    
    def __init__(self, file_path: str, mode: str):
        """
        Initialize with a file path and mode.
        
        Args:
            file_path: Path to the file
            mode: File open mode ('r', 'w', etc.)
        """
        self.file_path = file_path
        self.mode = mode
        self.file = None
        
    async def __aenter__(self):
        """Async context manager entry."""
        # Open the file in the specified mode
        loop = asyncio.get_event_loop()
        self.file = await loop.run_in_executor(None, lambda: open(self.file_path, self.mode))
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.file:
            # Ensure data is flushed before closing
            await self.flush()
            await asyncio.get_event_loop().run_in_executor(None, self.file.close)
    
    async def write(self, data: str) -> int:
        """
        Write data to the file asynchronously.
        
        Args:
            data: Data to write
            
        Returns:
            Number of bytes written
        """
        if not self.file:
            raise ValueError("File is not open")
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, self.file.write, data)
        return result
    
    async def flush(self) -> None:
        """Flush the file buffer to disk asynchronously."""
        if not self.file:
            raise ValueError("File is not open")
        
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.file.flush)


async def async_write_open(file_path: str, mode: str) -> AsyncFileWriter:
    """
    Open a file for writing asynchronously.
    
    Args:
        file_path: Path to the file
        mode: File open mode
        
    Returns:
        An async file writer object
    """
    writer = AsyncFileWriter(file_path, mode)
    await writer.__aenter__()
    return writer
