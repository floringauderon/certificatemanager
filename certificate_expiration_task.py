# certificate_expiration_task.py
import sendgrid
from sendgrid.helpers.mail import Mail
from mysite import app, db, models, SENDGRID_API_KEY # adjust import to your project
import datetime

def send_certificate_expiration_email(certificate, user_email):
    sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
    message = Mail(
        from_email=app.config['MAIL_DEFAULT_SENDER'],
        to_emails=user_email,
        subject="Certificate Expiration Notification",
        html_content=f"Your certificate '{certificate.common_name}' is expiring in 30 days. Please take necessary action.",
    )
    try:
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))

def check_certificate_expiration():
    today = datetime.date.today()
    expiration_date = today + datetime.timedelta(days=30)

    with app.app_context():
        certificates = models.Certificate.query.filter(models.Certificate.valid_to_date == expiration_date).all()

        for certificate in certificates:
            user = models.User.query.get(certificate.user_id)
            if user and user.email:
                send_certificate_expiration_email(certificate, user.email)

if __name__ == '__main__':
    check_certificate_expiration()