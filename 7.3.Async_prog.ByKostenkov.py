from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import asyncio
from g4f.client import AsyncClient


async def main(prompt, status_var):
    try:
        client = AsyncClient()
        response = await client.images.generate(
            prompt=prompt,
            model="flux",
            response_format="url"
        )
        image_url = response.data[0].url
        status_var.set("Изображение сгенерировано!")
        return image_url
    except Exception as e:
        status_var.set("Ошибка генерации")
        messagebox.showerror("Ошибка", f"Не удалось сгенерировать изображение: {str(e)}")
        return None

def generate_image(prompt_entry, status_var):
    prompt = prompt_entry.get()
    if not prompt.strip():
        messagebox.showwarning("Ошибка", "Пожалуйста, введите запрос")
        return

    status_var.set("Генерация изображения...")
    window.update()

    async def run_generation():
        image_url = await main(prompt_entry.get(), status_var)
        if image_url:
            show_image_window(image_url)

    asyncio.run(run_generation())

def show_image_window(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()

        image_window = Toplevel(window)
        image_window.title("Сгенерированное изображение")

        image_data = BytesIO(response.content)
        pil_image = Image.open(image_data)

        max_size = (600, 480)
        if pil_image.width > max_size[0] or pil_image.height > max_size[1]:
            pil_image.thumbnail(max_size, Image.LANCZOS)

        tk_image = ImageTk.PhotoImage(pil_image)

        image_label = Label(image_window, image=tk_image)
        image_label.image = tk_image
        image_label.pack(padx=10, pady=10)

        close_btn = ttk.Button(image_window, text="Закрыть", command=image_window.destroy)
        close_btn.pack(pady=10)

    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {str(e)}")

def exit_app():
    window.destroy()

window = Tk()
window.title("Генератор изображений ИИ")
window.geometry("600x300")

menu_bar = Menu(window)
window.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Файл", menu=file_menu)
file_menu.add_command(label="Выход", command=exit_app)

ai_frame = ttk.LabelFrame(window, text="Генератор изображений ИИ", padding=10)
ai_frame.pack(pady=20, fill=X, padx=20)

ttk.Label(ai_frame, text="Введите описание изображения:").pack(pady=5)

prompt_entry = ttk.Entry(ai_frame, width=50)
prompt_entry.pack(pady=5)
prompt_entry.insert(0, "a white siamese cat")

status_var = StringVar()
status_var.set("Готов к работе")

generate_btn = ttk.Button(ai_frame, text="Сгенерировать изображение",
                         command=lambda: generate_image(prompt_entry, status_var))
generate_btn.pack(pady=10)

ttk.Label(ai_frame, textvariable=status_var).pack(pady=5)

window.mainloop()