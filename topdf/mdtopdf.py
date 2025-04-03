import re
from typing import Optional, Tuple

import markdown
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_all_styles
from weasyprint import HTML


class CodeHighlighter:
    """Code highlighting processor class"""

    def __init__(self, style: str = "default"):
        self.style = style
        self.formatter = HtmlFormatter(style=style)

    def get_css(self) -> str:
        """Get CSS for highlight styles"""
        return self.formatter.get_style_defs(".codehilite")

    def highlight_code(self, text: str) -> str:
        """Process code blocks in text and apply highlighting"""
        pattern = r"```(\w+)\n(.*?)```"

        def replace_code(match):
            lang, code = match.groups()
            try:
                lexer = get_lexer_by_name(lang)
                return f'<div class="codehilite">{highlight(code, lexer, self.formatter)}</div>'
            except Exception:
                return f"<pre><code>{code}</code></pre>"

        return re.sub(pattern, replace_code, text, flags=re.DOTALL)


class MarkdownConverter:
    """Markdown Converter - Supports PDF and HTML output"""

    DEFAULT_EXTENSIONS = ["tables", "fenced_code", "codehilite", "nl2br", "sane_lists", "smarty", "toc"]
    CODE_CSS = """
        code {
            font-family: "Menlo", "Monaco", "Courier New", "monospace", "sans-serif";
            line-height: 1.7;
            font-variant-numeric: normal;
            font-size: 85%;
        }
    """
    DEFAULT_CSS = """
        @font-face {
            font-family: 'monospace';
            src: url('static/Monospace.ttf') format('truetype');
        }
        body {
            font-family: "ui-sans-serif", "-apple-system", "system-ui", "Segoe UI", "Menlo", "Monaco", "Courier New", "monospace", "sans-serif";
            line-height: 1.6;
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
        }
        pre {
            background-color: #f6f8fa;
            border-radius: 3px;
            padding: 16px;
            overflow: auto;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 16px;
        }
        th, td {
            border: 1px solid #dfe2e5;
            padding: 6px 13px;
        }
        th {
            background-color: #f6f8fa;
        }
    """

    def __init__(
        self,
        highlight_style: str = "xcode",
        custom_css: Optional[str] = None,
        page_size: str = "A4",
        margin: str = "0.05in",
    ):
        self.highlighter = CodeHighlighter(highlight_style)
        # Add custom page settings
        page_css = f"@page {{ size: {page_size}; margin: {margin}; }}"
        if custom_css:
            self.custom_css = page_css + "\n" + custom_css
        else:
            self.custom_css = page_css
        self.md_converter = markdown.Markdown(extensions=self.DEFAULT_EXTENSIONS)

    def generate_html(self, markdown_content: str) -> str:
        """Convert Markdown content to complete HTML"""
        html_content = self.md_converter.convert(markdown_content)

        full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Markdown to HTML</title>
    <style>
        {self.DEFAULT_CSS}
        {self.highlighter.get_css()}
        {self.custom_css or ''}
        {self.CODE_CSS}
    </style>
</head>
<body>{html_content}</body>
</html>"""
        return full_html

    @staticmethod
    def convert_to_pdf(html_content: str, output_file: str) -> None:
        """Convert HTML content to a PDF file"""
        # When using WeasyPrint, ensure @page rules are correctly applied
        HTML(string=html_content, base_url=".").write_pdf(
            output_file,
            # Optional: explicitly specify page size and margins as a fallback
            presentational_hints=True,
        )

    def convert(
        self, markdown_content: str, output_pdf: str, output_html: Optional[str] = None
    ) -> Tuple[str, Optional[str]]:
        """Convert Markdown content to PDF and optional HTML file"""
        html_content = self.generate_html(markdown_content)

        # Convert to PDF
        self.convert_to_pdf(html_content, output_pdf)

        # If HTML output path is provided, save the HTML file
        if output_html:
            with open(output_html, "w", encoding="utf-8") as f:
                f.write(html_content)
            return output_pdf, output_html

        return output_pdf, None

    @staticmethod
    def list_styles():
        """List all available code highlighting styles"""
        return sorted(list(get_all_styles()))
