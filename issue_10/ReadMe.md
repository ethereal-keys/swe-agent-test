# Async File Processor

This project demonstrates an asynchronous file processing system that processes multiple files in parallel.

## Project Structure

```
.
├── async_io/
│   ├── __init__.py
│   ├── async_file_reader.py
│   └── async_file_writer.py
├── processing/
│   ├── __init__.py
│   └── file_processor.py
├── utils/
│   ├── __init__.py
│   └── file_utils.py
├── main.py
└── README.md
```

## Components

- **async_io**: Contains utilities for asynchronous file I/O operations
  - `async_file_reader.py`: Classes and functions for asynchronous file reading
  - `async_file_writer.py`: Classes and functions for asynchronous file writing

- **processing**: Contains file processing logic
  - `file_processor.py`: Implements the `AsyncFileProcessor` class that processes files in parallel

- **utils**: Contains utility functions
  - `file_utils.py`: Utilities for creating test files and verifying output

- **main.py**: Main entry point that demonstrates the functionality

## Usage

Run the main script:

```bash
python main.py
```

This will:
1. Create test files in the `test_input` directory
2. Process these files asynchronously
3. Write the results to the `test_output` directory
4. Verify that the output files contain the correctly transformed content

## Known Issues

There is a known issue with data loss during file processing. See GitHub Issue #10 for details.
