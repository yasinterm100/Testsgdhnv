import subprocess
import time

def get_recent_sms(phone_number):
    # Calculate the current time and the time 5 minutes ago
    current_time = int(time.time())
    five_minutes_ago = current_time - 300

    # Retrieve SMS messages
    result = subprocess.run(['termux-sms-list'], capture_output=True, text=True)
    messages = result.stdout.splitlines()

    recent_messages = []

    for message in messages:
        # Parse the SMS data
        msg_data = eval(message)
        if msg_data['address'] == phone_number and msg_data['date'] >= five_minutes_ago:
            recent_messages.append(msg_data['body'])

    return recent_messages

if __name__ == "__main__":
    phone_number = input("Enter the phone number: ")
    messages = get_recent_sms(phone_number)

    if messages:
        print("Recent messages:")
        for msg in messages:
            print(msg)
    else:
        print("No new messages.")