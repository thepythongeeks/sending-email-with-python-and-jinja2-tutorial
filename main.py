# -*- coding: utf-8 -*-
import smtplib, ssl
import mimetypes

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

import six
from pyfiglet import figlet_format
from PyInquirer import (Token, ValidationError, Validator, print_json, prompt,
                        style_from_dict)

try:
    from termcolor import colored
except ImportError:
    colored = None

style = style_from_dict({
    Token.QuestionMark: '#fac731 bold',
    Token.Answer: '#4688f1 bold',
    Token.Instruction: '',
    Token.Separator: '#cc5454',
    Token.Selected: '#0abf5b',
    Token.Pointer: '#673ab7 bold',
    Token.Question: '',
})

PLAINT_TEXT_EMAIL = """
    Hi there,

    This message is sent from Python Geeks.

    Have a good day!
"""

def get_email_info():
    questions = [
        {
            'type': 'list',
            'name': 'smtp_server',
            'message': 'What is your SMTP server?',
            'choices': ['smtp.gmail.com (Gmail)'],
            'filter': lambda x: x.split(' ')[0].lower()
        },
        {
            'type': 'list',
            'name': 'smtp_protocol',
            'message': 'What is your SMTP protocol?',
            'choices': ['SSL (Port: 465)', 'TLS (Port: 587)'],
            'filter': lambda x: x.split(' ')[0].lower()
        },
        {
            'type': 'input',
            'name': 'smtp_account',
            'message': 'SMTP Login Account'
        },
        {
            'type': 'password',
            'name': 'smtp_password',
            'message': 'SMTP Login Password'
        },
        {
            'type': 'list',
            'name': 'example_no',
            'message': 'Which example do you want to run?',
            'choices': [
                '1. Plant-Text Email',
                '2. HTML Email',
                '3. Email With Attachment',
            ],
            'filter': lambda x: x.split('.')[0]
        },
        {
            'type': 'input',
            'name': 'from_email',
            'message': 'From Email',
            'when': lambda answers: answers.get("example_no", ''),
        },
        {
            'type': 'input',
            'name': 'to_email',
            'message': 'To Email',
            'when': lambda answers: answers.get("example_no", ''),
        },
        {
            'type': 'input',
            'name': 'subject',
            'message': 'Subject',
            'when': lambda answers: answers.get("example_no", ''),
        },
    ]

    answers = prompt(questions, style=style)
    return answers

def get_html_message(from_email, to_email, subject):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    # Plain-text version of content
    plain_text = """\
        Hi there,

        This message is sent from Python Geeks.
        Visit us here https://pythongeeks.net

        Have a good day!
    """
    # html version of content
    html_content = """\
        <html>
        <head></head>
        <body>
            <p>Hi there,</p>
            <p>This message is sent from Python Geeks.</p>
            <p>Visit us here 
                <a href="https://pythongeeks.net">
                    Python Geeks
                </a>
            </p>
        </body>
    </html>
    """
    text_part = MIMEText(plain_text, 'plain')
    html_part = MIMEText(html_content, 'html')
    msg.attach(text_part)
    msg.attach(html_part)
    return msg

def get_attachment_message(from_email, to_email, subject):
    msg = get_html_message(from_email, to_email, subject)
    # Define MIMEImage part
    # Remember to change the file path
    file_path = './assets/level_up_your_python.png'
    ctype, encoding = mimetypes.guess_type(file_path)
    maintype, subtype = ctype.split('/', 1)
    with open(file_path, 'rb') as fp:
        img_part = MIMEImage(fp.read(), _subtype=subtype)
        # Set the filename for the attachment
        img_part.add_header('Content-Disposition', 'attachment', filename='level_up_your_python')
        msg.attach(img_part)
    return msg

def cli_print(string, color, font="slant", figlet=False):
    if colored:
        if not figlet:
            six.print_(colored(string, color))
        else:
            six.print_(colored(figlet_format(
                string, font=font), color))
    else:
        six.print_(string)

def send_email(email_info):
    smtp_server = email_info.get('smtp_server', '')
    protocol = email_info.get('smtp_protocol', '')
    username = email_info.get('smtp_account', '')
    password = email_info.get('smtp_password', '')
    example_no = email_info.get('example_no', '')
    from_email = email_info.get('from_email', '')
    to_email = email_info.get('to_email', '')
    subject = email_info.get('subject', '')

    # Create a secure SSL context
    context = ssl.create_default_context()

    cli_print("********************************************", "green")

    try:
        if protocol == 'ssl':
            port = 465
            server = smtplib.SMTP_SSL(smtp_server, port, context=context)
            cli_print("Connecting to SMTP Server By Using SSL...", "green")
            server.login(username, password)
        elif protocol == 'tls':
            port = 587
            server = smtplib.SMTP(smtp_server, port)
            cli_print("Connecting to SMTP Server  By Using TLS...", "green")
            server.starttls(context=context) # Secure the connection with TLS
            server.login(username, password)
    except Exception as e:
        cli_print("Could not connect to SMTP server with exception: %s" % e, "red")
    else:
        cli_print("Sending your email...", "green")
        if example_no == '1':
            body = PLAINT_TEXT_EMAIL
            server.sendmail(from_email, to_email, body)
        elif example_no == '2':
            msg = get_html_message(from_email, to_email, subject)
            server.send_message(msg)
        elif example_no == '3':
            msg = get_attachment_message(from_email, to_email, subject)
            server.send_message(msg)
        cli_print("Your email was sent...", "green")
    finally:
        server.quit()

def main():
    """
    Simple CLI for sending emails with Python
    """
    cli_print("Sending Email CLI", color="blue", figlet=True)
    cli_print("*** Welcome to Sending Email With Python***", "green")

    email_info = get_email_info()
    send_email(email_info)


if __name__ == "__main__":
    main()
