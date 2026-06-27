from django.core.mail import EmailMessage


def send_otp_code(email: str, otp_code: str) -> None:

    subject: str = "OTP code"
    message:  str = "Your OTP code is: " + str(otp_code)

    email_message = EmailMessage(
        subject=subject,
        body=message,
        to=[email]

    )
    email_message.content_subtype = "html"
    email_message.send(fail_silently=False)
