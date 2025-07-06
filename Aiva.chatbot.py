import tkinter as tk
from tkinter import scrolledtext, messagebox, PhotoImage
import speech_recognition as sr
import google.generativeai as genai
import threading
import os
import asyncio
import edge_tts
from playsound import playsound
api_key = None


# === BASISINSTELLINGEN ===
history_file = "chat_history.txt"

# Licht thema standaard
default_bg = "#e9f2fb"
default_accent = "#4a90e2"

# === TEXT-TO-SPEECH ===
async def edge_speak(text, voice="en-US-JennyNeural"):
    filename = "output.mp3"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(filename)
    playsound(filename)
    os.remove(filename)

def speak_text(text):
    lang = voice_language.get()
    voice = "nl-NL-FennaNeural" if lang == 'nl-NL' else "en-US-JennyNeural"
    threading.Thread(target=lambda: asyncio.run(edge_speak(text, voice))).start()

# === STEMINSTELLINGEN ===
def set_voice_language(lang_code):
    print(f"Voice language set to {lang_code}")

def on_voice_language_change(*args):
    lang = voice_language.get()
    set_voice_language(lang)

# === CHATGESCHIEDENIS ===
def save_to_history(speaker, message):
    with open(history_file, "a", encoding="utf-8") as file:
        file.write(f"{speaker}: {message}\n")

def load_history():
    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as file:
            return file.read()
    return ""

def clear_history():
    if os.path.exists(history_file):
        open(history_file, "w").close()
    chat_area.config(state='normal')
    chat_area.delete(1.0, tk.END)
    chat_area.config(state='disabled')

# === GEMINI AI ===
def get_gemini_response(user_input):
    if not client:
        return "Error: API key not set."
    try:
        resp = client.models.generate_content(model='gemini-2.0-flash', contents=user_input)
        return resp.text
    except Exception as e:
        return f"Error: {e}"

# === SPEECH TO TEXT ===
def listen_and_insert():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            chat_area.config(state='normal')
            chat_area.insert(tk.END, "🎙️ Listening...\n", "bot")
            chat_area.config(state='disabled')
            chat_area.see(tk.END)

            audio = recognizer.listen(source, timeout=5)
            lang = voice_language.get()
            text = recognizer.recognize_google(audio, language=lang)
            entry.insert(tk.END, text)
            send_message()
        except Exception as e:
            messagebox.showerror("Voice Input Error", str(e))

# === VERZEND BERICHT ===
def send_message():
    user_input = entry.get().strip()
    if not user_input:
        return

    chat_area.config(state='normal')
    chat_area.insert(tk.END, f"Gebruiker: {user_input}\n", "user")
    chat_area.see(tk.END)
    entry.delete(0, tk.END)
    save_to_history("Gebruiker", user_input)

    if not api_key:
        chat_area.insert(tk.END, "AIVA: Error: API key not set.\n", "bot")
        chat_area.config(state='disabled')
        return

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(user_input)

        if hasattr(response, "text"):
            bot_resp = response.text
        else:
            bot_resp = "Geen geldig antwoord ontvangen."
    except Exception as e:
        bot_resp = f"Er ging iets mis:\n{str(e)}"

    chat_area.insert(tk.END, f"AIVA: {bot_resp}\n\n", "bot")
    save_to_history("AIVA", bot_resp)

    if voice_output_enabled.get():
        speak_text(bot_resp)

    chat_area.config(state='disabled')
    chat_area.see(tk.END)



# === DARK MODE TOGGLE ===
def toggle_dark_mode():
    if dark_mode_enabled.get():
        bg, fg = "#2E2E2E", "white"
        chat_area.configure(bg="#1E1E1E", fg=fg, insertbackground=fg)
        entry.configure(bg="#2B2B2B", fg=fg, insertbackground=fg)
        entry_frame.configure(bg=bg)
        root.configure(bg=bg)
        title.configure(bg=bg, fg=fg)
        chat_area.tag_config("user", foreground=fg)
        chat_area.tag_config("bot", foreground=fg)
    else:
        bg, fg = default_bg, "black"
        chat_area.configure(bg="white", fg=fg, insertbackground=fg)
        entry.configure(bg="white", fg=fg, insertbackground=fg)
        entry_frame.configure(bg=bg)
        root.configure(bg=bg)
        title.configure(bg=bg, fg=default_accent)
        chat_area.tag_config("user", foreground="black")
        chat_area.tag_config("bot", foreground=default_accent)



