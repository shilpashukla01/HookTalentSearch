import smtplib
from email.mime.text import MIMEText

sender = 'hooktalentsearch@gmail.com'
recepients = 'arati.mahimane@hooklogic.com, shilpa.shukla@hooklogic.com'
textfile = 'file.txt'

def send():

    # TODO send in HTML format instead of text
    fp = open(textfile, 'rb')
    msg = MIMEText(fp.read())
    fp.close()

    msg['Subject'] = 'HookTalentSearch: Top 10 Matching Profiles from GitHub'
    msg['From'] = sender
    msg['To'] = recepients

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()

    # TODO store credentials somewhere
    s.login('hooktalentsearch', '')
    s.sendmail(sender, [recepients], msg.as_string())
    s.quit()