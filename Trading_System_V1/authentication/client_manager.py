import logging
from authentication import Auth

def authenticate_and_get_client():
    logger = logging.getLogger(__name__)
    auth_instance = Auth()

    # Check if the access token is valid
    if not auth_instance.access_token or not auth_instance.validate_access_token():
        # If not valid, attempt reauthentication
        if not auth_instance.reauthenticate():
            logger.error("Authentication failed.")
            return None

    # If authenticated, get the client instance
    client = auth_instance.get_client()
    if client:
        logger.info("Authenticated PMClient retrieved successfully.")
        return client
    else:
        logger.error("Client could not be retrieved.")
        return None
