import os
import tkinter as tk
from tkinter import scrolledtext, messagebox, PhotoImage
import threading
import asyncio
import speech_recognition as sr
from playsound import playsound
import edge_tts
import google.generativeai as genai

# ========== CONFIG ========== #
HISTORY_FILE = "chat_history.txt"
DEFAULT_BG = "#e9f2fb"
DEFAULT_ACCENT = "#4a90e2"
VOICE_EN = "en-US-JennyNeural"
VOICE_NL = "nl-NL-FennaNeural"
LOGO_PATH = "AIVALOGO.png"
ICO_PATH = os.path.abspath("../AIVA.ico")
API_KEY = None

# ========== CHAT MEMORY ========== #
chat_history = []

# ========== TEXT-TO-SPEECH ========== #
async def edge_speak(text, voice=VOICE_EN):
    filename = "output.mp3"
    await edge_tts.Communicate(text, voice).save(filename)
    playsound(filename)
    os.remove(filename)

def speak_text(text):
    lang = voice_language.get()
    voice = VOICE_NL if lang == 'nl-NL' else VOICE_EN
    threading.Thread(target=lambda: asyncio.run(edge_speak(text, voice))).start()

# ========== GEMINI AI ========== #
def get_gemini_response(history):
    if not API_KEY:
        return "Error: API key not set."
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(history)
        return response.text if hasattr(response, "text") else "Geen geldig antwoord ontvangen."
    except Exception as e:
        return f"Er ging iets mis:\n{str(e)}"

# ========== CHATGESCHIEDENIS ========== #
def save_to_history(speaker, message):
    with open(HISTORY_FILE, "a", encoding="utf-8") as file:
        file.write(f"{speaker}: {message}\n")

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            return file.read()
    return ""

def clear_history():
    global chat_history
    chat_history = []
    if os.path.exists(HISTORY_FILE):
        open(HISTORY_FILE, "w").close()
    chat_area.config(state='normal')
    chat_area.delete(1.0, tk.END)
    chat_area.config(state='disabled')

# ========== STEM NAAR TEKST ========== #
def listen_and_insert():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            chat_area.config(state='normal')
            chat_area.insert(tk.END, "🎙️ Listening...\n", "bot")
            chat_area.config(state='disabled')
            chat_area.see(tk.END)
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language=voice_language.get())
            entry.insert(tk.END, text)
            send_message()
        except Exception as e:
            messagebox.showerror("Voice Input Error", str(e))

# ========== BERICHT VERZENDEN ========== #
def send_message():
    user_input = entry.get().strip()
    if not user_input:
        return
    entry.delete(0, tk.END)
    chat_area.config(state='normal')
    chat_area.insert(tk.END, f"Gebruiker: {user_input}\n", "user")
    save_to_history("Gebruiker", user_input)
    chat_area.see(tk.END)

    chat_history.append({"role": "user", "parts": user_input})

    bot_resp = get_gemini_response(chat_history)

    chat_history.append({"role": "model", "parts": bot_resp})

    chat_area.insert(tk.END, f"AIVA: {bot_resp}\n\n", "bot")
    save_to_history("AIVA", bot_resp)
    if voice_output_enabled.get():
        speak_text(bot_resp)

    chat_area.config(state='disabled')
    chat_area.see(tk.END)

# ========== DONKER THEMA ========== #
def toggle_dark_mode():
    is_dark = dark_mode_enabled.get()
    bg = "#2E2E2E" if is_dark else DEFAULT_BG
    fg = "white" if is_dark else "black"
    chat_bg = "#1E1E1E" if is_dark else "white"
    entry_bg = "#2B2B2B" if is_dark else "white"

    root.configure(bg=bg)
    entry_frame.configure(bg=bg)
    chat_area.configure(bg=chat_bg, fg=fg, insertbackground=fg)
    entry.configure(bg=entry_bg, fg=fg, insertbackground=fg)
    title.configure(bg=bg, fg=fg if is_dark else DEFAULT_ACCENT)
    logo_label.configure(bg=bg)

    chat_area.tag_config("user", foreground=fg)
    chat_area.tag_config("bot", foreground=DEFAULT_ACCENT if not is_dark else fg)

