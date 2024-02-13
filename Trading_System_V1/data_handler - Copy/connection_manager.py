import threading
import time
import websocket

class ConnectionManager:
    def __init__(self, token_manager, constants, logger, on_message, on_open):
        self.token_manager = token_manager
        self.constants = constants
        self.logger = logger
        self.on_message = on_message
        self.on_open = on_open
        self.ws = None
        self.reconnect_interval = 1
        self.reconnecting = False
        self.lock = threading.Lock()

    def connect(self):
        with self.lock:
            if self.ws is not None:
                self.logger.info("An existing WebSocket connection is already active.")
                return

            tokens = self.token_manager.get_tokens()
            public_access_token = tokens.get('public_access_token')

            if not public_access_token:
                self.logger.error("Cannot start WebSocket connection without a public access token.")
                return

            ws_url = self.constants._service_config['routes']['broadcast_websocket'][0].format(
                public_access_token=public_access_token
            )
            self.logger.info(f"Attempting to open WebSocket connection with URL: {ws_url}")

            self.ws = websocket.WebSocketApp(
                ws_url,
                on_open=self.on_open,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close
            )

            wst = threading.Thread(target=lambda: self.ws.run_forever(ping_interval=60, ping_timeout=10))
            wst.daemon = True
            wst.start()

    def reconnect(self):
        with self.lock:
            if self.reconnecting:
                return
            self.reconnecting = True
            self.logger.info(f"Reconnecting in {self.reconnect_interval} seconds...")
            time.sleep(self.reconnect_interval)
            if self.ws is not None:
                self.ws.close()
                self.ws = None
            self.connect()
            self.reconnecting = False

    def on_error(self, ws, error):
        self.logger.error(f"WebSocket error: {error}")
        self.reconnect()

    def on_close(self, ws, close_status_code, close_msg):
        self.logger.info("WebSocket closed.")
        self.reconnect()