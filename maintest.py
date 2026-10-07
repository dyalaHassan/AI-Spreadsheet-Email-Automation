import smtplib

from googleapiclient.discovery import build 
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os



load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SHEET_NAME = os.getenv("SHEET_NAME")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
def get_spreadsheet_data():
    """fetch spreadsheet daat"""
    service = build('sheets', 'v4', developerKey= GOOGLE_API_KEY)
    all_rows = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range = SHEET_NAME).execute()['values']
    with open("last_row.txt") as file:
        last_row = int(file.read())
    new_rows = all_rows[last_row:]
    headers = all_rows[0]


    return all_rows, new_rows,headers

#######################
def summarize_with_AI(text):
    sytem_prompt = """
    You are a helpful assistant that summarizes spreadsheet data 
    You will recieve new rows that were added tp a Google Spreadsheet.
    Please provide a clear,concise summary of this data"""


    model = ChatOpenAI(
    model="openrouter/free",
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1")
    message = [{"role":"system", "content":sytem_prompt},{"role":"user","content":f"here are the new rows from spreadsheet\n{text}"}]
    response = model.invoke(message).content
    return response

######################
def send_email(subject,body):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.send_message(msg)
    server.quit()
    print(f"email have sent successfully to {RECIPIENT_EMAIL}")
all_rows, new_rows,headers = get_spreadsheet_data()
total_rows = len(all_rows)

with open("last_row.txt", "w") as file:
    file.write(str(total_rows))

message =f"headers: {headers} \n new Rows: {new_rows}"
summary = summarize_with_AI(message)
send_email("dialy spreadsheet information update", summary)
print("SUMMARY", summary)
print ("ALL ROWS", all_rows)
print("New ROWS", new_rows)