# ========== API-SLEUTEL POPUP ========== #
def ask_for_api():
    def save_api():
        global API_KEY
        api = api_entry.get().strip()
        if not api:
            messagebox.showerror("Error", "Voer een API-sleutel in.")
            return
        try:
            genai.configure(api_key=api)
            if not hasattr(genai.GenerativeModel("gemini-1.5-flash").generate_content("Hallo!"), 'text'):
                raise Exception("Ongeldig AI antwoord.")
            API_KEY = api
            api_window.destroy()
        except Exception as e:
            messagebox.showerror("API Error", f"Verbinding mislukt:\n{str(e)}")

    def on_close():
        if not api_entry.get().strip():
            root.destroy()

    api_window = tk.Toplevel(root)
    api_window.title("API-sleutel invoeren")
    api_window.geometry('500x100')
    api_window.transient(root)
    api_window.grab_set()
    api_window.focus()
    api_window.protocol("WM_DELETE_WINDOW", on_close)

    try:
        api_window.iconphoto(False, logo)
    except:
        pass

    tk.Label(api_window, text='API Key:').pack(side='left', padx=10, pady=20)
    api_entry = tk.Entry(api_window)
    api_entry.pack(side='left', fill=tk.X, expand=True, padx=10)
    tk.Button(api_window, text="Verstuur", command=save_api).pack(side='left', padx=10)
    api_entry.focus()

# ========== MAIN GUI ========== #
root = tk.Tk()
root.title("AIVA - Jouw Chatbot Assistent")
root.geometry("550x600")
root.configure(bg=DEFAULT_BG)
root.iconbitmap(ICO_PATH)

# === Logo / Titel === #
try:
    logo = PhotoImage(file=LOGO_PATH)
    root.iconphoto(False, logo)
    logo_img = logo.subsample(2, 2)
    logo_label = tk.Label(root, image=logo_img, bg=DEFAULT_BG)
    logo_label.pack(pady=10)
except:
    logo_label = tk.Label(root, text="AIVA", font=("Arial", 24, "bold"), bg=DEFAULT_BG, fg=DEFAULT_ACCENT)
    logo_label.pack(pady=10)

title = tk.Label(root, text="AIVA", font=("Arial", 18), bg=DEFAULT_BG, fg=DEFAULT_ACCENT)
title.pack()

# === Variabelen === #
voice_output_enabled = tk.BooleanVar(value=False)
dark_mode_enabled = tk.BooleanVar(value=False)
voice_language = tk.StringVar(value='en-US')
voice_language.trace_add('write', lambda *args: None)

# === Menu === #
menu = tk.Menu(root)
settings = tk.Menu(menu, tearoff=0)
settings.add_checkbutton(label="Donker Thema", variable=dark_mode_enabled, command=toggle_dark_mode)
settings.add_checkbutton(label="Stem Uitspraak", variable=voice_output_enabled)
lang_menu = tk.Menu(settings, tearoff=0)
lang_menu.add_radiobutton(label="Engels", variable=voice_language, value='en-US')
lang_menu.add_radiobutton(label="Nederlands", variable=voice_language, value='nl-NL')
settings.add_cascade(label="Taalinvoer", menu=lang_menu)
settings.add_command(label="Verwijder geschiedenis", command=clear_history)
menu.add_cascade(label="Opties", menu=settings)
root.config(menu=menu)

# === Chatveld === #
chat_area = scrolledtext.ScrolledText(root, height=20, width=65, state='disabled', font=("Arial", 10), bg="white")
chat_area.pack(pady=10)
chat_area.tag_config("user", foreground="black")
chat_area.tag_config("bot", foreground=DEFAULT_ACCENT)

# === Invoerveld + Knoppen === #
entry_frame = tk.Frame(root, bg=DEFAULT_BG)
entry_frame.pack(pady=5, fill=tk.X, padx=10)
entry_frame.columnconfigure(0, weight=1)

entry = tk.Entry(entry_frame, font=("Arial", 12))
entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
entry.bind("<Return>", lambda event: send_message())

tk.Button(entry_frame, text="Stuur naar AIVA", font=("Arial", 11, "bold"),
          command=send_message, bg=DEFAULT_ACCENT, fg="white", width=16).grid(row=0, column=1, padx=5)

tk.Button(entry_frame, text="🎤", font=("Arial", 11),
          command=lambda: threading.Thread(target=listen_and_insert).start()).grid(row=0, column=2)

# === Startprogramma === #
chat_area.config(state='normal')
chat_area.insert(tk.END, load_history())
chat_area.config(state='disabled')
toggle_dark_mode()
ask_for_api()
root.mainloop()
