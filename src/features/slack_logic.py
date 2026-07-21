from slack_sdk.webhook import WebhookClient
from pathlib import Path
from pydantic import Field, SecretStr
from pydantic_settings import SettingsConfigDict, BaseSettings

from features.email_logic import EmailSender

class SlackSender(BaseSettings):
    slack_webhook_url: SecretStr = Field(alias='SLACK_WEBHOOK_URL')
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent.joinpath('.env'),
        extra='ignore'
    )
    def _send_slack_message(self):
        slack_webhook = WebhookClient(url=self.slack_webhook_url.get_secret_value())
        message = EmailSender()._define_email_contents()
        contents = f"""
{message.get('subject')}\n\n{message.get('body')}
"""
        slack_webhook.send(text=contents)