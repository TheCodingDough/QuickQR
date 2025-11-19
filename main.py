import qrcode
import os
import sys
import traceback
from tkinter import Tk, Label, Entry, Button, StringVar, filedialog, messagebox

# --- CONFIG ---
DEFAULT_SAVE_DIR = r"D:\Anant\Coding\QR code generator\all saved qr codes"
os.makedirs(DEFAULT_SAVE_DIR, exist_ok=True)

# --- GUI ---

class QRGui:
    def __init__(self, master):
        self.master = master
        master.title("QR Code Generator")

        # Variables
        self.url_var = StringVar()
        self.filename_var = StringVar()
        self.folder_var = StringVar(value=DEFAULT_SAVE_DIR)

        # Widgets
        Label(master, text="URL / Text:").grid(row=0, column=0, sticky="w", padx=6, pady=6)
        Entry(master, textvariable=self.url_var, width=60).grid(row=0, column=1, columnspan=3, padx=6, pady=6)

        Label(master, text="File name (no ext):").grid(row=1, column=0, sticky="w", padx=6, pady=6)
        Entry(master, textvariable=self.filename_var, width=30).grid(row=1, column=1, padx=6, pady=6)

        Label(master, text="Save folder:").grid(row=2, column=0, sticky="w", padx=6, pady=6)
        Entry(master, textvariable=self.folder_var, width=40).grid(row=2, column=1, padx=6, pady=6)
        Button(master, text="Browse...", command=self.browse_folder).grid(row=2, column=2, padx=6, pady=6)

        Button(master, text="Generate and Save PNG", command=self.generate_and_save).grid(row=3, column=1, pady=12)
        Button(master, text="Quit", command=master.quit).grid(row=3, column=2, pady=12)

    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.folder_var.get() or DEFAULT_SAVE_DIR)
        if folder:
            self.folder_var.set(folder)

    def _sanitize_filename(self, name: str) -> str:
        # Remove characters that are illegal in filenames on Windows
        invalid = '<>:"/\\|?*'
        cleaned = ''.join(ch for ch in name if ch not in invalid).strip()
        # fallback
        if not cleaned:
            cleaned = 'qrcode'
        return cleaned

    def generate_and_save(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter the URL or text to encode.")
            return

        filename = self.filename_var.get().strip()
        filename = self._sanitize_filename(filename)
        # ensure .png extension
        if not filename.lower().endswith('.png'):
            filename = filename + '.png'

        folder = self.folder_var.get().strip() or DEFAULT_SAVE_DIR
        if not os.path.isdir(folder):
            try:
                os.makedirs(folder, exist_ok=True)
            except Exception as e:
                messagebox.showerror("Error", f"Could not create folder:\n{e}")
                return

        full_path = os.path.join(folder, filename)

        # If file exists, ask to overwrite
        if os.path.exists(full_path):
            if not messagebox.askyesno("Overwrite?", f"File already exists:\n{full_path}\nOverwrite?"):
                return

        try:
            qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M)
            qr.add_data(url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            # make sure image is a PIL Image and save as PNG
            img = img.convert('RGB') if hasattr(img, 'convert') else img
            img.save(full_path, format='PNG')

            messagebox.showinfo("Saved", f"QR code saved to:\n{full_path}")
        except Exception:
            traceback.print_exc(file=sys.stderr)
            messagebox.showerror("Error", "Failed to generate/save QR code. See console for details.")


if __name__ == '__main__':
    try:
        root = Tk()
        gui = QRGui(root)
        root.resizable(False, False)
        root.mainloop()
    except Exception:
        traceback.print_exc()
