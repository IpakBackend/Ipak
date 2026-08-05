from django.conf import settings
from django.core import signing
from django.core.mail import EmailMessage


def send_email_verification_link(user_id: int, email: str) -> None:
    token: str = signing.dumps(
        obj={"user_id": user_id},
        salt="email-verification"
    )

    verification_link: str = settings.FRONTEND_URL + f"/verify-email/{token}/"

    subject: str = "Email verification"
    message: str = (
        "<p>Click or copy the link below to verify your email:</p>"
        f'<p><a href="{verification_link}">{verification_link}</a></p>'
    )

    email_message = EmailMessage(
        subject=subject,
        body=message,
        to=[email]

    )
    email_message.content_subtype = "html"
    email_message.send(fail_silently=False)
