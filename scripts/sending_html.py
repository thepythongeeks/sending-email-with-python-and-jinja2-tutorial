import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

password = input("Your password: ")
context = ssl.create_default_context()

msg = MIMEMultipart('alternative')
msg['Subject'] = "[Python Geeks] Sending Email With Python"
msg['From'] = "test@pythongeeks.net"
msg['To'] = "receiver@pythongeeks.net"
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

with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login("test@pythongeeks.net", password)
    server.send_message(msg)