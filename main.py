import os
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFont


class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Watermarking Desktop App")
        self.root.geometry("950x650")

        # Image & Watermark State
        self.image_path = None
        self.original_image = None
        self.display_image = None
        self.watermark_preview_img = None
        self.text_color = "#FFFFFF"

        # Watermark Coordinates (Canvas relative)
        self.wm_canvas_x = 100
        self.wm_canvas_y = 100
        self.drag_data = {"x": 0, "y": 0}

        self._build_ui()

    def _build_ui(self):
        # Top Control Bar
        control_frame = tk.Frame(self.root, pady=10)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        btn_upload = tk.Button(control_frame, text="1. Select Image", command=self.load_image, bg="#2b5c8f", fg="white", font=("Arial", 10, "bold"))
        btn_upload.pack(side=tk.LEFT, padx=10)

        # Left Options Sidebar
        options_frame = tk.LabelFrame(self.root, text="Watermark Settings", padx=10, pady=10)
        options_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Text Inputs
        tk.Label(options_frame, text="Watermark Text:").pack(anchor=tk.W, pady=(5, 0))
        self.entry_text = tk.Entry(options_frame, width=22)
        self.entry_text.insert(0, "© My Watermark")
        self.entry_text.pack(anchor=tk.W, pady=5)

        btn_color = tk.Button(options_frame, text="Choose Text Color", command=self.choose_color)
        btn_color.pack(anchor=tk.W, pady=5)

        tk.Label(options_frame, text="Opacity (10 - 255):").pack(anchor=tk.W, pady=(10, 0))
        self.scale_opacity = tk.Scale(options_frame, from_=10, to=255, orient=tk.HORIZONTAL)
        self.scale_opacity.set(180)
        self.scale_opacity.pack(fill=tk.X, pady=5)

        btn_update = tk.Button(options_frame, text="2. Place / Update Text", command=self.create_watermark_overlay, bg="#27ae60", fg="white", font=("Arial", 10, "bold"))
        btn_update.pack(fill=tk.X, pady=(15, 5))

        tk.Label(options_frame, text="💡 Tip: Click and drag\nthe watermark on screen!", fg="#7f8c8d", justify=tk.LEFT).pack(anchor=tk.W, pady=10)

        btn_save = tk.Button(options_frame, text="3. Save Copy", command=self.save_image, bg="#e67e22", fg="white", font=("Arial", 10, "bold"))
        btn_save.pack(fill=tk.X, pady=(20, 5))

        # Right Side: Interactive Preview Canvas
        self.canvas_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.canvas_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.canvas = tk.Canvas(self.canvas_frame, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack(expand=True, fill=tk.BOTH)

        # Bind Mouse Events for Dragging
        self.canvas.tag_bind("watermark", "<Button-1>", self.on_drag_start)
        self.canvas.tag_bind("watermark", "<B1-Motion>", self.on_drag_motion)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.webp")])
        if file_path:
            self.image_path = file_path
            self.original_image = Image.open(self.image_path).convert("RGBA")
            self._render_base_image()
            self.create_watermark_overlay()

    def choose_color(self):
        color = colorchooser.askcolor(title="Choose Watermark Color")
        if color[1]:
            self.text_color = color[1]
            self.create_watermark_overlay()

    def _render_base_image(self):
        # Resize original image to fit preview canvas while preserving aspect ratio
        self.preview_image = self.original_image.copy()
        self.preview_image.thumbnail((650, 500))
        self.display_image = ImageTk.PhotoImage(self.preview_image)

        self.canvas.delete("all")
        # Center image on canvas
        self.img_x = (650 - self.preview_image.width) // 2 + 20
        self.img_y = (500 - self.preview_image.height) // 2 + 20
        self.canvas.create_image(self.img_x, self.img_y, image=self.display_image, anchor=tk.NW, tags="bg_image")

    def create_watermark_overlay(self):
        if not self.original_image:
            return

        text = self.entry_text.get()
        if not text:
            return

        # Calculate scaling factor for preview
        scale = self.preview_image.width / self.original_image.width
        font_size = max(12, int(self.original_image.height * 0.04 * scale))

        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except OSError:
            font = ImageFont.load_default()

        # Render transparent text layer
        r, g, b = tuple(int(self.text_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        alpha = self.scale_opacity.get()

        # Measure text box
        dummy_img = Image.new("RGBA", (1, 1))
        draw = ImageDraw.Draw(dummy_img)
        bbox = draw.textbbox((0, 0), text, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]

        txt_img = Image.new("RGBA", (w + 10, h + 10), (0, 0, 0, 0))
        draw = ImageDraw.Draw(txt_img)
        draw.text((5, 5), text, fill=(r, g, b, alpha), font=font)

        self.watermark_preview_img = ImageTk.PhotoImage(txt_img)

        # Redraw or update canvas watermark tag
        self.canvas.delete("watermark")
        self.wm_item = self.canvas.create_image(
            self.wm_canvas_x, self.wm_canvas_y,
            image=self.watermark_preview_img,
            anchor=tk.NW,
            tags="watermark"
        )

    # Dragging Event Handlers
    def on_drag_start(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_drag_motion(self, event):
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]

        self.canvas.move("watermark", dx, dy)

        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

        # Track absolute canvas coordinates
        coords = self.canvas.coords("watermark")
        if coords:
            self.wm_canvas_x, self.wm_canvas_y = coords[0], coords[1]

    def save_image(self):
        if not self.original_image or not self.watermark_preview_img:
            messagebox.showwarning("Warning", "No image or watermark loaded!")
            return

        # Calculate exact relative coordinates on full resolution image
        scale_x = self.original_image.width / self.preview_image.width
        scale_y = self.original_image.height / self.preview_image.height

        rel_x = int((self.wm_canvas_x - self.img_x) * scale_x)
        rel_y = int((self.wm_canvas_y - self.img_y) * scale_y)

        # Composite watermark onto full res copy
        full_base = self.original_image.copy()
        txt_layer = Image.new("RGBA", full_base.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(txt_layer)

        font_size = int(self.original_image.height * 0.04)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except OSError:
            font = ImageFont.load_default()

        r, g, b = tuple(int(self.text_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        alpha = self.scale_opacity.get()

        draw.text((rel_x, rel_y), self.entry_text.get(), fill=(r, g, b, alpha), font=font)
        final_image = Image.alpha_composite(full_base, txt_layer)

        # Prepare save path
        dir_name, full_filename = os.path.split(self.image_path)
        filename, ext = os.path.splitext(full_filename)
        default_name = f"{filename}_watermarked{ext}"

        save_path = filedialog.asksaveasfilename(
            initialdir=dir_name,
            initialfile=default_name,
            defaultextension=".png",
            filetypes=[("PNG file", "*.png"), ("JPEG file", "*.jpg")]
        )

        if save_path:
            if os.path.abspath(save_path) == os.path.abspath(self.image_path):
                messagebox.showerror("Error", "Please select a different filename or location to protect your original image.")
                return

            if save_path.lower().endswith((".jpg", ".jpeg")):
                final_image = final_image.convert("RGB")

            final_image.save(save_path)
            messagebox.showinfo("Success", f"Saved successfully to:\n{os.path.basename(save_path)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()