import os
from tkinter import Tk, Label, Button, filedialog, messagebox


def hide_zip_in_image(image_path, zip_path, output_path):
    try:
        with open(image_path, 'rb') as img_file:
            image_data = img_file.read()

        with open(zip_path, 'rb') as zip_file:
            zip_data = zip_file.read()

        with open(output_path, 'wb') as out_file:
            out_file.write(image_data + zip_data)

        return True
    except Exception as e:
        print("Error:", e)
        return False


def select_image():
    file_path = filedialog.askopenfilename(title="انتخاب عکس")
    if file_path:
        image_label.config(text=f"عکس انتخاب شد: {os.path.basename(file_path)}")
        app.selected_image = file_path


def select_zip():
    file_path = filedialog.askopenfilename(title="انتخاب فایل ZIP یا RAR",
                                           filetypes=[("ZIP/RAR", "*.zip *.rar")])
    if file_path:
        zip_label.config(text=f"فایل انتخاب شد: {os.path.basename(file_path)}")
        app.selected_zip = file_path


def generate_file():
    image = getattr(app, 'selected_image', None)
    zip_file = getattr(app, 'selected_zip', None)

    if not image or not zip_file:
        messagebox.showerror("خطا", "لطفاً عکس و فایل زیپ را انتخاب کنید.")
        return

    output_file = os.path.join(os.getcwd(), "combined_image.jpg")
    success = hide_zip_in_image(image, zip_file, output_file)

    if success:
        messagebox.showinfo("موفقیت", f"فایل ساخته شد: {output_file}")
    else:
        messagebox.showerror("خطا", "خطایی در ساخت فایل رخ داد.")


# رابط گرافیکی
app = Tk()
app.title("پنهان کردن فایل ZIP در عکس")
app.geometry("400x220")

Label(app, text="پنهان‌سازی فایل ZIP یا RAR در عکس", font=("tahoma", 12, "bold")).pack(pady=10)

Button(app, text="انتخاب عکس", command=select_image).pack(pady=5)
image_label = Label(app, text="هیچ عکسی انتخاب نشده")
image_label.pack()

Button(app, text="انتخاب فایل ZIP یا RAR", command=select_zip).pack(pady=5)
zip_label = Label(app, text="هیچ فایلی انتخاب نشده")
zip_label.pack()

Button(app, text="ساخت فایل نهایی", command=generate_file, bg="green", fg="white").pack(pady=15)

app.mainloop()
