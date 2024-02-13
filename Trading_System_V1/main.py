import logging
from authentication.authentication import Auth
from cli import run_cli

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    setup_logging()

    auth = Auth()  # Create an instance of Auth
    if not auth.access_token or not auth.validate_access_token():
        logging.error("Authentication failed or was cancelled.")
        return

    logging.info("Authentication successful. Proceeding to the CLI.")
    run_cli(auth)  # Pass the Auth instance to run_cli

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExecution interrupted by the user. Exiting...")
