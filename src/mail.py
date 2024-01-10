from .student import Student
from . import globals

from enum import Enum
import ssl
import smtplib

class EmailType(Enum):
    ON_REGISTER = 0
    ON_FIRST = 1
    ON_FIFTH = 2
    # ON_EMERGENCY

port = 465

context = ssl.create_default_context()

message_template = """\
From: "SJA Jeju Waiting List" <{sender_email}>
Subject: {subject}

--- Student Info ---
{student_description}
--------------------

{content}
"""


# https://realpython.com/python-send-email/
def send_email(student: Student, email_type: EmailType):
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(globals.google_id, globals.google_password)

        student_description = f'Name: {student.name}\nGrade: {student.grade}'

        match email_type:
            case EmailType.ON_REGISTER:
                message = message_template.format(
                    sender_email=globals.google_id,
                    subject='Registration Success',
                    content='Registration Success',
                    student_description=student_description
                )
            case EmailType.ON_FIRST:
                message = message_template.format(
                    sender_email=globals.google_id,
                    subject='Enter Office',
                    content='Enter Office',
                    student_dscription=student_description
                )
            case EmailType.ON_FIFTH:
                message = message_template.format(
                    sender_email=globals.google_id,
                    subject='Wait in front',
                    content='Wait in front',
                    student_description=student_description
                )
        
        server.sendmail(globals.google_id, student.email, message)
