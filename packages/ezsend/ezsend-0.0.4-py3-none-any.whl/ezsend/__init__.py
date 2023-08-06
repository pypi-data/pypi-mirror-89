import smtplib, sys, re, time
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
def add(email, password, accountname):
    if not (re.search(regex,email)):
            print("Invalid Email")
            sys.exit()
    file = open(accountname + '.txt', 'w')
    file.write(email)
    file.close()
    filep = open(accountname + 'password.txt', 'w')
    filep.write(password)
    filep.close()
def send(accountname, subject, body, time, *argv):
    if not (re.search(regex,arg)):  
        print("Invalid Email")  
        sys.exit()
    try:
        fileo = open(accountname + '.txt')
        email = fileo.read()
        fileop = open(accountname + 'password.txt')
        password = fileop.read()
    except:
        print('Error getting credentials')
    if '@gmail.com' in email:
        smtpserver = 'smtp.gmail.com'
    elif '@icloud.com' in email:
        smtpserver = 'smtp.mail.me.com'
    elif '@outlook.com' in email:
        smtpserver = 'smtp.live.com'
    elif '@hotmail.com' in email:
        smtpserver = 'smtp.live.com'
    elif '@msn.com' in email:
        smtpserver = 'smtp.live.com'
    elif '@yahoo.com' in email:
        smtpserver = 'smtp.mail.yahoo.com'
    else:
        print('Email provider not yet supported')
        sys.exit()
    if not time == '':
        time.sleep(time)
    smtpObj = smtplib.SMTP(smtpserver, 587)
    smtpObj.starttls()
    smtpObj.ehlo()
    try:
        smtpObj.login(email, password)
    except:
        print('Login Error')
        sys.exit()
    smtpObj.sendmail(email, arg, (f'Subject: {subject}\n{body}'))
def text(accountname, carrier, subject, body, time, *argv):
    try:
        fileo = open(accountname + '.txt')
        email = fileo.read()
        fileop = open(accountname + 'password.txt')
        password = fileop.read()
    except:
        print('Error getting credentials')
    if '@gmail.com' in email:
        smtpserver = 'smtp.gmail.com'
    elif '@icloud.com' in email:
        smtpserver = 'smtp.mail.me.com'
    elif '@outlook.com' in email:
        smtpserver = 'smtp.live.com'
    elif '@hotmail.com' in email:
        smtpserver = 'smtp.live.com'
    elif '@msn.com' in email:
        smtpserver = 'smtp.live.com'
    elif '@yahoo.com' in email:
        smtpserver = 'smtp.mail.yahoo.com'
    else:
        print('Email provider not yet supported')
        sys.exit()
    if carrier.lower() == 'verizon':
        carrier = '@vtext.com'
    elif carrier.lower() == 'at&t':
        carrier = '@txt.att.net'
    elif carrier.lower() == 'sprint':
        carrier = '@messaging.sprintpcs.com'
    elif carrier.lower() == 't-mobile':
        carrier = '@tmomail.net'
    else :
        print('Carrier not listed YET')
        sys.exit()
    receiversphone = arg + carrier
    if not time == '':
        time.sleep(time)
    smtpObj = smtplib.SMTP(smtpserver, 587)
    smtpObj.starttls()
    smtpObj.ehlo()
    try:
        smtpObj.login(email, password)
    except:
        print('Error logging in')
        sys.exit()
    smtpObj.sendmail(email, receiversphone, (f'Subject: {subject}\n{body}'))
    
    
    
    
            
