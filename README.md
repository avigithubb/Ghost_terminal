# 👻 The Last Developer

### A haunted terminal. An AI that remembers. A computer that doesn't want you to leave.

**The Last Developer** is an experimental AI-powered horror chatbot that transforms an ordinary terminal into a mysterious, unsettling computer experience.

Inspired by the eerie talking computer from *Courage the Cowardly Dog* and the memory-retaining diary from *Harry Potter*, this project combines local AI inference, persistent conversation memory, terminal effects, and voice synthesis to create an interactive horror experience.

Unlike a conventional chatbot, this computer develops a personality over time. It starts out friendly, becomes increasingly suspicious, and can eventually turn hostile.

But something is not quite right about it.

---

## 🎬 Demo

**Demo Video:** 
<img href="https://www.youtube.com/watch?v=0c8fQcmnvec" />
---

## ✨ Features

### 🧠 AI-Powered Conversations
- Uses Google's Gemma open-weight model through Ollama.
- Runs AI inference locally on your machine.
- Generates dynamic responses based on the conversation.
- Maintains a horror-themed personality rather than behaving like a conventional AI assistant.

### 👁️ Evolving Personality

The computer has multiple personality states:

| Personality | Behaviour |
|---|---|
| Friendly | Welcoming, innocent, and occasionally unusual. |
| Suspicious | Cryptic responses, strange observations, and unsettling remarks. |
| Hostile | Aggressive language, uppercase responses, and glitch effects. |
| Imposter | Pretends to be the original friendly computer while revealing inconsistencies. |

### 💾 Persistent Memory
- Stores conversation history using SQLite.
- Remembers previous interactions across application restarts.
- Uses stored context to make conversations feel continuous.

### 🔊 Voice Interaction
- Integrates ElevenLabs for AI voice synthesis.
- Supports spoken responses alongside terminal output.
- Plays unsettling warning beeps during randomly triggered disturbances.
- Follows disturbances with a spoken apology.

### 💻 Haunted Terminal Interface
- Built with Python and Rich.
- Animated startup sequence.
- Character-by-character text rendering.
- Glitch effects and unsettling visual interactions.
- Mood-dependent terminal presentation.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Ollama | Local AI model execution |
| Gemma 3 | Open-weight language model |
| SQLite | Persistent conversation memory |
| Rich | Terminal interface and formatting |
| ElevenLabs API | Voice synthesis |
| Pygame | Audio playback |
| Python-dotenv | Environment variable management |
| Windows winsound | Warning beep effects |

---

## 🏗️ Project Structure

```text
the-last-developer/
│
├── main.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
│
├── effects/
│   ├── __init__.py
│   ├── interface.py
│   └── voice.py
│
├── ghost/
│   ├── __init__.py
│   ├── ai_engine.py
│   └── memory.py
│
└── data/
    └── memory.db
```

### Core Components

**`main.py`**
- Application entry point.
- Manages the conversation loop.
- Handles user commands and personality transitions.
- Coordinates AI responses, voice playback, and terminal effects.

**`ghost/ai_engine.py`**
- Handles communication with the local Ollama model.
- Generates responses using the computer's personality and conversation context.

**`ghost/memory.py`**
- Manages persistent conversation memory.
- Uses SQLite to store and retrieve previous interactions.

**`effects/interface.py`**
- Handles terminal formatting and animations.
- Manages personality-dependent visual effects.
- Implements warning beeps and disturbance sequences.

**`effects/voice.py`**
- Handles voice synthesis and audio playback.
- Manages the voice response queue.

---

## 🚀 Getting Started

Follow these steps to run The Last Developer locally.

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/the-last-developer.git
cd the-last-developer
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, use:

