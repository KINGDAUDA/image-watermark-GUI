# 📸 Image Watermarking Desktop Application

A modern, lightweight Python desktop application built with **Tkinter** and **Pillow (PIL)** that allows users to protect and brand their images with customizable, draggable text watermarks.

---

## ✨ Features

- **Interactive Drag & Drop Positioning:** Freely drag the watermark across the preview canvas to place it anywhere on your image.
- **Customizable Typography & Appearance:**
  - Dynamic watermark text input.
  - Native color palette selector for any custom hex color.
  - Fine-grained opacity slider ($10$ to $255$).
- **Non-Destructive Editing & Quality Preservation:**
  - Fast, responsive canvas preview rendering using thumbnail scaling.
  - Mathematical ratio mapping ensures the watermark is placed at the exact corresponding coordinates on the original high-resolution file.
  - Source file overwrite protection: Automatically suggests a new filename (e.g., `image_watermarked.png`) and prevents accidental overwrites of the original image.
- **Multi-Format Support:** Load and export `.png`, `.jpg`, `.jpeg`, `.bmp`, and `.webp` files.

---

## 🛠️ Prerequisites & Tech Stack

- **Python 3.10+** (tested and compatible with Python 3.13+)
- **Tkinter** (included with standard Windows Python installers)
- **Pillow (`PIL`)** (for image manipulation and compositing)

---

## 🚀 Installation & Setup

### 1. Clone or Download the Repository
```bash
git clone https://github.com/your-username/image-watermarking-app.git
cd image-watermarking-app
```

### 2. Create and Activate a Virtual Environment

**Windows (PowerShell):**
```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install Pillow
```

> **Note:** Do not run `pip install PIL`. The modern, maintained distribution is `Pillow`.

---

## 🖥️ Running the Application

Launch the desktop GUI by executing `main.py`:

```bash
python main.py
```
*(On Windows, you can also run `py main.py` if python aliases are not configured).*

---

## 📖 How to Use

1. **Upload an Image:** Click **1. Select Image** to open your target photo.
2. **Customize Watermark:**
   - Type your custom text in the **Watermark Text** field.
   - Click **Choose Text Color** to select a color.
   - Adjust the **Opacity** slider to control transparency.
3. **Position Watermark:**
   - Click **2. Place / Update Text** to generate or update the watermark on the preview canvas.
   - Click and hold directly on the watermark text, then **drag it** anywhere over your photo.
4. **Save a Copy:** Click **3. Save Copy** to export your watermarked image without overwriting your original file.

---

## 🔧 Common Troubleshooting

### `ImportError: DLL load failed while importing _tkinter`
If you recently upgraded Python (e.g., between Python 3.13 minor releases) or updated your virtual environment on Windows, your environment may point to outdated Tcl/Tk DLL paths.

**Fix:**
1. Verify Tkinter runs on your base Python install:
   ```powershell
   py -m tkinter
   ```
2. If working, re-create your virtual environment so it binds to the new Python installation:
   ```powershell
   Remove-Item -Recurse -Force .\venv
   py -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install Pillow
   ```
3. Alternatively, copy the base Tcl/Tk DLL files to your virtual environment's Scripts folder:
   ```powershell
   Copy-Item "C:\Users\<YourUser>\AppData\Local\Programs\Python\Python313\DLLs\tcl*.dll" -Destination ".\venv\Scripts\"
   Copy-Item "C:\Users\<YourUser>\AppData\Local\Programs\Python\Python313\DLLs\tk*.dll" -Destination ".\venv\Scripts\"
   ```

---

## 🗺️ Roadmap & Planned Features

- [ ] Support for image/logo watermark overlays (PNG with transparency).
- [ ] Font family picker and bold/italic styling options.
- [ ] Batch watermarking for entire folders of photos.
- [ ] Rotation slider for angled watermarks.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).