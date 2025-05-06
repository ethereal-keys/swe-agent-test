"""
Asynchronous file I/O utilities for reading files.
"""

import asyncio
from typing import Optional


class AsyncFileReader:
    """A file-like object wrapper for asynchronous reading."""
    
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
            await asyncio.get_event_loop().run_in_executor(None, self.file.close)
    
    async def readline(self) -> str:
        """
        Read a line from the file asynchronously.
        
        Returns:
            A line from the file
        """
        if not self.file:
            raise ValueError("File is not open")
        
        loop = asyncio.get_event_loop()
        line = await loop.run_in_executor(None, self.file.readline)
        return line
    
    def __aiter__(self):
        """Return self as an async iterator."""
        return self
    
    async def __anext__(self) -> str:
        """
        Get the next line asynchronously.
        
        Returns:
            Next line from the file
            
        Raises:
            StopAsyncIteration: When end of file is reached
        """
        line = await self.readline()
        if not line:
            raise StopAsyncIteration
        return line


async def async_open(file_path: str, mode: str) -> AsyncFileReader:
    """
    Open a file asynchronously.
    
    Args:
        file_path: Path to the file
        mode: File open mode
        
    Returns:
        An async file reader object
    """
    reader = AsyncFileReader(file_path, mode)
    await reader.__aenter__()
    return reader
