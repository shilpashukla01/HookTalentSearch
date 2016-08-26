import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def send():

    sender = 'hooktalentsearch@gmail.com'
    recepients = 'arati.mahimane@hooklogic.com, shilpa.shukla@hooklogic.com'
    textfile = 'file.html'

    # Create message container.
    msgRoot = MIMEMultipart()
    msgRoot['Subject'] = 'HookTalentSearch: Matching Profiles'
    msgRoot['From'] = sender
    msgRoot['To'] = recepients

    fp = open(textfile, 'rb')
    msgText = MIMEText(fp.read())
    fp.close()

    # Create the body of the message.
    html = """\
        <body style='background-color:#e6e6ff;'>
        <p><br/>&nbsp
            <img src="cid:image1" height="120" width="600">
        </p>
        <p> {} </p>
    """.format(msgText.get_payload())

    # Record the MIME types.
    msgHtml = MIMEText(html, 'html')
    img = open('HookTalentSearch.png', 'rb').read()
    msgImg = MIMEImage(img, 'png')
    msgImg.add_header('Content-ID', '<image1>')
    msgImg.add_header('Content-Disposition', 'inline', filename='HookTalentSearch.png')

    msgRoot.attach(msgHtml)
    msgRoot.attach(msgImg)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()

    # TODO store credentials somewhere
    s.login('hooktalentsearch', '')
    s.sendmail(sender, [recepients], msgRoot.as_string())
    s.quit()

if __name__ == "__main__":
        send()