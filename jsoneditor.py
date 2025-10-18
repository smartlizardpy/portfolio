import os
import json
from tkinter import (
    Tk, Toplevel, Frame, Label, Entry, Text, Button, OptionMenu, StringVar, Scrollbar, END, filedialog, messagebox
)
from tkcalendar import DateEntry  # pip install tkcalendar

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PHOTOS_DIR = os.path.join(PROJECT_ROOT, "..", "public", "images", "photos")
OUTPUT_JSON = os.path.join(PROJECT_ROOT, "src", "data", "photos.json")
CATEGORIES = ["Cats", "Dogs", "Nature", "Other"]

def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_json(data, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ...existing code...

class PhotoEditor(Toplevel):
    def __init__(self, master, photo=None, on_save=None):
        super().__init__(master)
        self.title("Edit Photo Entry")
        self.photo = photo or {}
        self.on_save = on_save

        # ID
        Label(self, text="ID:").grid(row=0, column=0, sticky="e")
        self.id_entry = Entry(self)
        self.id_entry.grid(row=0, column=1)
        self.id_entry.insert(0, str(self.photo.get("id", "")))

        # Title
        Label(self, text="Title:").grid(row=1, column=0, sticky="e")
        self.title_entry = Entry(self, width=40)
        self.title_entry.grid(row=1, column=1)
        self.title_entry.insert(0, self.photo.get("title", ""))

        # Description
        Label(self, text="Description:").grid(row=2, column=0, sticky="ne")
        self.desc_text = Text(self, width=40, height=4)
        self.desc_text.grid(row=2, column=1)
        self.desc_text.insert(END, self.photo.get("description", ""))

        # Category (custom entry)
        Label(self, text="Category:").grid(row=3, column=0, sticky="e")
        self.cat_entry = Entry(self, width=40)
        self.cat_entry.grid(row=3, column=1)
        self.cat_entry.insert(0, self.photo.get("category", ""))

        # Topic
        Label(self, text="Topic:").grid(row=4, column=0, sticky="e")
        self.topic_entry = Entry(self, width=40)
        self.topic_entry.grid(row=4, column=1)
        self.topic_entry.insert(0, self.photo.get("topic", ""))

        # Image
        Label(self, text="Image:").grid(row=5, column=0, sticky="e")
        self.img_entry = Entry(self, width=40)
        self.img_entry.grid(row=5, column=1)
        self.img_entry.insert(0, self.photo.get("image", ""))

        Button(self, text="Browse", command=self.browse_image).grid(row=5, column=2)

        # Thumbnail
        Label(self, text="Thumbnail:").grid(row=6, column=0, sticky="e")
        self.thumb_entry = Entry(self, width=40)
        self.thumb_entry.grid(row=6, column=1)
        self.thumb_entry.insert(0, self.photo.get("thumbnail", ""))

        Button(self, text="Browse", command=self.browse_thumbnail).grid(row=6, column=2)

        # Date (always 2025-07-13, no widget)
        Label(self, text="Date:").grid(row=7, column=0, sticky="e")
        Label(self, text="2025-07-13").grid(row=7, column=1, sticky="w")

        # Save Button
        Button(self, text="Save", command=self.save).grid(row=8, column=1, pady=10)

    def browse_image(self):
        path = filedialog.askopenfilename(initialdir=PHOTOS_DIR, filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif *.bmp")])
        if path:
            rel_path = "/images/photos/" + os.path.basename(path)
            self.img_entry.delete(0, END)
            self.img_entry.insert(0, rel_path)

    def browse_thumbnail(self):
        path = filedialog.askopenfilename(initialdir=PHOTOS_DIR, filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif *.bmp")])
        if path:
            rel_path = "/images/photos/" + os.path.basename(path)
            self.thumb_entry.delete(0, END)
            self.thumb_entry.insert(0, rel_path)

    def save(self):
        try:
            photo = {
                "id": int(self.id_entry.get()),
                "title": self.title_entry.get(),
                "description": self.desc_text.get("1.0", END).strip(),
                "category": self.cat_entry.get(),
                "topic": self.topic_entry.get(),
                "image": self.img_entry.get(),
                "thumbnail": self.thumb_entry.get(),
                "date": "2025-07-13"
            }
            if self.on_save:
                self.on_save(photo)
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

# ...existing code...
    def browse_image(self):
        path = filedialog.askopenfilename(initialdir=PHOTOS_DIR, filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif *.bmp")])
        if path:
            rel_path = "/images/photos/" + os.path.basename(path)
            self.img_entry.delete(0, END)
            self.img_entry.insert(0, rel_path)

    def browse_thumbnail(self):
        path = filedialog.askopenfilename(initialdir=PHOTOS_DIR, filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif *.bmp")])
        if path:
            rel_path = "/images/photos/" + os.path.basename(path)
            self.thumb_entry.delete(0, END)
            self.thumb_entry.insert(0, rel_path)

    def save(self):
        try:
            photo = {
                "id": int(self.id_entry.get()),
                "title": self.title_entry.get(),
                "description": self.desc_text.get("1.0", END).strip(),
                "category": self.cat_entry.get(),
                "topic": self.topic_entry.get(),
                "image": self.img_entry.get(),
                "thumbnail": self.thumb_entry.get(),
                "date": "2025-07-13"
            }
            if self.on_save:
                self.on_save(photo)
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
class MainApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("Photo JSON Editor")
        self.geometry("700x500")
        self.photos = load_json(OUTPUT_JSON)

        self.list_frame = Frame(self)
        self.list_frame.pack(fill="both", expand=True)

        self.refresh_list()

        Button(self, text="Add Photo", command=self.add_photo).pack(side="left", padx=10, pady=10)
        Button(self, text="Save All", command=self.save_all).pack(side="right", padx=10, pady=10)

    def refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        Label(self.list_frame, text="Photos:", font=("Arial", 14)).pack(anchor="w")
        for idx, photo in enumerate(self.photos):
            frame = Frame(self.list_frame)
            frame.pack(fill="x", pady=2)
            Label(frame, text=f"{photo['id']}: {photo['title']}", width=40, anchor="w").pack(side="left")
            Button(frame, text="Edit", command=lambda i=idx: self.edit_photo(i)).pack(side="left")
            Button(frame, text="Delete", command=lambda i=idx: self.delete_photo(i)).pack(side="left")

    def add_photo(self):
        def on_save(photo):
            self.photos.append(photo)
            self.refresh_list()
        PhotoEditor(self, on_save=on_save)

    def edit_photo(self, idx):
        def on_save(photo):
            self.photos[idx] = photo
            self.refresh_list()
        PhotoEditor(self, photo=self.photos[idx], on_save=on_save)

    def delete_photo(self, idx):
        if messagebox.askyesno("Delete", "Are you sure you want to delete this photo?"):
            del self.photos[idx]
            self.refresh_list()

    def save_all(self):
        save_json(self.photos, OUTPUT_JSON)
        messagebox.showinfo("Saved", f"Saved to {OUTPUT_JSON}")

if __name__ == "__main__":
    MainApp().mainloop()