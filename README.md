# 🧠 **AIVA Chatbot**

**AIVA** is a desktop chatbot powered by **Gemini 2.0 Flash**. It supports both text and voice interactions, dark mode, and saves your chat history locally for seamless conversations.

---

## ✨ **Features**

* 💬 **Gemini-powered AI responses**
* 🎤 **Voice input** using `SpeechRecognition`
* 🔊 **Voice output** using `pyttsx3`
* 🌙 **Dark Mode** toggle
* 🗃️ **Chat history** saved to local file
* 🔐 **API Key** prompt on first run
* 📋 **User-friendly menu** (Clear History, Voice toggle, Language Selection for TTS, Exit)

---

## 📦 **Requirements**

Install the necessary dependencies:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install tk pyttsx3 SpeechRecognition google-generativeai
```

---

## 🚀 **How to Run**

### ▶️ Run from source (requires Python):

```bash
python aiva.py
```

### 💻 Run the compiled app:

```bash
dist/AIVA.exe
```

> ℹ️ First launch will ask for your **Gemini API Key**.

---

## 🛠️ **Build the App (.exe)**

Use [PyInstaller](https://pyinstaller.org/) to compile to a standalone executable:

```bash
pyinstaller --noconfirm --onefile --windowed --icon=AIVA.ico --name=AIVA main.py
```

Output will be in the `dist/` folder.

---

## 📁 **Project Structure**

```
📂 AIVA-Chatbot/
├── main.py              # Main application file
├── README.md            # Project documentation
├── requirements.txt     # Python libraries
├── .gitignore           # Git ignored files
├── dist/                # Executable output folder
├── build/               # PyInstaller build folder
└── chat_history.txt     # Auto-generated chat history
```

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

## 🧠 **Notes**

* API key is **only kept in memory** (not saved).
* Ensure internet access during API use.

---

## ⚠️ **Disclaimer**

This project uses **Google Gemini API** via `google-generativeai`. You must provide your own API key to use the chatbot.
