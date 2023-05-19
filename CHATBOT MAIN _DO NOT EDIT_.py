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

loop_start = 7
loop_end = 8

def send_sms(to_number, sms_body):
    # Create an instance of the Twilio client
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    from_number = '+17193949966'
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
    server.login("nolan@blacksprucerealty.com", GMAIL_PASSWORD)

    # Add HTML signature to the email body
    html_signature = '<div style="margin: 0 !important; padding: 0 !important; width: 100% !important;"><div style="font-family: Arial, sens-serif; font-size: 16px; line-height: 1.3; color: #000000;" class="template-template3 is-flipped-true font-family-arial contact-icon-family-outline font-size font-family text-color"><table cellpadding="0" cellspacing="0" border="0" role="presentation" style="border-collapse: collapse !important; font-size: inherit;"><tr><td style="color: #000000; font-weight: 700; font-family: Arial, sens-serif; font-size: 17px;" class="name title-color">Nolan Stephenson</td></tr><tr><td style="padding-top: 4px;"><table cellpadding="0" cellspacing="0" border="0" role="presentation" style="border-collapse: collapse !important; font-size: inherit;"><tr><td style="font-family: Arial, sens-serif; font-size: 16px;" class="job-title">Owner/Broker |</td><td style="padding-left: 8px; font-family: Arial, sens-serif; font-size: 16px;" class="company">Black Spruce Group</td></tr></table></td></tr><tr><td style="padding-top: 10px;"><table cellpadding="0" cellspacing="0" border="0" role="presentation" style="border-collapse: collapse !important; font-size: inherit;"><tr><td><table cellpadding="0" cellspacing="0" border="0" role="presentation" style="border-collapse: collapse !important; font-size: inherit;"><tr><td style="line-height: 0px; padding: 0 5px 0 0;"><img style="border: 0px; height: 24px; line-height: 100%; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; width: 24px;" src="https://woodpecker.co/cdn-cgi/imagedelivery/dbHg18raJkJAbxhrT08asw/f669c002-0bd2-462c-69a1-d6129089a700/public" alt width="24" height="24" /></td><td><a href="mailto:nolan@blacksprucerealty.com" style="color: #000000 !important; text-decoration: underline !important; font-size: 16px !important; font-family: Arial, sens-serif !important; font-weight: inherit !important; line-height: inherit !important;" class="email">nolan@blacksprucerealty.com</a></td></tr></table></td></tr><tr><td style="padding-top: 6px;"><table cellpadding="0" cellspacing="0" border="0" role="presentation" style="border-collapse: collapse !important; font-size: inherit;"><tr><td style="line-height: 0px; padding: 0 5px 0 0;"><img style="border: 0px; height: 24px; line-height: 100%; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; width: 24px;" src="https://woodpecker.co/cdn-cgi/imagedelivery/dbHg18raJkJAbxhrT08asw/bef2635b-c63f-46f3-c865-525638aa7d00/public" alt width="24" height="24" /></td><td><a href="https://www.blacksprucegroup.com" style="color: #000000 !important; text-decoration: underline !important; font-size: 16px !important; font-family: Arial, sens-serif !important; font-weight: inherit !important; line-height: inherit !important;" class="link-color website">blacksprucegroup.com</a></td></tr></table></td></tr><tr><td style="padding-top: 6px;"><table cellpadding="0" cellspacing="0" border="0" role="presentation" style="border-collapse: collapse !important; font-size: inherit;"><tr><td style="line-height: 0px; padding: 0 4px 0 0;"><img style="border: 0px; height: 24px; line-height: 100%; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; width: 24px;" src="https://woodpecker.co/cdn-cgi/imagedelivery/dbHg18raJkJAbxhrT08asw/f0ec7c3e-5957-4157-e09c-22c60ead8300/public" alt width="24" height="24" /></td><td style="font-family: Arial, sens-serif; font-size: 16px;" class="phone">719-334-0783</td></tr></table></td></tr></table></td></tr><tr><td style="padding-top: 17px;"><table cellpadding="0" cellspacing="0" border="0" role="presentation" style="border-collapse: collapse !important; font-size: inherit;"><tr class="social-icon-family-color"><td style="font-size: 0px; line-height: 0px; padding-right: 10px;"><a href="https://www.facebook.com/BlackSpruceGroupRealEstate" style="color: inherit !important; text-decoration: none !important; font-size: inherit !important; font-family: inherit !important; font-weight: inherit !important; line-height: inherit !important;" aria-label="Facebook link" class="facebook"><img style="border: 0px; height: 24px; line-height: 100%; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; width: 24px;" src="https://woodpecker.co/cdn-cgi/imagedelivery/dbHg18raJkJAbxhrT08asw/20068542-1edd-4841-1aa6-78fb537c6c00/public" alt width="24" height="24" class="icon-size" /></a></td><td style="font-size: 0px; line-height: 0px; padding-right: 10px;"><a href="https://www.instagram.com/nolanstephenson_bsg/" style="color: inherit !important; text-decoration: none !important; font-size: inherit !important; font-family: inherit !important; font-weight: inherit !important; line-height: inherit !important;" aria-label="Instagram link" class="instagram"><img style="border: 0px; height: 24px; line-height: 100%; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; width: 24px;" src="https://woodpecker.co/cdn-cgi/imagedelivery/dbHg18raJkJAbxhrT08asw/e08c3c85-eee3-4015-ce04-e0554a00e700/public" alt width="24" height="24" class="icon-size" /></a></td><td style="font-size: 0px; line-height: 0px; padding-right: 10px;"><a href="https://www.youtube.com/channel/UCACFWLhuEQmtZ65GFdd7tsw" style="color: inherit !important; text-decoration: none !important; font-size: inherit !important; font-family: inherit !important; font-weight: inherit !important; line-height: inherit !important;" aria-label="Youtube link" class="youtube"><img style="border: 0px; height: 24px; line-height: 100%; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; width: 24px;" src="https://woodpecker.co/cdn-cgi/imagedelivery/dbHg18raJkJAbxhrT08asw/2e8253e9-1e3c-4d71-e56d-880e1df34500/public" alt width="24" height="24" class="icon-size" /></a></td></tr></table></td></tr><tr><td style="font-size: 0px; line-height: 0px; padding: 16px 0 0 0;"><img style="border: 0px; height: 110px; line-height: 100%; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; width: 110px;" src="https://i.imgur.com/5TiKgoT.png" alt="Email sender photo" width="110" height="110" class="photo photo-size" /></td></tr><tr><td style="padding-top: 10px;"><a href="https://calendly.com/consult-bsg" style="color: #0000FF !important; text-decoration: underline !important; font-size: 20px !important; font-family: Arial, sens-serif !important; font-weight: inherit !important; line-height: inherit !important;" class="link-color website">Let&#39;s Meet! The Coffee is on me! ☕️</a></td></tr></table></td></tr>'

    # Create the email message
    email_body += html_signature
    message = MIMEText(email_body, 'html')
    message['Subject'] = email_subject
    message['From'] = 'nolan@blacksprucerealty.com'
    message['To'] = to_email
    message['Bcc'] = 'nolan@blacksprucerealty.com'

    # Send the email message
    server.sendmail('nolan@blacksprucerealty.com', to_email, message.as_string())
    server.quit()

