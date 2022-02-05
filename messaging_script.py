import time
import smtplib
import argparse
from email.message import EmailMessage
import camping_scraper as cs


def msg_alert(
    subject,
    body,
    to=None,
    email_addr=None,
    app_pwd=None,
):
    """Send text message alerts to phone.
    Check README for configuration instructions.

    Parameters
    ----------
    subject : str

    body : str

    to : str
        Phone number appended with the mobile carrier's SMS Gateway Address

    email_addr : str
        this code only works with a Gmail address

    app_pwd : str
    """
    if not to or not email_addr or not app_pwd:
        raise ValueError("Please check README and overwrite keyword args with personal info")
    msg = EmailMessage()
    msg.set_content(body)
    msg["subject"] = subject
    msg["to"] = to
    msg["from"] = email_addr

    server = smtplib.SMTP("smtp.gmail.com", 587)

    server.starttls()
    server.login(str(email_addr), str(app_pwd))
    server.send_message(msg)
    server.quit()

parser = argparse.ArgumentParser(description="Find available campsites.")
parser.add_argument("--park", "-p")
parser.add_argument("--campground", "-c")
parser.add_argument("--year", "-y")
parser.add_argument("--months", "-m", nargs='+', default=[])
parser.add_argument("--sleep", "-s", default=86400)
parser.add_argument("--verbose", "-v", action="store_true")

args = parser.parse_args()

while True:
    availability = cs.find_availability_by_year(args.park, args.campground, args.year, args.months)

    if availability:
        msg = "Availability found at " + args.park + " " + args.campground + ":\n"
        for available in availability:
            msg += available.strftime("%Y-%m-%d") + "\n"
            # split up texts before they go over newline limit
            if len(msg) > 125:
                msg_alert("Campsite Availability", msg)
                if args.verbose:
                    print(msg)
                msg = ""
        if len(msg) > 0:
            msg_alert("Campsite Availability", msg)
    else:
        msg = ("No available sites found for " + args.park + " " + args.campground +
               ". Will try to search again in " + str(args.sleep / 3600) + " hours.")
        msg_alert("Campsite Availability", msg)

    if args.verbose:
        print(msg)

    time.sleep(args.sleep)
