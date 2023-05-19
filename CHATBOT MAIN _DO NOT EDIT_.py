# Import necessary packages
import gspread
# import flask
# from flask import request, jsonify
import dotenv
import os
from twilio.rest import Client
import threading
import time
import smtplib
from email.mime.text import MIMEText
from google.cloud import dialogflow_v2beta1 as dialogflow
# pip install --upgrade google-cloud-dialogflow
from google.api_core.exceptions import InvalidArgument


# Load the .env file
dotenv.load_dotenv('.env')

# Set up the authorization to Google Sheets
sa = gspread.service_account('sheets.json')

# Load the spreadsheet
wb = sa.open('Leads')

# All Leads Sheet
all_leads_sheet = wb.get_worksheet(0)

# Get the credentials from the .env file
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')

# Dialogflow Settings
# DIALOGFLOW_PROJECT_ID = 'rechatbot4you'
# SESSION_ID = 'me'
# session_client = dialogflow.SessionsClient()
# session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

# Set up Twilio Client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_sms(to_number, sms_body):
    # Create an instance of the Twilio client
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    from_number = 'TWILIO NUMBER'
    # Send the SMS message
    text = client.messages.create(
        to=to_number,
        from_= from_number,
        body=sms_body
    )

def send_email(to_email, email_subject, email_body):
    # Create an instance of the email client
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("YOUR EMAIL", GMAIL_PASSWORD)

    # Add HTML signature to the email body
    html_signature = 'HTML EMAIL SIGNATURE'

    # Create the email message
    email_body += html_signature
    message = MIMEText(email_body, 'html')
    message['Subject'] = email_subject
    message['From'] = 'YOUR EMAIL'
    message['To'] = to_email
    message['Bcc'] = 'YOUR EMAIL'

    # Send the email message
    server.sendmail('YOUR EMAIL', to_email, message.as_string())
    server.quit()

# Function that will send me a SMS and Email if a Lead is unresponsive
def alert_me(fname, lname, email, to_number,
             initial_search, tag, bed_cri, bath_cri,
             area_cri, sqft_cri, budget_cri):
    sms_body = f'*{fname} {lname}* was UNRESPONSIVE\n' \
               f'Phone: {to_number}'
    send_sms(+'YOUR PHONE NUMBER', sms_body)