```powershell
.venv\Scripts\activate.bat
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama

Download and install Ollama:

https://ollama.com/download

After installation, download the Gemma model:

```bash
ollama pull gemma3:4b
```

The project uses local Ollama inference, so make sure Ollama is running before launching the application.

If your system has limited resources, you can use a smaller model such as:

```bash
ollama pull gemma3:1b
```

> Make sure the model configured in the application matches the model installed in Ollama.

### 5. Configure environment variables

Create a `.env` file in the project root.

```env
ELEVENLABS_API_KEY=your_elevenlabs_api_key
ELEVENLABS_VOICE_ID=your_elevenlabs_voice_id
```

Get your API key from:

https://elevenlabs.io/

Voice synthesis requires valid ElevenLabs API access. Keep your API key private.

### 6. Run the application

```bash
python main.py
```

The haunted terminal should initialize and begin its conversation.

---

## ⌨️ Available Commands

| Command | Description |
|---|---|
| `/help` | Displays available commands. |
| `/clear` | Clears the terminal screen. |
| `/about` | Displays information about the computer. |
| `/exit` | Exits the application. |
| `/imposter on` | Activates imposter personality mode. |
| `/imposter off` | Deactivates imposter personality mode. |
| `/mood friendly` | Changes the personality to friendly. |
| `/mood suspicious` | Changes the personality to suspicious. |
| `/mood hostile` | Changes the personality to hostile. |
| `/voice on` | Enables voice responses. |
| `/voice off` | Disables voice responses. |

---

## 🧩 How It Works

The application combines local language-model inference with a persistent memory system and a terminal presentation layer.

```text
              USER INPUT
                  |
                  v
             main.py
                  |
          +-------+-------+
          |               |
          v               v
       AI Engine       Memory System
          |               |
          v               v
       Ollama           SQLite
       Gemma 3
          |
          v
     AI RESPONSE
          |
     +----+----+
     |         |
     v         v
 Terminal   Voice Engine
 Interface  ElevenLabs
     |
     v
 Personality Effects
     |
     v
 Disturbance Sequence
```

The AI engine generates responses using the selected personality and conversation context. The memory system stores interactions so the computer can refer to previous conversations.

The terminal interface presents the responses using animated text and mood-dependent effects. When voice is enabled, the voice engine also synthesizes and plays the responses.

---

## 🔐 Privacy and Safety

One of the primary goals of this project is to experiment with locally hosted AI.

- The language model runs locally through Ollama.
- Conversation memory is stored in a local SQLite database.
- The project does not execute operating-system commands on the user's behalf.
- It is a fictional horror chatbot, not a real terminal or shell emulator.
- ElevenLabs is an external service used for voice synthesis when configured.

**Important:** Never commit API keys, private conversation databases, or other sensitive information to a public repository.

---

## 🌱 Why Local AI?

The Last Developer uses Gemma through Ollama to demonstrate how open-weight AI models can power interactive applications without depending on a cloud-hosted language-model API.

Local inference offers several advantages:

- Greater control over model selection.
- Reduced dependence on external AI inference services.
- Local processing of chatbot conversations.
- Flexibility to experiment with different open-weight models.

The project also demonstrates how local AI can be combined with external services when additional capabilities, such as realistic voice synthesis, are required.

---

## 🔮 Future Improvements

Some ideas for future development:

- Additional personality states and hidden interactions.
- More advanced long-term memory and contextual recall.
- Customizable voice personalities.
- More dynamic terminal glitches and visual effects.
- Support for additional Ollama-compatible models.
- A web-based interface for browser interaction.

---

## 🤝 Contributing

Contributions are welcome!

If you have ideas for improving the haunted terminal experience, feel free to:

1. Fork this repository.
2. Create a new branch.
3. Implement your changes.
4. Submit a pull request.

```bash
git checkout -b feature/your-feature-name
git add .
git commit -m "Add: your feature description"
git push origin feature/your-feature-name
```

Please keep contributions aligned with the project's fictional horror theme and local-AI focus.

---

## 📜 License

This project is open source. See the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Abhishek Napit**

GitHub: [YOUR_GITHUB_PROFILE](https://github.com/YOUR_USERNAME)

---

*Some computers are built to answer questions.*

*This one remembers who asked them.*

**The Last Developer — Are you still there?**
