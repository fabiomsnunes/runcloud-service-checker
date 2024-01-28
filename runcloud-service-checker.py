"""
RunCloud Service Checker
Author: Fábio Nunes
License: MIT License
GitHub: https://github.com/fabiomsnunes/runcloud-service-checker

Description:
This script checks the status of services on your RunCloud servers and restarts them if necessary.
"""
import time
import requests
import base64
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration options
CONFIG = {
    'base_url': 'https://manage.runcloud.io/api/v2',
    'api_key': 'YOUR_API_KEY',  # Replace with your API key
    'api_secret': 'YOUR_API_SECRET',  # Replace with your API secret
    'services_to_check': ['lsws-rc', 'mysql', 'redis-server'],  # List of services to check, use the realName field. See available here: https://runcloud.io/docs/api/services
    'excluded_services': {  # List of servers and services to exclude
        # 12345: ['ALL_SERVICES'], # Example to exclude all services on server 12345
        # 56789: ['redis'], # Example to exclude redis on server 56789
    },
}
EMAIL_SETTINGS = {
    'email_notifications': True,  # Set to False to disable email notifications
    'email_receiver': 'your_email@example.com',  # Set your email address here
    'from_name': 'Runcloud service checker',
    'from_email': 'noreply@example.com',
    'smtp_host': 'smtp.example.com',
    'smtp_port': 587,
    'smtp_username': 'your_smtp_username',
    'smtp_password': 'your_smtp_password',
}

# Global variable for verbosity, set to False by default
VERBOSE_MODE = False

# Headers for API requests
api_credentials = f"{CONFIG['api_key']}:{CONFIG['api_secret']}"
HEADERS = {
    'Authorization': f'Basic {base64.b64encode(api_credentials.encode()).decode()}',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
}

def send_notification(server_id: str, server_name: str, service_name: str) -> None:
    """Sends an email notification about a service restart."""

    # Check if email notifications are enabled
    if not EMAIL_SETTINGS['email_notifications']:
        return

    # Compose the subject and body of the email
    subject = f"Service Restarted on {server_name}"
    body = f"The service {service_name} has been restarted on server {server_name}.\nhttps://manage.runcloud.io/servers/{server_id}/log"

    # Create the email message
    msg = MIMEMultipart()
    msg['To'] = EMAIL_SETTINGS['email_receiver']
    msg['From'] = f"{EMAIL_SETTINGS['from_name']} <{EMAIL_SETTINGS['from_email']}>"
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server and send the email
    smtp_server = smtplib.SMTP(EMAIL_SETTINGS['smtp_host'], EMAIL_SETTINGS['smtp_port'])
    smtp_server.starttls()
    smtp_server.login(EMAIL_SETTINGS['smtp_username'], EMAIL_SETTINGS['smtp_password'])
    smtp_server.sendmail(EMAIL_SETTINGS['smtp_username'], EMAIL_SETTINGS['email_receiver'], msg.as_string())
    smtp_server.quit()

def fetch_data(url, page=1, per_page=40):
    """Fetches data from the API with pagination."""
    paginated_url = f"{url}?page={page}&perPage={per_page}"
    response = requests.get(paginated_url, headers=HEADERS)
    # Check if the request was successful
    if response.status_code == 200:
        # Return the fetched data as a list of dictionaries
        return response.json()

    # Print error message if the request failed
    print(f"Failed to fetch data. Status code: {response.status_code}")
    print(response.text)

    # Return an empty list as a fallback
    return []

def restart_service(server_id: int, service_name: str) -> bool:
    """Restarts a service on the specified server."""
    # Construct the URL for restarting the service
    reset_url = f"{CONFIG['base_url']}/servers/{server_id}/services"

    # Prepare the data for the restart action
    reset_data = {
        'action': 'restart',
        'realName': service_name,
    }

    # Send the restart request and get the response
    response = requests.patch(reset_url, json=reset_data, headers=HEADERS)

    # Check if the restart was successful and return the result
    if response.status_code == 200:
        if VERBOSE_MODE:
            print(f"Service {service_name} restarted successfully.")
        return True
    else:
        if VERBOSE_MODE:
            print(f"Failed to restart service {service_name}.")
        return False

def check_services(servers):
    """Checks the specified services on each server."""
    # Loop through the list of servers
    for server in servers:
        server_id = server['id']
        server_name = server['name']

        # Print a message indicating the server being checked
        if VERBOSE_MODE:
            print("\nChecking server:", server_name)

        # Check if the server is excluded from service checks
        if server_id in CONFIG['excluded_services']:
            excluded_services = CONFIG['excluded_services'][server_id]

            # Check if all services on this server should be skipped
            if 'ALL_SERVICES' in excluded_services:
                if VERBOSE_MODE:
                    print("-- 🚧 Skipping all services on this server as requested.")
                continue

        # Construct the URL to fetch services data for the current server
        services_url = f"{CONFIG['base_url']}/servers/{server_id}/services"
        services_data = fetch_data(services_url)

        # Check if the fetched services data is in the expected format
        if isinstance(services_data, list):
            if VERBOSE_MODE:
                print("Failed to fetch services data. Expected a dictionary.")
            continue

        # Loop through the services data for the current server
        for service_key, service_data in services_data.items():
            service_name = service_data['realName']

            # Check if this service should be checked
            if service_name in CONFIG['services_to_check']:

                # Check if this service is excluded for this server
                if server_id in CONFIG['excluded_services'] and service_name in CONFIG['excluded_services'][server_id]:
                    if VERBOSE_MODE:
                        print(f"-- 🚧 Skipping service {service_name} on {server_name} as it's excluded.")
                    continue

                # Check if the service is currently not running
                running = service_data['running']

                if not running:
                    if VERBOSE_MODE:
                        print(f"-- ❌ Resetting {service_name} on {server_name}...")
                    # Attempt to restart the service and send a notification if successful
                    if restart_service(server_id, service_name):
                        send_notification(server_id, server_name, service_name)
                else:
                    # The service is running
                    if VERBOSE_MODE:
                        print(f"-- ✅ {service_name} on {server_name}")

                    # Sleep for 1.6 seconds (60 sec / 40 servers per page + 0.1 for buffer) to avoid rate limiting
                    time.sleep(1.6)
def main():
    global VERBOSE_MODE
    servers = []
    page = 1
    more_data = True

    if '--verbose' in sys.argv:
        VERBOSE_MODE = True

    while more_data:
        response = fetch_data(f"{CONFIG['base_url']}/servers", page)
        data = response.get('data', [])
        servers.extend(data)

        # Check if there are more pages of data
        more_data = len(data) == 40  # If we got 40 items, there might be more
        page += 1

    check_services(servers)

if __name__ == "__main__":
    main()
