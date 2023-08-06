import smtplib
import configparser
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# This function configures the credentials required 
# for sending emails. Check config.ini for this
def configure_email(fromEmail, toEmail, password):
    '''
    This function configures the credentials required for sending emails. Check config.ini for this
    '''
    config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.ini")
    config = configparser.ConfigParser()
    try:
        config.read(config_file_path)
    except Exception as err:
        raise Exception(err)
        
    status = ""
    try:
        config['EMAIL-SETUP']['FromEmail'] = fromEmail
        config['EMAIL-SETUP']['ToEmail'] = toEmail
        config['EMAIL-SETUP']['Password'] = password
        with open(config_file_path, 'w') as configfile:
            config.write(configfile)
        status = True
    except Exception as err:
        print(err)
        status = False
    
    return status


# This function is responsible for sending the email 
# Make sure that the sender's email account is configured to... 
# ..... allow login from these kind of applications
def send_mail(subject = "Function Test", message = "Did you really doubt this function?"):
    '''
    This function is responsible for sending the email. Make sure that the sender's email account is configured to allow login from these kind of applications
    '''
    config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.ini")
    msg = MIMEMultipart()
    # print(config_file_path)
    # # Configure the email credentials
    config = configparser.ConfigParser()
    config.read(config_file_path)
    # print(config.sections())
    # print(config.get('EMAIL-SETUP','HOST'))
    fromEmail = config['EMAIL-SETUP']['FromEmail']
    password = config['EMAIL-SETUP']['Password']
    msg['From'] = config['EMAIL-SETUP']['FromEmail']
    msg['To'] = config['EMAIL-SETUP']['ToEmail']
    msg['Subject'] = subject
    msg.attach(MIMEText(message,'plain'))
    # with open(config_file_path, 'w') as configfile:
    #     config.write(configfile)

    try:
        s = smtplib.SMTP_SSL(host=config['EMAIL-SETUP']['Host'], port=config['EMAIL-SETUP']['Port'])
    except Exception as err:
        raise smtplib.SMTPConnectError(err)
    
    try:
        # print(fromEmail, password)
        s.login(fromEmail, password)
    except Exception as err:
        raise smtplib.SMTPAuthenticationError("Unable to sign in.", err)
        # print("Error while signing-in:", err)
    try:
        s.send_message(msg)
    except Exception as err:
        raise smtplib.SMTPSenderRefused(err)
        # print("Error while sending mail: ",err)
    s.quit()

# send_mail()