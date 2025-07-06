# 🧠 **AIVA Chatbot**

**AIVA** is een desktop chatbot aangedreven door **Gemini 2.0 Flash**. Het ondersteunt zowel tekst- als spraakinteracties, een donkere modus en slaat je chatgeschiedenis lokaal op voor naadloze gesprekken.

---

## ✨ **Functies**

* 💬 **Gemini-aangedreven AI-antwoorden**
* 🎤 **Spraakinvoer** via `SpeechRecognition`
* 🔊 **Spraakuitvoer** via `pyttsx3`
* 🌙 **Donkere modus** schakelaar
* 🗃️ **Chatgeschiedenis** opgeslagen in een lokaal bestand
* 🔐 **API-sleutel** prompt bij eerste gebruik
* 📋 **Gebruiksvriendelijk menu** (Geschiedenis wissen, Spraak in-/uitschakelen, Taalkeuze voor TTS, Afsluiten)

---

## 📦 **Vereisten**

Installeer de benodigde dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚀 **Hoe te starten**

### ▶️ Start vanuit de bron (vereist Python):

```bash
python Aiva.chatbot.py
```

### 💻 Start de gecompileerde app:

```bash
dist/AIVA.exe
```

> ℹ️ Bij de eerste keer opstarten wordt om je **Gemini API-sleutel** gevraagd.

---

## 🛠️ **De app bouwen (.exe)**

Gebruik [PyInstaller](https://pyinstaller.org/) om een standalone executable te maken:

```bash
pyinstaller --noconfirm --onefile --windowed --icon=AIVA.ico --name=AIVA Aiva.chatbot.py
```

De output komt in de map `dist/`.

---

## 🚫 **.gitignore**

```gitignore
dist/
build/
__pycache__/
*.exe
*.log
chat_history.txt
```

---

## 🧠 **Notities**

* API-sleutel wordt **alleen in het geheugen gehouden** (niet opgeslagen).
* Zorg voor internetverbinding tijdens gebruik van de API.

---

## ⚠️ **Disclaimer**

Dit project gebruikt de **Google Gemini API** via `google-generativeai`. Je moet je eigen API-sleutel aanleveren om de chatbot te kunnen gebruiken.
