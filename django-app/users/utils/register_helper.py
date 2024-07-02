class RegisterHelper:
    def email_already_exists(self):
        query = "SELECT * FROM user WHERE email = %s"
        email_list = self.run_select_query(query, (self.email,))
        return len(email_list) > 0

    def send_conf_email(self, site):
        from django.core.mail import send_mail
        from django.core import signing

        signer = signing.Signer()
        signed_email = signer.sign(self.email)

        conf_link = f"http://{site.domain}/confirm-email?link={signed_email}"
        try:
            send_mail(
                subject='Confirm your email',
                message=f'Please confirm your email by clicking on the following link: {conf_link}',
                recipient_list=[self.email],
                from_email=None,
                fail_silently=False
            )
        except Exception as e:
            print(e)
            return False
        return True

    def confirm_email_update(self):
        query = "UPDATE user SET activation_status = 1 WHERE email = %s"
        affected_rows = self.run_update_query(query, (self.email,))
        return affected_rows > 0
