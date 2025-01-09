import requests

def send_sms_to_roubika(phone_number):
    url = "https://api.roubika.com/send_sms"  # URL فرضی برای ارسال SMS
    payload = {
        "phone": phone_number,
        "message": "کد یکبار مصرف شما: 123456"  # پیام نمونه
    }
    headers = {
        "Authorization": "Bearer 7757874477:AAHufGbhaUHbiHmEFaZizqcloKkAp_N8mqk"  # توکن دسترسی
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print("پیام با موفقیت ارسال شد.")
        return response.json()  # فرض بر این است که پاسخ JSON است
    else:
        print("خطا در ارسال پیام:", response.status_code)
        return None

# شماره مورد نظر را وارد کنید
phone_number = input("enter phone number : ")
send_sms_to_roubika(phone_number)
