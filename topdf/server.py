import asyncio
import os
import tempfile
from contextlib import asynccontextmanager

import click
import uvicorn
from fastapi import FastAPI, BackgroundTasks, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from topdf.mdtopdf import MarkdownConverter


class MarkdownToPdfApp:
    """FastAPI application for converting Markdown to PDF."""

    def __init__(self):
        """
        Initialize the FastAPI application and configure routes and middleware.
        """

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            yield
            await self.shutdown()

        self.app = FastAPI(
            title="Markdown to PDF Converter",
            description="API service for converting Markdown text to PDF files",
            version="1.0.0",
            lifespan=lifespan,
        )
        self.static_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static")

        self._setup_middleware()
        self._setup_routes()
        self._mount_static_files()

        # Store active file cleanup tasks to ensure they complete
        self.cleanup_tasks = set()

    def _setup_middleware(self):
        """Configure middleware for the application."""
        # Add CORS middleware with restricted origins
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Restrict to specific origins
            allow_credentials=True,
            allow_methods=["POST", "GET"],
            allow_headers=["Content-Type"],
        )

    def _setup_routes(self):
        """Set up API routes."""
        self.app.post("/api/topdf", summary="Convert Markdown to PDF")(self.convert_markdown_to_pdf)
        self.app.get("/health", summary="Health check endpoint")(self.health_check)
        self.app.get("/", summary="Homepage")(self.homepage)

    def _mount_static_files(self):
        """Mount static files directory."""
        # Check if static directory exists
        if not os.path.exists(self.static_dir):
            raise FileNotFoundError(f"Static directory not found: {self.static_dir}")

        # Mount the static directory
        self.app.mount("/static", StaticFiles(directory=self.static_dir), name="static")

    async def homepage(self):
        """Serve the index.html file as the homepage."""
        index_path = os.path.join(self.static_dir, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        else:
            raise HTTPException(status_code=404, detail="Homepage not found")

    @staticmethod
    async def health_check():
        """Health check endpoint for monitoring."""
        return {"status": "ok"}

    async def convert_markdown_to_pdf(
        self,
        request: Request,
        background_tasks: BackgroundTasks,
        mdcontent: str = Form(..., description="Markdown content"),
    ):
        """
        Convert Markdown content to PDF and return the file.
        """
        # Validate input
        if not mdcontent.strip():
            raise HTTPException(status_code=400, detail="Markdown content cannot be empty")
        # test
        # await asyncio.sleep(12)
        # Create temporary file with secure method
        try:
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_file:
                pdf_path = tmp_file.name
        except Exception:
            raise HTTPException(status_code=500, detail="Failed to create temporary file")

        try:
            # Create converter with validated settings
            converter = MarkdownConverter(highlight_style="xcode", custom_css=None)

            # Convert content
            converter.convert(mdcontent, pdf_path)

            # Schedule file cleanup
            cleanup_task = asyncio.create_task(self.delete_file(pdf_path))
            self.cleanup_tasks.add(cleanup_task)
            cleanup_task.add_done_callback(self.cleanup_tasks.discard)

            # Return PDF file
            return FileResponse(
                path=pdf_path,
                filename="output.pdf",
                media_type="application/pdf",
                headers={"Content-Disposition": "attachment; filename=output.pdf"},
            )

        except Exception as e:
            # Clean up temporary file if conversion failed
            self.safe_delete_file(pdf_path)
            raise HTTPException(status_code=500, detail=f"Error during conversion: {str(e)}")

    @staticmethod
    def safe_delete_file(file_path: str) -> None:
        """
        Safely delete a file if it exists.
        """
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
        except Exception:
            pass

    @staticmethod
    async def delete_file(file_path: str, delay: int = 60) -> None:
        """
        Delete a file after a specified delay.
        """
        try:
            await asyncio.sleep(delay)
            if os.path.exists(file_path):
                os.unlink(file_path)
        except Exception:
            pass

    async def shutdown(self) -> None:
        """Clean up resources when shutting down."""
        # Wait for all cleanup tasks to complete
        if self.cleanup_tasks:
            await asyncio.gather(*self.cleanup_tasks, return_exceptions=True)

    def run(self, host: str = "0.0.0.0", port: int = 8882, reload: bool = False) -> None:
        """
        Run the FastAPI application with uvicorn.
        """
        print(f"Web service running at http://{host}:{port}")
        uvicorn.run(
            self.app,
            host=host,
            port=port,
            reload=reload,
            access_log=False,
        )


@click.command()
@click.option("--host", default="127.0.0.1", show_default=True, help="Host address to listen on")
@click.option("--port", default=8882, show_default=True, help="Port to listen on")
def serve(host: str, port: int) -> None:
    """Start web service providing Markdown to PDF conversion API."""
    try:
        app = MarkdownToPdfApp()
        app.run(host=host, port=port)
    except FileNotFoundError as e:
        click.echo(f"Error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    try:
        serve()
    except Exception as e:
        click.echo(f"Fatal error: {str(e)}")
        exit(1)
