# Spreadsheet AI Email Monitor

A small Python automation that:

1. Reads data from a Google Sheet.
2. Detects rows added since the previous run.
3. Uses OpenRouter AI to summarize the new rows.
4. Sends the summary by email through Gmail SMTP.
5. Uses `last_row.txt` to remember which rows were already processed.

## Files

```text
project/
├── maintest.py
├── requirements.txt
├── last_row.txt
├── .env
└── README.md
```

`last_row.txt` should contain a number such as:

```text
1
```

The script updates this number after processing the spreadsheet.

## Install

Install the packages from `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

For the current OpenRouter version of the project, make sure `requirements.txt` includes:

```text
google-api-python-client
langchain
langchain-openai
python-dotenv
```

## Environment variables

Create a `.env` file in the same folder as `maintest.py`:

```env
GOOGLE_API_KEY=your_google_sheets_api_key
OPENROUTER_API_KEY=your_openrouter_api_key

SPREADSHEET_ID=your_google_sheet_id
SHEET_NAME=Sheet1

SENDER_EMAIL=your_gmail@gmail.com
RECIPIENT_EMAIL=receiver@gmail.com
SENDER_PASSWORD=your_gmail_app_password
```

### Important: `SENDER_PASSWORD`

`SENDER_PASSWORD` is **NOT your normal Gmail password**.

It must be a Google **App Password**.

To create one:

1. Enable 2-Step Verification on your Google account.
2. Open your Google Account security settings.
3. Search for **App passwords**.
4. Create a new app password for this project.
5. Copy the generated 16-character password.
6. Put that value in `.env` as `SENDER_PASSWORD`.

Do not upload your real `.env` file to GitHub.

Add this to `.gitignore`:

```text
.env
```

You can also create `.env.example` containing only empty placeholders.

## Gmail SMTP

### Current recommended method

The SSL method connects securely from the beginning using port `465`:

```python
import ssl
import smtplib

context = ssl.create_default_context()

with smtplib.SMTP_SSL(
    "smtp.gmail.com",
    465,
    context=context
) as server:
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.send_message(msg)
```

The `with` block closes the connection automatically.

### Previous method

The first version used port `587` and upgraded the connection with `starttls()`:

```python
# OLD METHOD
# server = smtplib.SMTP("smtp.gmail.com", 587)
# server.starttls()
# server.login(SENDER_EMAIL, SENDER_PASSWORD)
# server.send_message(msg)
# server.quit()
```

Both are valid Gmail SMTP approaches. This project switched to SSL on port `465` while troubleshooting SMTP authentication/connection issues.

## Run locally

Run:

```bash
python maintest.py
```

The script will read the spreadsheet, identify new rows, summarize them, and email the result.

## Schedule it with PythonAnywhere

If you want the script to run automatically, upload the project to **PythonAnywhere**.

Open a Bash console and install the requirements:

```bash
python -m pip install -r requirements.txt
```

Then go to:

```text
Dashboard -> Tasks
```

Create a scheduled task that runs your script.

For example:

```bash
python /home/YOUR_USERNAME/YOUR_PROJECT/maintest.py
```

If you use a virtual environment, use that environment's Python executable instead.

Example:

```bash
/home/YOUR_USERNAME/.virtualenvs/YOUR_ENV/bin/python /home/YOUR_USERNAME/YOUR_PROJECT/maintest.py
```

Make sure the `.env` and `last_row.txt` files are also available to the script.

### PythonAnywhere note

PythonAnywhere changed scheduled-task availability in 2026. New free accounts may not include scheduled tasks, while paid accounts support them. Check the **Tasks** tab on your account to see what is available.

Also note that free PythonAnywhere accounts restrict outbound internet access to allowlisted services. If Google Sheets, OpenRouter, or Gmail SMTP is blocked for your account, you may need a paid account or another scheduler.

## Security

Never commit these values to GitHub:

- API keys
- Gmail App Password
- Spreadsheet credentials
- `.env`

A safe `.gitignore`:

```text
.env
__pycache__/
*.pyc
```

## Flow

```text
Google Sheet
    |
    v
Detect new rows
    |
    v
OpenRouter AI summary
    |
    v
Gmail SMTP
    |
    v
Email summary
```
