from .student import Student
from . import globals

from enum import Enum
import ssl
import smtplib

class EmailType(Enum):
    ON_REGISTER = 0
    ON_FIRST = 1
    ON_TENTH = 2
    ON_EMERGENCY = 3

port = 465

context = ssl.create_default_context()
server =  smtplib.SMTP_SSL("smtp.gmail.com", port, context=context)
server.login(globals.google_id, globals.google_password)

message_template = """\
From: "SJA Jeju Waiting List" <{sender_email}>
Subject: {subject}

--- Student Info ---
{student_description}
--------------------

{content}
You must check with your current teacher before coming down to the office. There is no add /drop during lunch
"""


# https://realpython.com/python-send-email/
def send_email(student: Student, email_type: EmailType, content: str):
    student_description = f'Name: {student.name}\nGrade: {student.grade}'

    match email_type:
        case EmailType.ON_REGISTER:
            message = message_template.format(
                sender_email=globals.google_id,
                subject='Registration Success',
                content=content,
                student_description=student_description
            )
        case EmailType.ON_FIRST:
            message = message_template.format(
                sender_email=globals.google_id,
                subject='Wait in front of the office',
                content=content,
                student_description=student_description
            )
        case EmailType.ON_TENTH:
            message = message_template.format(
                sender_email=globals.google_id,
                subject='Lineup in the office',
                content=content,
                student_description=student_description
            )
        case EmailType.ON_EMERGENCY:
            message = message_template.format(
                sender_email=globals.google_id,
                subject='Come to the office (Emergency)',
                content=content,
                student_description=student_description
            )
    
    server.sendmail(globals.google_id, student.email, message)
