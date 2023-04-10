# email_assistant

The given code is a Python script that reads emails from the Gmail inbox and performs certain actions based on the content of those emails. The script uses several libraries such as imaplib, email, pyttsx3, and re to achieve its functionality.

The main() function is the entry point of the script. It prompts the user for their Gmail username and password and then calls the fetch_unread_emails() function to fetch all the unread emails from the user's Gmail inbox. It then sorts the emails by their priority level using the sort_emails_by_priority() function and reads them out loud using the convert_emails_to_speech() function.

The fetch_unread_emails() function uses the imaplib library to connect to the Gmail IMAP server and fetches all the unread emails from the inbox. It returns a tuple containing the IMAP4_SSL object and a list of message IDs for the unread emails.

The sort_emails_by_priority() function takes the IMAP4_SSL object and the list of message IDs as input and sorts the emails based on their priority. It first extracts the sender's email address, subject, and body from each email message and then checks if the sender's email address is in the list of important senders or if the email subject contains the word "urgent". If either of these conditions is true, the email is considered important and added to a list of important emails.

The convert_emails_to_speech() function takes a list of important emails and uses the pyttsx3 library to convert each email to a speech message. It first initializes the pyttsx3 engine and sets the voice and rate properties of the engine. It then loops through the list of emails, extracts the email sender, subject, and body, and reads them out loud using the pyttsx3 engine.

The script also includes a sending_emails() function that allows the user to send emails from their Gmail account. It prompts the user for the from address, to address, and message content and uses the smtplib library to send the email.

To run the script, the user needs to have Python and the required libraries installed on their system. They can then run the script using a Python interpreter or an IDE that supports Python. The script prompts the user for their Gmail username and password and then performs the required actions based on the content of the user's Gmail inbox.

If you have any suggestions for improvements or new features to add to this application, feel free to submit a pull request.
