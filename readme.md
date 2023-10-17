
---

## Conformity Report Configuration Updater

This script allows Cloud One Conformity customers to update the date filters of specific report configurations by specifying a date range.

### Prerequisites

- Python 3.6+
- `requests` library. Install it using:
  ```
  pip install requests
  ```

### Configuration

1. Set the `REGION` variable to your specific Cloud One Conformity region (e.g., `us-west-2`).
2. Set the `C1_API_KEY` variable with your Cloud One Conformity API Key.

### How It Works

1. The script fetches all the report configurations for the specified region and API key.
2. It displays the report IDs and titles for the user to select.
3. The user specifies which report configurations they want to update by entering the corresponding numbers.
4. The user provides a start date and end date in the format `YYYY-MM-DD`.
5. The script calculates the day difference from today to the provided dates and updates the selected report configurations with these values.

### Running the Script

Navigate to the directory containing the script and run:

```
python update_report_date.py
```

Replace `<script_name>` with the name you saved the script as.

### Error Handling

The script includes error handling for HTTP errors, JSON parsing errors, and invalid user inputs. If there's an issue with a specific operation, an error message will be displayed.

### Logging

Logging has been set up to provide information on any errors encountered during execution. It will log messages with severity levels of INFO and above.

### Customization

To customize the script, such as adding additional attributes to update in the report configuration, you can modify the payload in the `update_report_configuration` function.

---

You can save this content in a `README.md` file. This will provide an overview and guidance for anyone who wants to use the script and is a Conformity customer.