# === API POPUP ===
def ask_for_api():
    def on_close():
        if not api_entry.get().strip():
            root.destroy()

    def save_api():
        global api_key
        api = api_entry.get().strip()

        if not api:
            messagebox.showerror("Error", "Voer een API-sleutel in.")
            return

        try:
            genai.configure(api_key=api)
            model = genai.GenerativeModel("gemini-1.5-flash")
            test_resp = model.generate_content("Hallo!")
            if not hasattr(test_resp, 'text'):
                raise Exception("Ongeldig AI antwoord.")

            api_key = api  # <-- Hier sla je de werkende sleutel op
            api_window.destroy()

        except Exception as e:
            messagebox.showerror("API Error", f"Verbinding mislukt:\n{str(e)}")

    api_window = tk.Toplevel(root)
    api_window.geometry('500x100')
    api_window.title("API-sleutel invoeren")
    # Voeg logo toe aan popupvenster (icoon rechtsboven)
    try:
        api_window.iconphoto(False, logo)
    except:
        pass
    api_window.transient(root)
    api_window.grab_set()
    api_window.focus()
    api_window.protocol("WM_DELETE_WINDOW", on_close)
    tk.Label(api_window, text='API Key:').pack(side='left', padx=10, pady=20)
    api_entry = tk.Entry(api_window)
    api_entry.pack(side='left', fill=tk.X, expand=True, padx=10)
    tk.Button(api_window, text="Verstuur", command=save_api).pack(side='left', padx=10)
    api_entry.focus()



# === GUI ===
import os

root = tk.Tk()
ico_path = os.path.abspath("logo.ico")
root.iconbitmap(ico_path)
root.title("AIVA - Jouw Chatbot Assistent")
root.geometry("550x600")
root.configure(bg=default_bg)



try:
    logo = PhotoImage(file="AIVALOGO.png")
    root.iconphoto(False, logo)
    logo_img = logo.subsample(2, 2)
    tk.Label(root, image=logo_img, bg=default_bg).pack(pady=10)
except:
    tk.Label(root, text="AIVA", font=("Arial", 24, "bold"), bg=default_bg, fg=default_accent).pack(pady=10)

# === Variabelen ===
voice_output_enabled = tk.BooleanVar(value=False)
dark_mode_enabled = tk.BooleanVar(value=False)
voice_language = tk.StringVar(value='en-US')
voice_language.trace_add('write', on_voice_language_change)

# === Menu ===
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

# === Titel ===
title = tk.Label(root, text="AIVA", font=("Arial", 18), bg=default_bg, fg=default_accent)
title.pack()

# === Chat ===
chat_area = scrolledtext.ScrolledText(root, height=20, width=65, state='disabled', font=("Arial", 10), bg="white")
chat_area.pack(pady=10)
chat_area.tag_config("user", foreground="black")
chat_area.tag_config("bot", foreground=default_accent)

# === Invoerveld ===
entry_frame = tk.Frame(root, bg=default_bg)
entry_frame.pack(pady=5, fill=tk.X, padx=10)

# === Layoutconfiguratie (zorgt dat het veld meegroeit) ===
entry_frame.columnconfigure(0, weight=1)

# === Invoerveld ===
entry = tk.Entry(entry_frame, font=("Arial", 12))
entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))
entry.bind("<Return>", lambda event: send_message())

# === Verzendknop ===
send_button = tk.Button(entry_frame, text="Stuur naar AIVA", font=("Arial", 11, "bold"),
                        command=send_message, bg=default_accent, fg="white", width=16)
send_button.grid(row=0, column=1, padx=5)

# === Microfoonknop ===
mic_button = tk.Button(entry_frame, text="🎤", font=("Arial", 11),
                       command=lambda: threading.Thread(target=listen_and_insert).start())
mic_button.grid(row=0, column=2)



# === Start ===
chat_area.config(state='normal')
chat_area.insert(tk.END, load_history())
chat_area.config(state='disabled')
toggle_dark_mode()
set_voice_language(voice_language.get())
ask_for_api()
root.mainloop()
