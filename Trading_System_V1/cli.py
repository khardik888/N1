import logging
import requests
import time

def validate_token(func):
    def wrapper(auth, *args, **kwargs):
        logger = logging.getLogger(__name__)  # Define logger here
        if not auth.access_token or not auth.validate_access_token():
            logger.error("Access token is invalid or expired.")
            auth.reauthenticate()
            return  # Exit the function if authentication fails
        return func(auth, *args, **kwargs)
    return wrapper

@validate_token
def view_account_details(auth):
    logger = logging.getLogger(__name__)  # Define logger here
    url = "https://developer.paytmmoney.com/accounts/v1/user/details"
    headers = {"x-jwt-token": auth.access_token}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            account_details = response.json()
            logger.info(f"Account Details: {account_details}")
        else:
            logger.error(f"Failed to fetch account details. Status Code: {response.status_code}")
    except Exception as e:
        logger.error(f"An error occurred while fetching account details: {e}")

@validate_token
def view_fund_details(auth):
    logger = logging.getLogger(__name__)  # Define logger here
    url = "https://developer.paytmmoney.com/funds/v1/fund/details"
    headers = {"x-jwt-token": auth.access_token}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            fund_details = response.json()
            logger.info(f"Fund Details: {fund_details}")
        else:
            logger.error(f"Failed to fetch fund details. Status Code: {response.status_code}")
    except Exception as e:
        logger.error(f"An error occurred while fetching fund details: {e}")

def start_live_data_stream(auth):
    logger = logging.getLogger(__name__)  # Define logger here
    logger.info("Starting Live Market Data Stream...")
    while True:
        # Implement your live data stream logic here
        time.sleep(5)  # Simulate data streaming every 5 seconds

def display_menu():
    print("\nOptions:")
    print("1. View Account Details")
    print("2. View Fund Details")
    print("3. Start Live Market Data Stream")
    print("4. Exit")
    return input("Enter your choice (1-4): ")

def run_cli(auth):
    try:
        while True:
            choice = display_menu()
            if choice == '1':
                view_account_details(auth)
            elif choice == '2':
                view_fund_details(auth)
            elif choice == '3':
                start_live_data_stream(auth)
            elif choice == '4':
                logger.info("Exiting the application.")
                break
            else:
                logger.warning("Invalid choice, please try again.")
    except KeyboardInterrupt:
        logger.info("Program interrupted. Exiting gracefully.")
