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

Before you begin, make sure you have Python 3.x installed along with the `python-dotenv` package, which is required for loading configuration settings from the `.env` file. If you don't have Python and `python-dotenv` installed, follow the instructions below:

- **Python 3 Installation:**
  - Instructions for installing Python 3 vary by platform. Please refer to the Python 3 installation guide for your operating system.

- **Installing python-dotenv:**
  - Once Python 3 is installed, open your terminal or command prompt and install the `python-dotenv` package using pip:
    ```bash
    pip install python-dotenv
    ```

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

To set up the project, you will start by renaming the `.env.example` file to `.env`. Inside this `.env` file, you'll find placeholders for various settings that need to be configured:

- **RunCloud API Secrets**: These are your personal credentials for accessing the [RunCloud API](https://runcloud.io/docs/api), including your API Key (`API_KEY`) and API Secret (`API_SECRET`). You will need to replace the placeholders with your actual RunCloud API credentials.

- **Services to Check**: Specify which services the script should monitor on your RunCloud servers. This is done by listing the service names under `SERVICES_TO_CHECK`, separated by commas.

- **SMTP Details**: For the script to send email notifications, you must provide SMTP server details, including the host (`SMTP_HOST`), port (`SMTP_PORT`), username (`SMTP_USERNAME`), and password (`SMTP_PASSWORD`).

Ensure that you carefully replace the placeholder values with your actual configuration details to ensure the script functions correctly.


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
