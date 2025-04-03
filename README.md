# Markdown to PDF Converter

This project provides a CLI and a web-based API service for converting Markdown files into PDF and optionally HTML files.

## Features
- Convert Markdown files to PDF with syntax highlighting.
- Optionally generate an HTML version of the output.
- Custom CSS support for styling.
- Adjustable page size and margins.
- List available code highlighting styles.
- FastAPI-based web service with RESTful API.

## Installation
To install the required dependencies, use:
```sh
pip install -r requirements.txt
```

## CLI Usage
```sh
python convert.py [INPUT_FILE] [OUTPUT_FILE] [OPTIONS]
```

### Arguments:
- `INPUT_FILE` (optional): Path to the Markdown file.
- `OUTPUT_FILE` (optional): Output PDF file path.

### Options:
- `--style, -s` (default: `xcode`): Code highlighting style.
- `--css, -c`: Path to a custom CSS file.
- `--page-size` (default: `A4`): Page size options (e.g., `Letter`, `A3`).
- `--margin` (default: `0.05in`): Page margin settings.
- `--html, -h`: Also generate an HTML file.
- `--list-styles, -l`: List all available code highlighting styles.

### Example:
```sh
python convert.py sample.md sample.pdf --html --style=monokai
```

## API Usage
You can run the FastAPI web service to provide Markdown-to-PDF conversion:
```sh
python serve.py --host 127.0.0.1 --port 8882
```

### API Endpoints
#### Convert Markdown to PDF
**POST** `/api/topdf`

**Parameters:**
- `mdcontent`: Markdown content as a form parameter.

**Response:**
- Returns the generated PDF file.

#### Health Check
**GET** `/health`

**Response:**
```json
{"status": "ok"}
```

## Running the Server
To start the web server:
```sh
python serve.py
```
By default, the server runs on `http://127.0.0.1:8882/`.

## Dependencies
- `Click` for the CLI interface.
- `FastAPI` and `Uvicorn` for the web service.
- `MarkdownConverter` for conversion logic.

## License
This project is licensed under the MIT License.

