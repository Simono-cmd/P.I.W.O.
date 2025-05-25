from customtkinter import CTk, CTkToplevel, CTkFrame, CTkLabel
from PIL import Image, ImageTk
import os

from sqlalchemy.orm import Session


class ReportWindow(CTkToplevel):
    def __init__(self, parent : CTk, session : Session) -> None:
        super().__init__(parent)
        self.session = session
        self.title("Reports")
        self.focus()
        self.grab_set()
        self.geometry("1300x350")
        self.iconbitmap("gui/icons/chart.ico")

        self.images_frame = CTkFrame(self)
        self.images_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.image_labels = []
        self.image_tk_refs = []

        images_dir = "../Statistics"
        if not os.path.exists(images_dir):
            print(f"Image folder '{images_dir}' not found!")
            return

        files = [f for f in os.listdir(images_dir) if f.lower().endswith((".png", ".jpg", ".jpeg"))]

        for file in files:
            img_path = os.path.join(images_dir, file)
            pil_image = Image.open(img_path)
            pil_image.thumbnail((500, 300))
            tk_image = ImageTk.PhotoImage(pil_image)
            self.image_tk_refs.append(tk_image)
            label = CTkLabel(self.images_frame, image=tk_image, text="")
            label.pack(pady=10, side = "left")
            self.image_labels.append(label)
