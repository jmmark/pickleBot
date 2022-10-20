import smtplib


def sendMail(to, subject, body):
    userPwd = {}
    with open("mailLoginhm.txt") as f:
        for line in f:
            (key, val) = line.split()
            userPwd[key] = val

    sent_from = userPwd['id']
    email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(userPwd['id'], userPwd['pwd'])
    server.sendmail(sent_from, to, email_text)
    server.close()