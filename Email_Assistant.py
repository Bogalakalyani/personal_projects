import imaplib
import email
import pyttsx3
import re
import smtplib

def main():
    """
    If you are getting the following error:
    imaplib.IMAP4.error: b'[ALERT] Application-specific password required: https://support.google.com/accounts/answer/185833 (Failure)'
    you need to generate an application-specific password to access your Gmail account using IMAP.
    """
    try:
        # asking user for input
        name = input("Username:").lower()
        password = input("Password:")
        mail = fetch_unread_emails(name,password)
        try:
            priority = sort_emails_by_priority(mail[0],mail[1])
            if len(priority) != 0:
                question = input("Do you want me to read emails for you: ")
                if question.lower() == "yes":
                    convert_emails_to_speech(priority)
            else:
                print("you have no importent mails today")
        except:
            print("you have no unread messages")
        try:
            question2 = input("Do you want to send emails:").lower()
            if question2 == "yes":
                sending_emails(name,password)
        except smtplib.SMTPException:
            print("Error: Failed to authenticate with the email server.")
    except imaplib.IMAP4.error:
        print("Error: Failed to authenticate with the email server.")

#reading emails from the inbox
def fetch_unread_emails(username, password):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username, password)
    mail.select('inbox')
    status, response = mail.search(None, 'UNSEEN')
    unread_messages = response[0].split()
    return [mail, unread_messages]

#sorting emails by using the priority
def sort_emails_by_priority(mail, unread_messages):
    important = [
        "username1@gmail.com",
        "username2@gamil.com",
        "username3@gmail.com"
        ]
    emails = []
    for num in unread_messages:
        _, response = mail.fetch(num, '(RFC822)')
        email_data = response[0][1]
        message = email.message_from_bytes(email_data)
        for msg_part in message.walk():
            if msg_part.get_content_type() == "text/plain":
                message["Body"] = msg_part.get_payload(decode=False)
                body = message["body"]
    sender_with_name = message['From']
    sender = re.search(r"<(.+)>",sender_with_name).group(1)
    subject = message['Subject']
    if sender in important:
        emails.append({'sender': sender, 'subject': subject, 'body': body})
    elif subject:
        if "urgent" in subject.lower():
            emails.append({'sender': sender, 'subject': subject, 'body': body})
        
    return emails

#coverting text to voice message
def convert_emails_to_speech(emails):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    engine.setProperty("rate",120)
    for i,email in enumerate(emails):
        index = i + 1
        if index  == 1:
            ordinal = str(index) + "st"
        elif index  == 2:
            ordinal = str(index) + "nd"
        elif index  == 3:
            ordinal = str(index) + "rd"
        else:
            ordinal = str(index) + "th"
        if email['subject'] == "":
            email['subject'] = "There is no subject for this email."
            engine.say(f"this is the {ordinal} mail in today's importent mails")
            engine.say(f"You have an email from {email['sender']}. {email['subject']}. The message is {email['body']}")
        else:    
            engine.say(f"this is the {ordinal} mail in today's importent mails")
            engine.say(f"You have an email from {email['sender']}. The subject is {email['subject']}. The message is {email['body']}")
    engine.runAndWait()

def sending_emails(username,password):
    from_adress = input("From:")
    to_adress = input("To:")
    message = input("Message:")
    connection = smtplib.SMTP('smtp.gmail.com')
    connection.login(username,password)
    connection.starttls()
    connection.sendmail(from_adress,to_adress,message)
    print("message sent")
    connection.quit()



if __name__ == "__main__":
    main()



