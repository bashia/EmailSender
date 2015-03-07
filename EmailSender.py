import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import senderinfo

class Person:

    def __init__(self,lastname,firstname,email):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email

def loadpeople(filename): #'emails.csv'
    people = []
    with open(filename, 'rU') as f:
        reader = csv.reader(f,dialect="excel")
        for row in reader:
            if not "@" in row[3]:
                continue
            newperson = Person(row[0],row[1],row[3])
            people.append(newperson)

    return people

def formatmessage(html,name):


    return html.replace("^name^",name)

def FiletoString(filepath): #message.html
    string = ""
    with open(filepath, 'rU') as html:
        string = html.read()
    return string

def sendmail(sender,people,html,text,subject): #dougmcarthur.sfu@gmail.com,
    fromaddr = sender.address
    username = sender.address
    password = sender.password
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username,password)

    for person in people:
        toaddrs = person.email
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = fromaddr
        msg['To'] = person.email

        #htmlcomp = formatmessage(html,person.firstname)
        htmltxt = formatmessage(text,person.firstname)
        #htmlbody = MIMEText(htmlcomp,'html')
        txtbody = MIMEText(htmltxt,'html')
        #msg.attach(htmlbody)
        msg.attach(txtbody)

        htmltxt = "From: "+sender.name +" <"+ sender.address +">\r\n" + "To: " + person.firstname + " " + person.lastname +"<" + person.email + ">\r\n" + "Subject: " + subject + "\r\n\r\n" + htmltxt


        server.sendmail(fromaddr, toaddrs, htmltxt) #Ignoring smtplib message format for now- just get a plaintext out!
    server.quit()

sender = senderinfo.sender
html = FiletoString("message.html")
text = FiletoString("messagetext.txt")
people = loadpeople("emails.csv")


subject = "Re: Murray Rankin"

sendmail(sender,people,html,text,subject)
