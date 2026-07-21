from features.email_logic import EmailSender
from features.slack_logic import SlackSender

if __name__=='__main__':
    EmailSender()._sending_email()
    SlackSender()._send_slack_message()