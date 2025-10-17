from osbot_fast_api.api.routes.Fast_API__Routes                         import Fast_API__Routes
from starlette.responses                                                import FileResponse, Response, PlainTextResponse
from pathlib                                                            import Path
import mimetypes


class Routes__Admin(Fast_API__Routes):                                              # Admin UI static file server with cross-version reference support

    tag: str = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.adminUiRoot = Path(__file__).parent.parent.parent.parent / 'mgraph_ai_service_html__admin_ui'

    def serveStaticFile(self, filePath: str) -> Response:                           # Serve static files from admin UI package
        if filePath.startswith('html-service/'):                                    # Remove prefix
            relPath = filePath.replace('html-service/', '')
        elif filePath.startswith('/html-service/'):
            relPath = filePath.replace('/html-service/', '')
        else:
            relPath = filePath

        fullPath = (self.adminUiRoot / relPath).resolve()                           # Resolve full path

        try:
            fullPath.relative_to(self.adminUiRoot)                                  # Security check
        except ValueError:
            return self.serve404()                                                  # Path traversal detected

        if not fullPath.exists() or not fullPath.is_file():                         # Missing file
            return self.serve404()

        mimeType, _ = mimetypes.guess_type(str(fullPath))                           # Determine MIME type

        if mimeType is None:                                                        # Fallback for known types
            if   fullPath.suffix == '.css' : mimeType = 'text/css'
            elif fullPath.suffix == '.js'  : mimeType = 'application/javascript'
            elif fullPath.suffix == '.html': mimeType = 'text/html'
            else                           : mimeType = 'application/octet-stream'

        return FileResponse(fullPath, media_type=mimeType)

    def serve404(self) -> Response:                                                 # Serve 404 error page
        errorPage = self.adminUiRoot / 'v0' / 'v0.1.0' / '404.html'

        if errorPage.exists():
            return FileResponse(errorPage, status_code=404, media_type='text/html')

        return PlainTextResponse(content     = '404 - File Not Found\n\nThe requested admin UI resource could not be found.',
                                 status_code = 404)

    def getAvailableVersions(self) -> list:                                         # Scan for available UI versions
        versions = []
        v0Path   = self.adminUiRoot / 'v0'

        if v0Path.exists():
            for versionDir in sorted(v0Path.iterdir()):
                if versionDir.is_dir() and versionDir.name.startswith('v0.'):
                    versions.append(versionDir.name)

        return versions

    def setup_routes(self):                                                          # Register admin UI routes

        @self.router.get("/html-service/{file_path:path}")                          # Static file catch-all (must be last)
        async def serveStatic(file_path: str):
            return self.serveStaticFile(file_path)
