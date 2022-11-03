import smtplib
import imaplib
import easyimap as imap

EMAIL_ADDRESS = 'noreply.piservice@gmail.com' #piservice! or Piservice!
PASSWORD = 'bvlg sbug wars xozh'
RECEIVER_ADDRESS = 'tonynadeau03@gmail.com'
NOT_REFUSED = True

def send_email(subject, body):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADDRESS, PASSWORD)
        msg = f'Subject: {subject}\n\n{body}'
        smtp.sendmail(EMAIL_ADDRESS, RECEIVER_ADDRESS, msg)


# Method to delete email
def delete_email():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(EMAIL_ADDRESS, PASSWORD)

    mail.select("inbox")
    # typ, data = mail.search(None, 'SUBJECT "hello"')  # Filter by subject
    # typ, data = mail.search(None, 'FROM "example@gmail.com"')  # Filter by sender
    # typ, data = mail.search(None, 'SINCE "015-JUN-2020"')  # Filter by date
    typ, data = mail.search(None, "ALL")  # Filter by all

    for num in data[0].split():
        mail.store(num, '+FLAGS', r'(\Deleted)')

    mail.expunge()
    mail.close()
    mail.logout()


# Method to receive email
def receive_email():
    global NOT_REFUSED
    server = imap.connect('imap.gmail.com', EMAIL_ADDRESS, PASSWORD)

    for mail in server.listids():
        email = server.mail(mail)
        response =  (email.title + " " + email.body).lower()
        if "yes" in response:
            delete_email()
            return True
        elif "no" in response:
            NOT_REFUSED = False
    else:
        server.quit()
        delete_email()
        return False