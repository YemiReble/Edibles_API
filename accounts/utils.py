import random
from .models import Account as User
from django.core.mail import EmailMessage, send_mail


# generate stings and number with symbols password
def generate_password():
    symbols = "!@#$%^&*"
    password = ''.join(random.choice(symbols + "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for i in range(12))
    return password

# generate OTP
def generateOTP():
    otp = ''.join(random.choice("0123456789") for i in range(6))
    return otp

def send_forget_mail(name, email, token):
    subject = 'Your forget password link'
    message = f'Hi {name}, click on the link to reset your password http://127.0.0.1:8000/change_password/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


def sendOTP_to_user(email):
    subject = "Email Varification"
    otp = genrateOTP()
    user = User.objects.get(email=email)
    current_site = "BeatsFussion.com"
    email_body = f"Hello {user.first_name}! welcome to {current_site}, Here is your OTP is {otp} for email confirmation"
    from_email = settings.DEFAULT_FROM_EMAIL

    OneTimePassword.objects.create(user=user, otp=otp)
    mail = EmailMessage(subject=subject, body=email_body, from_email=from_email, to=[email])
    mail.send(fail_silenly=True)


import secrets  # Use secrets module for cryptographically secure random numbers

class PasswordGenerator:
    """A class for generating secure passwords and OTPs."""

    def __init__(self, password_length=12, otp_length=6):
        """
        Initializes the PasswordGenerator with default lengths for password and OTP.

        Args:
            password_length (int, optional): The length of the generated password. Defaults to 12.
            otp_length (int, optional): The length of the generated OTP. Defaults to 6.
        """

        self.password_length = password_length
        self.otp_length = otp_length

    def password_gen(self):
        """Generates a strong password using a combination of lowercase, uppercase,
        digits, and symbols.

        Returns:
            str: The generated password.
        """

        symbols = "!@#$%^&*"
        chars = symbols + string.ascii_lowercase + string.ascii_uppercase + string.digits
        return ''.join(secrets.choice(chars) for _ in range(self.password_length))

    def generate_otp(self):
        """Generates a time-based one-time password (OTP) using digits.

        Returns:
            str: The generated OTP.
        """

        return ''.join(secrets.choice(string.digits) for _ in range(self.otp_length))

if __name__ == "__main__":
    generator = PasswordGenerator()
    password = generator.password_gen()
    otp = generator.generate_otp()

    print(f"Generated password: {password}")
    print(f"Generated OTP: {otp}")

