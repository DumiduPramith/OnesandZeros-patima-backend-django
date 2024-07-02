import secrets
import string

class ForgotPasswordHelper:
    @staticmethod
    def generate_password(length=6):
        characters = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(characters) for i in range(length))
        return password

    def send_forgot_password_email(self, new_password):
        from django.core.mail import send_mail
        email_text = f'Your new password is: {new_password}'
        try:
            send_mail(
                subject='Forgot Password',
                message=email_text,
                recipient_list=[self.email],
                from_email=None,
                fail_silently=False
            )
        except Exception as e:
            print(e)
            return False
        return True

