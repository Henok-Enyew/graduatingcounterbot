"""Keep-Alive Server Module

This module provides a Flask HTTP server that runs in a background thread
to keep the bot active on Render's platform.
"""

import logging
import threading
from flask import Flask


class KeepAliveServer:
    """Flask HTTP server for Render platform keep-alive.
    
    Runs a simple HTTP server in a background daemon thread that responds
    to health check requests, preventing Render from hibernating the service.
    """
    
    def __init__(self, port: int = 8080):
        """Initialize the KeepAliveServer.
        
        Args:
            port: Port number for the HTTP server to listen on
        """
        self.port = port
        self.app = Flask(__name__)
        self.logger = logging.getLogger(__name__)
        
        # Configure Flask to be less verbose
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.WARNING)
        
        # Define routes
        self._setup_routes()
    
    def _setup_routes(self):
        """Set up Flask routes."""
        
        @self.app.route('/')
        def health_check():
            """Health check endpoint for Render platform.
            
            Returns:
                Tuple of (response_text, status_code)
            """
            return 'Bot is active', 200
        
        @self.app.route('/health')
        def health():
            """Alternative health check endpoint.
            
            Returns:
                Tuple of (response_text, status_code)
            """
            return 'OK', 200
        
        @self.app.route('/ping')
        def ping():
            """Ping endpoint for external monitoring services.
            
            Returns:
                Tuple of (response_text, status_code)
            """
            return 'pong', 200
    
    def start(self):
        """Start the Flask server in a background daemon thread.
        
        The server runs in a daemon thread so it doesn't prevent the main
        program from exiting when needed. Uses threaded mode for better
        handling of concurrent requests.
        """
        def run_server():
            """Internal function to run the Flask server."""
            try:
                self.logger.info(f"Starting keep-alive server on port {self.port}")
                # Use threaded=True for better concurrency
                # Use host='0.0.0.0' to accept connections from any IP
                self.app.run(
                    host='0.0.0.0',
                    port=self.port,
                    debug=False,
                    use_reloader=False,
                    threaded=True
                )
            except Exception as e:
                self.logger.error(f"Keep-alive server error: {str(e)}")
        
        # Start server in daemon thread
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        self.logger.info(f"Keep-alive server started on port {self.port}")
        self.logger.info(f"Health check endpoints: /, /health, /ping")
