import Client
import time

twilio_number = '09374361359'
target_number = '09921249360'

# ایجاد کلاینت
client = Client(account_sid, auth_token)

# تابع برای ارسال SMS
def send_sms(message):
    message = client.messages.create(
        to=target_number,
        from_=twilio_number,
        body=message
    )
    return message.sid

# فرض کنید که شما می‌خواهید یک پیام را ارسال کنید
if __name__ == "__main__":
    current_time = time.ctime()
    message = f"پیام شما در {current_time} ارسال شده است."
    sms_sid = send_sms(message)
    print(f"SMS با SID {sms_sid} ارسال شد.")
