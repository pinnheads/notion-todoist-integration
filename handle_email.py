import os
import datetime as dt
import smtplib

msg_txt = ""


class HandleEmail:
    def __init__(self):
        self.my_email = os.environ["MY_EMAIL"]
        self.smtp_email = os.environ["MY_SMTP_EMAIL"]
        self.password = os.environ["MY_SMTP_PASSWORD"]
        self.today = (dt.datetime.now()).strftime("[%d-%m-%Y | %H:%M:%S]")
        self.subject = f"Your logs and tasks for {self.today}"

    def add_to_msg(self, text):
        """
        Adds either empty space b/w logs or the text for logs
        """
        global msg_txt
        if text == "\n\n":
            msg_txt += f"{text}"
        else:
            msg_txt += f"{self.today} - {text}\n"

    def send_email(self):
        """
        Sends email with all the logs as the body
        """
        global msg_txt
        email_text = f"Subject:{self.subject}\n\n{msg_txt}"
        if email_text != "":
            with smtplib.SMTP("smtp.gmail.com") as connection:
                print("Connection Established")
                print(email_text)
                connection.starttls()
                connection.login(user=self.smtp_email, password=self.password)
                connection.sendmail(
                    from_addr=self.smtp_email,
                    to_addrs=self.my_email,
                    msg=email_text,
                )
            print(f"Email sent to {self.my_email}")
        else:
            print("Something went wrong")
