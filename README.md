# 🎨 QR Code Maker

A professional-grade QR Code Generator built with [Streamlit](https://streamlit.io/).  
Easily create custom QR codes with logo embedding, high error correction, and a clean, user-friendly interface.

🔗 **Live Demo:** [https://qrcode-maker.streamlit.app/](https://qrcode-maker.streamlit.app/)

---

## ✨ Features

- **Customizable QR Codes** – Enter any text/URL to generate instantly.
- **Logo Embedding** – Add logos to your QR codes without breaking scanability.
- **High Error Correction** – Uses `ERROR_CORRECT_H` (up to 30% damage tolerance).
- **Responsive UI** – Streamlit-powered layout, looks great on desktop & mobile.
- **Download Support** – Save generated QR codes as PNG images.
- **Professional Styling** – Black QR codes on white background for maximum readability.

---

## 🖼️ Preview

![QR Code Example](https://raw.githubusercontent.com/yourusername/yourrepo/main/preview.png)  
*(Optional – replace with an actual screenshot from your app)*

---

## 📂 Code Structure

- **`streamlit_qr_code_app.py`** → Main app file
- **`requirements.txt`** → Dependencies list
- **Libraries Used:**
  - `streamlit` → Web app framework
  - `qrcode[pil]` → QR code generation
  - `pillow (PIL)` → Image processing, logo handling
  - `io` → Handling downloads

---

## 🚀 Installation & Usage

Clone this repository and install dependencies:

```bash
git clone https://github.com/yourusername/qrcode-maker.git
cd qrcode-maker
pip install -r requirements.txt
