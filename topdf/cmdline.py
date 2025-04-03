import sys
from pathlib import Path

import click

from topdf.mdtopdf import MarkdownConverter


@click.command()
@click.argument("input_file", type=click.Path(exists=True), required=False)
@click.argument("output_file", type=click.Path(), required=False)
@click.option("--style", "-s", default="xcode", help="Code highlight style (e.g.: xcode, monokai, vs)")
@click.option("--css", "-c", type=click.Path(exists=True), help="Custom CSS file path")
@click.option("--page-size", default="A4", help="Page size (e.g.: A4, Letter, A3)")
@click.option("--margin", default="0.05in", help="Page margin (e.g.: 0.1in, 1cm, 10mm)")
@click.option("--html", "-h", is_flag=True, help="Also output HTML file")
@click.option("--list-styles", "-l", is_flag=True, help="List all available code highlighting styles")
def convert(input_file, output_file, style, css, page_size, margin, html, list_styles):
    """Convert Markdown file to PDF and optional HTML, or list available styles."""
    if list_styles:
        styles = MarkdownConverter.list_styles()
        click.echo("\n".join(styles))
        return

    if not input_file:
        click.echo("Error: No input file provided.", err=True)
        return

    input_path = Path(input_file)

    if output_file is None:
        output_pdf_path = input_path.with_suffix(".pdf")
    else:
        output_pdf_path = Path(output_file)

    base_path = output_pdf_path.with_suffix("")
    pdf_suffix = output_pdf_path.suffix
    index = 1

    while output_pdf_path.exists():
        output_pdf_path = Path(f"{base_path}_{index}{pdf_suffix}")
        index += 1

    output_html_path = None
    if html:
        output_html_path = input_path.with_suffix(".html")
        html_base_path = output_html_path.with_suffix("")
        html_suffix = ".html"
        html_index = 1

        while output_html_path.exists():
            output_html_path = Path(f"{html_base_path}_{html_index}{html_suffix}")
            html_index += 1

    custom_css = None
    if css:
        try:
            with open(css, "r", encoding="utf-8") as f:
                custom_css = f.read()
        except Exception as e:
            click.echo(f"Unable to read CSS file: {e}", err=True)
            return

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            md_content = f.read()

        converter = MarkdownConverter(highlight_style=style, custom_css=custom_css, page_size=page_size, margin=margin)
        pdf_path, html_path = converter.convert(
            md_content, str(output_pdf_path), str(output_html_path) if output_html_path else None
        )

        click.echo(f"PDF conversion successful: {pdf_path}")
        if html_path:
            click.echo(f"HTML conversion successful: {html_path}")

    except Exception as e:
        click.echo(f"Conversion failed: {e}", err=True)


if __name__ == "__main__":
    sys.argv.append("--html")
    sys.argv.append("/Users/seven/Desktop/test.md")
    convert()