# Function that will send me a SMS and Email if a Lead is unresponsive
def alert_me(fname, lname, email, to_number,
             initial_search, tag, bed_cri, bath_cri,
             area_cri, sqft_cri, budget_cri):
    sms_body = f'*{fname} {lname}* was UNRESPONSIVE\n' \
               f'Phone: {to_number}'
    send_sms(+17193340783, sms_body)

# This is the initial start of the convo after lead signs up on site
def initial_convo(fname, lname, email, to_number,
                 initial_search,tag, bed_cri, bath_cri,
                 area_cri, sqft_cri, budget_cri, row_data, i, num_rows):

    print(f'sending new message to {fname}')
    send_sms('+17193340783', f'NEW LEAD and below is their info: \n\n'
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
    send_sms(to_number, f"Hi {fname}, my name is Dana and I am the Customer Success Manager with Black Spruce Group. \n\n"
                        f"First off, we would like to say thank you for signing up on our website 🙂 In order to serve "
                        f"you better I'd like to ask you a few questions in regards to your home search.\n\n"
                        f"Firstly, what has you in the market looking for a home?")
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
                        send_sms(to_number, f"We understand that you may be early in the process of buying a home {fname}, "
                                            f"and we want to be able to help you find the perfect place! \n\n"
                                            f"I'll be on standby should you have any questions!")
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
                        send_sms(to_number, f"Almost forgot! Nolan is doing a really awesome deal right now with buyers "
                                            f"where, when you work with him as your Realtor, he will give you $2,500 back as "
                                            f"a rebate and as a thanks!")
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
                send_sms(to_number, f"{fname}, I am well versed with our searching tool and am more than"
                                    f" happy to set you up with a search that will automatically send you listings daily, biweekly, or really"
                                    f"whatever works best for you! Let me know how we can better serve you in the home buying journey.\n\n "
                                    f"-Dana")
                all_leads_sheet.update_cell(num_rows, 10, 'C')
                send_email(email, f"{fname}'s Home Search", f'Hello {fname},</p><p>'
                                  f'</p><p>'
                                  f'Thank you for filling out the contact form on my website in order to gain access to the search tool.</p><p>'
                                  f'</p><p>'
                                  f'My name is Nolan Stephenson and I am the owner of Black Spruce Group and would just like to introduce myself and make sure you are aware '
                                  f'that I am available to assist you and answer any questions or concerns you may have as it relates to the '
                                  f'home buying process.</p><p>'
                                  f'</p><p>'
                                  f'Here is my contact info:</p><p>'
                                  f'Cell -- (719) 334-0783</p><p>'
                                  f'Email -- Nolan@BlackSpruceRealty.com</p><p>'
                                  f'</p><p>'
                                  f'I am free to chat, so feel free to give me a shout!</p><p>'
                                  f'-Nolan</p><p>')
                alert_me(fname, lname, email, to_number,
                         initial_search, tag, bed_cri, bath_cri,
                         area_cri, sqft_cri, budget_cri)
                exit()
            else:
                pass

def dialogflow_response(to_number, response):
    DIALOGFLOW_PROJECT_ID = 'rechatbot4you'
    SESSION_ID = 'me'



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