# This is the initial start of the convo after lead signs up on site
def initial_convo(fname, lname, email, to_number,
                 initial_search,tag, bed_cri, bath_cri,
                 area_cri, sqft_cri, budget_cri, row_data, i, num_rows):

    print(f'sending new message to {fname}')
    send_sms('YOUR PHONE NUMBER GOES HERE', f'NEW LEAD and below is their info: \n\n'
                             f'*{fname} {lname}*\n'
                             f'Phone: {to_number}\n'
                             f'Email: {email}\n'
                             f'initial search: {initial_search}\n\n'
                             f'CRITERIA if applicable\n'
                             f'Beds: {bed_cri}\n'
                             f'Baths: {bath_cri}\n'
                             f'Community: {area_cri}\n'
                             f'SQ FT: {sqft_cri}\n'
                             f'Budget: {budget_cri}\n\n'
                             f'That is all, love, yourself!\n'
                             f'-Nolan ;)')
    time.sleep(10)
    send_sms(to_number, f"FILL THIS WITH AN INITIAL TEXT MESSAGE PERHAPS WELCOMING THE LEAD TO YOUR SITE ETC.")
    start_time = time.time()
    while True:
        messages = client.messages.list(limit=50)
        if time.time() <= start_time + 20:
            for message in messages:
                if message.direction == 'inbound' and message.from_ == f'+1{to_number}':
                    all_leads_sheet.update_cell(num_rows, 10, 'B')

                    response = message.body
                    # Start Dialogflow conversation
                    criteria_appt_convo(fname, lname, email, to_number,
                                        initial_search, tag, bed_cri, bath_cri,
                                        area_cri, sqft_cri, budget_cri, row_data, i, response)
                    exit()
                else:
                    if time.time() == start_time + 20:
                        send_sms(to_number, f"MESSAGE HERE AFTER 20 SECONDS of NO RESPONSE FROM THE LEAD")
                    else:
                        pass

        elif time.time() > start_time + 20 and time.time() <= start_time + 80:
            for message in messages:
                if message.direction == 'inbound' and message.from_ == f'+1{to_number}':
                    all_leads_sheet.update_cell(num_rows, 10, 'B')

                    response = message.body
                    # Start Dialogflow conversation
                    criteria_appt_convo(fname, lname, email, to_number,
                                        initial_search, tag, bed_cri, bath_cri,
                                        area_cri, sqft_cri, budget_cri, row_data, i, response)

                    exit()
                else:
                    if time.time() == start_time + 80:
                        send_sms(to_number, f"MESSAGE HERE AFTER 80 SECONDS of NO RESPONSE FROM THE LEAD")
                    else:
                        pass

        elif time.time() > start_time + 80 and time.time() <= start_time + 200:
            for message in messages:
                if message.direction == 'inbound' and message.from_ == f'+1{to_number}':
                    all_leads_sheet.update_cell(num_rows, 10, 'B')

                    response = message.body
                    # Start Dialogflow conversation
                    criteria_appt_convo(fname, lname, email, to_number,
                                        initial_search, tag, bed_cri, bath_cri,
                                        area_cri, sqft_cri, budget_cri, row_data, i, response)
                    exit()
        else:
            if time.time() > start_time + 200:
                send_sms(to_number, f"MESSAGE HERE AFTER 200 SECONDS of NO RESPONSE FROM THE LEAD")
                all_leads_sheet.update_cell(num_rows, 10, 'C')
                send_email(email, f"AN EMAIL MESSAGE YOU WOULD WANT TO SEND OUT TO YOUR NEW LEAD IF THEY HAVE NOT RESPONDED TO THE AUTOMATED TEXT MESSAGES')
                alert_me(fname, lname, email, to_number,
                         initial_search, tag, bed_cri, bath_cri,
                         area_cri, sqft_cri, budget_cri)
                exit()
            else:
                pass

def dialogflow_response(to_number, response):
    DIALOGFLOW_PROJECT_ID = 'NAME OF YOUR PROJECT ID W/IN DIALOGFLOW'
    SESSION_ID = 'SESSION_ID'



    text_to_be_analyzed = response
    print(response)
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code='en')
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
        # print(f'query score: {response.query_result.intent_detection_confidence}')
        if response.query_result.intent_detection_confidence >= 0.2:
            # print(f'intent: {response.query_result.intent.display_name}')
            # print(response)
            # print(f'fulfillment text: {response.query_result.fulfillment_text}')
            send_sms(to_number, response.query_result.fulfillment_text)
    except:
        pass
    time.sleep(5)


# This is the second stage of the convo that will route through dialogflow after initial response from lead
def criteria_appt_convo(fname, lname, email, to_number,
                        initial_search,tag, bed_cri, bath_cri,
                        area_cri, sqft_cri, budget_cri, row_data, i, response):
    # dialogflow_response(to_number, response)

    while True:
        # start_time = time.time()
        messages = client.messages.list(limit=1)
        for message in messages:
            if message.direction == 'inbound' and message.from_ == f'+1{to_number}':
                response = message.body
                text_analyzed = response
                dialogflow_response(to_number, text_analyzed)
                # send_sms('+17193340783', f'{fname} said: {text_analyzed}')
                time.sleep(5)

# Main function that will loop through Google Sheets for new leads every 1 minute
def func():
    while True:
        # Could put time parameters in here in order for the loop to break out
        # and then you could save the loop_start variable to a Pickle Object
        # print('Looking for new leads....')
        time.sleep(60)
        row_data = all_leads_sheet.get_all_values()
        num_rows = len(row_data)
        for i in range(num_rows-1, num_rows):
            row_data = all_leads_sheet.get_all_values()
            if row_data[i][9] == 'NEW_LEAD':
                # Grab Column Values to be used in other functions
                fname = row_data[i][2]
                lname = row_data[i][3]
                email = row_data[i][4]
                to_number = row_data[i][5]
                initial_search = row_data[i][6]
                tag = row_data[i][9]
                bed_cri = row_data[i][10]
                bath_cri = row_data[i][11]
                area_cri = row_data[i][12]
                sqft_cri = row_data[i][13]
                budget_cri = row_data[i][14]

                all_leads_sheet.update_cell(num_rows, 10, 'contacted')
                x = threading.Thread(target=initial_convo, args=(fname, lname, email, to_number, initial_search,
                                                                tag, bed_cri, bath_cri, area_cri, sqft_cri, budget_cri, row_data, i, num_rows))
                x.start()



# Run the program!!!
func()
