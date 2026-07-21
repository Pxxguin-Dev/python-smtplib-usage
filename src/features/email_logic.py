# Pydantic library
from typing import List, Any, Optional
from pydantic import EmailStr, SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Basic Library
from pathlib import Path

# Email Library
from email.message import EmailMessage
from smtplib import SMTP

class EmailSender(BaseSettings):
    sender_email: EmailStr
    sender_password: SecretStr
    sender_server: str
    sender_port: int
    receiver_email: EmailStr

    # Github workflows env
    run_id: str = Field(alias='RUN_ID')
    actor: str = Field(alias='ACTOR')
    workflow_url: str = Field(alias='WORKFLOW_URL')
    current_status: str = Field(alias='CURRENT_STATUS')
    commit_message: str = Field(alias='COMMIT_MESSAGE')
    github_sha: str = Field(alias="GITHUB_SHA")

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent.joinpath(".env"),
        extra='ignore'
    )

    def _define_email_contents(self):
        subject = f'[Github] Github workflow is triggered by {self.actor}'
        body = f"""
안녕하세요, 
Github workflows를 담당하고 있는 🤖pxxguin입니다.
해당 workflow의 결과를 아래에 전달해드립니다.

---------------------------------------------------------
1. status: {self.current_status}
2. commit message: {self.commit_message}
3. github sha: {self.github_sha}
5. workflow: {self.workflow_url}
---------------------------------------------------------
"""
        return {
            'subject':subject,
            'body':body
        }

    def _setting_sending_email(self, to_email: EmailStr):
        message = EmailMessage()
        message['Subject'] = self._define_email_contents().get('subject')
        message.set_content(self._define_email_contents().get('body'))
        message['To'] = to_email
        message['From'] = self.sender_email

        try:
            with SMTP(self.sender_server, self.sender_port) as server:
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
        except Exception as e:
            print("fuck")

    def _sending_email(self):
        self._setting_sending_email(to_email=self.receiver_email)