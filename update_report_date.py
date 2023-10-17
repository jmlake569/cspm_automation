import requests
import json
import datetime
import logging

REGION = "us-1"
C1_API_KEY = "<YOUR_API_KEY_HERE>"

# Set up a logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

class ApiException(Exception):
    def __init__(self, message, status_code=None, response_text=None):
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text

def get_report_configurations(base_url, headers):
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        logger.error(f"HTTP Error {response.status_code} when fetching report configurations. Response: {response.text}")
        raise ApiException("Failed to retrieve report configurations", response.status_code, response.text)
    except json.JSONDecodeError:
        logger.error("Failed to decode the response as JSON.")
        raise ApiException("Received invalid JSON from the server.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request to the API failed: {e}")
        raise ApiException("Failed to retrieve report configurations")

def update_report_configuration(report_id, title, days_difference_start, days_difference_end, base_url, headers):
    update_url = f"{base_url}/{report_id}"
    payload = {
    "data": {
        "attributes": {
            "configuration": {
                "title": title,
                "filter": {
                    "newerThanDays": days_difference_start,
                    "olderThanDays": days_difference_end
                }
            }
        }
    }
}

    try:
        response = requests.patch(update_url, headers=headers, json=payload)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        headers = response.headers
        logger.error(f"HTTP Error {response.status_code} when updating report configuration ID {report_id}. Response: {response.text}. Headers: {headers}")
        raise ApiException(f"Failed to update report configuration {report_id}", response.status_code, response.text)
    except json.JSONDecodeError:
        logger.error("Failed to decode the response as JSON.")
        raise ApiException("Received invalid JSON from the server.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request to update the report configuration failed: {e}")
        raise ApiException("Failed to update report configuration")

def calculate_date_difference(start_date_str, end_date_str):
    try:
        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")
        current_date = datetime.datetime.now()
        days_difference_start = (current_date - start_date).days
        days_difference_end = (current_date - end_date).days
        return days_difference_start, days_difference_end
    except ValueError as e:
        logger.error(f"Date calculation failed: {e}")
        raise ApiException("Invalid date format")

def main():
    base_url = f"https://conformity.{REGION}.cloudone.trendmicro.com/api/report-configs"
    headers = {
        "api-version": "v1",
        "Content-Type": "application/vnd.api+json",
        "Authorization": 'ApiKey ' + C1_API_KEY
    }

    report_configs_data = get_report_configurations(base_url, headers)
    report_configs_dict = {}
    for i, report_config in enumerate(report_configs_data.get("data", []), start=1):
        report_id = report_config.get("id")
        title = report_config.get("attributes", {}).get("configuration", {}).get("title", "")
        if report_id:
            report_configs_dict[i] = {"id": report_id, "title": title}

    for num, report_data in report_configs_dict.items():
        report_id = report_data["id"]
        title = report_data["title"]
        print(f"{num}. Report ID: {report_id} - Title: {title}")

    selected_numbers = input("Enter the number(s) of the report configuration(s) you want to update (comma-separated): ")

    try:
        selected_numbers_list = [int(num.strip()) for num in selected_numbers.split(",")]
        selected_reports = [report_configs_dict[num] for num in selected_numbers_list if num in report_configs_dict]
    except ValueError:
        logger.error("Invalid input for report numbers.")
        return

    start_date_str = input("Enter a start date (YYYY-MM-DD): ")
    end_date_str = input("Enter an end date (YYYY-MM-DD): ")
    days_difference_start, days_difference_end = calculate_date_difference(start_date_str, end_date_str)

    for report_data in selected_reports:
        report_id = report_data["id"]
        title = report_data["title"]
        try:
            update_report_configuration(report_id, title, days_difference_start, days_difference_end, base_url, headers)
            print(f" {title} report has been updated.")
        except Exception as e:
            print(e)
            logger.error(f"Application Error: {e}")

if __name__ == "__main__":
    main()

