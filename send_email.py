import smtplib


def sendMail(to, subject, body):
    userPwd = {}
    with open("mailLogin.txt") as f:
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

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(userPwd['id'], userPwd['pwd'])
    server.sendmail(sent_from, to, email_text)
    server.close()