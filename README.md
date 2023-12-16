# RunCloud Service Checker

[![License](https://img.shields.io/github/license/fabiomsnunes/runcloud-service-checker)](https://github.com/fabiomsnunes/runcloud-service-checker/blob/main/LICENSE)

## Overview

The RunCloud Service Checker is a Python script designed to prevent service interruptions on RunCloud servers caused by out-of-memory (OOM) events. This script monitors the status of server services and automatically restarts them if necessary.

### Features

- Check the status of specified services.
- Automatically restart services if they are not running.
- Email notifications for service restarts.

## Getting Started

These instructions will help you get the project up and running on your local machine or server.

### Prerequisites

Before you begin, make sure you have Python 3.x installed. If you don't have it installed, you can follow these instructions to install Python 3 on your specific platform:

- **macOS**:
  - Open the terminal and run the following commands to update your package list and install Python 3:
    ```bash
    brew install python3
    ```
  - You can verify the installation by running: `python3 --version`.

- **Linux** (Ubuntu/Debian):
  - Open the terminal and run the following commands to update your package list and install Python 3:
    ```bash
    sudo apt update
    sudo apt install python3
    ```
  - You can verify the installation by running: `python3 --version`.

- **Windows**:
  - Visit the official Python website: [Download Python](https://www.python.org/downloads/windows/).
  - Download the latest Python 3.x installer.
  - Run the installer, and during installation, make sure to check the option that says "Add Python X.X to PATH" (X.X represents the Python version).
  - After installation, you can open Command Prompt or PowerShell and verify Python 3 installation by running: `python --version` or `python3 --version`.

Please note that the exact commands and steps may vary depending on your Linux distribution or Windows version. Once you have Python 3 installed, you can proceed with setting up and running the RunCloud Service Checker as described in the installation and usage sections above.


### Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/fabiomsnunes/runcloud-service-checker.git
```

2. Navigate to the project directory:

```bash
cd runcloud-service-checker
```

### Configuration

Before running the script, configure the `CONFIG` dictionary in the `runcloud-service-checker.py` script:

```python
CONFIG = {
    'base_url': 'https://manage.runcloud.io/api/v2',
    'api_key': 'YOUR_API_KEY',
    'api_secret': 'YOUR_API_SECRET',
    'services_to_check': ['lsws-rc', 'mysql', 'redis-server'],
    'excluded_services': {
        # Define your exclusions here
    },
    'email_notifications': True,
    'email_receiver': 'your.email@example.com',
    'smtp_host': 'YOUR_SMTP_HOST',
    'smtp_port': 587,
    'smtp_username': 'YOUR_SMTP_USERNAME',
    'smtp_password': 'YOUR_SMTP_PASSWORD',
    # ... (other configuration options)
}
```

Make sure to set the SMTP settings for email notifications.

### Usage

Run the script using Python:

```bash
python runcloud-service-checker.py
```

You can also use the `--verbose` flag to display detailed output:

```bash
python runcloud-service-checker.py --verbose
```

### Running as a Cron Job

To automate the service checking process, you can set up a cron job to run the script at specified intervals. Here's an example of how to do it:

1. Open your crontab configuration for editing:

```
crontab -e
```

2. Add a new line to schedule the script to run at your preferred frequency. For example, to run the script every 5 minutes, add the following line:

```
*/5 * * * * /usr/bin/python3 /path/to/runcloud-service-checker/check.py
```

Make sure to replace `/usr/bin/python3` with the path to your Python 3 interpreter, and `/path/to/runcloud-service-checker` with the actual path to the script's directory.

3. Save and exit the text editor. The script will now run automatically according to your cron job schedule.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the [RunCloud](https://runcloud.io/) team for providing the API and services for this script.

## Contributing

Contributions are welcome! Please feel free to open an issue or create a pull request.

## Contact

For questions or feedback, you can contact the author:

- Fábio Nunes
- GitHub: [https://github.com/fabiomsnunes](https://github.com/fabiomsnunes)
