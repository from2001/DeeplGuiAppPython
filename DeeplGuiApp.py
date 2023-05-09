import requests
import tkinter as tk
from tkinter import messagebox
import os

API_KEY_FILE = 'api_key.txt'


def save_api_key(api_key):
    with open(API_KEY_FILE, 'w') as f:
        f.write(api_key)


def load_api_key():
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, 'r') as f:
            return f.read().strip()
    return ""


def translate_text(text, api_key):
    url = "https://api.deepl.com/v2/translate"
    payload = {
        "auth_key": api_key,
        "text": text,
        "source_lang": "JA",
        "target_lang": "EN",
        "split_sentences": "0",
        "tag_handling": "xml",
    }

    response = requests.post(url, data=payload)
    result = response.json()

    if response.status_code == 200:
        return result["translations"][0]["text"]
    else:
        messagebox.showerror("エラー", "翻訳できませんでした。")
        return None


def on_translate_button_click():
    translate_button.config(state="disabled")
    input_text = input_textbox.get("1.0", "end-1c")
    api_key = api_key_entry.get()
    translated_text = translate_text(input_text, api_key)
    if translated_text is not None:
        output_textbox.config(state="normal")
        output_textbox.delete("1.0", "end")
        output_textbox.insert("1.0", translated_text)
        output_textbox.config(state="disabled")
    translate_button.config(state="normal")


def on_closing():
    api_key = api_key_entry.get()
    save_api_key(api_key)
    app.destroy()



app = tk.Tk()
app.title("日本語から英語への翻訳アプリ")
app.geometry("800x600")  # Set initial size

# Configure grid to expand with window
app.grid_rowconfigure(0, weight=0)  # API key row
app.grid_rowconfigure(1, weight=0)  # API key entry row
app.grid_rowconfigure(2, weight=0)  # Input label row
app.grid_rowconfigure(3, weight=1)  # Input textbox row
app.grid_rowconfigure(4, weight=0)  # Translate button row
app.grid_rowconfigure(5, weight=0)  # Output label row
app.grid_rowconfigure(6, weight=1)  # Output textbox row
app.grid_columnconfigure(0, weight=1)

api_key_label = tk.Label(app, text="DeepL API Key:")
api_key_label.grid(row=0, column=0, sticky="w")

api_key_entry = tk.Entry(app, show="*")
api_key_entry.grid(row=1, column=0, sticky="ew")
api_key_entry.insert(0, load_api_key())

input_label = tk.Label(app, text="日本語:")
input_label.grid(row=2, column=0, sticky="nw")

input_textbox = tk.Text(app, wrap="word")
input_textbox.grid(row=3, column=0, sticky="nsew")

translate_button = tk.Button(app, text="翻訳", command=on_translate_button_click)
translate_button.grid(row=4, column=0)

output_label = tk.Label(app, text="英語:")
output_label.grid(row=5, column=0, sticky="nw")

output_textbox = tk.Text(app, wrap="word", state="disabled")
output_textbox.grid(row=6, column=0, sticky="nsew")

app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()