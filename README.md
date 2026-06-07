<div align="center">

# 🪶 The Multimodal Storyteller

### *An AI-powered interactive narrative engine — forge worlds, shape destinies, and watch your saga come alive.*

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/Gemini%201.5%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![Stability AI](https://img.shields.io/badge/Stable%20Diffusion%20v1.6-7C3AED?style=for-the-badge&logo=stability-ai&logoColor=white)](https://stability.ai/)

✦ ─────────────────────────────────────────── ✦

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🌍 **World Forge** | Generate a living "World Bible" from your chosen theme, protagonist archetype, and core contradiction — ensuring every chapter feels cohesive. |
| 📖 **Interactive Narrative** | Three choices guide each chapter. Two follow the plot's logic — the third is a **Wildcard** that bends reality in surprising directions. |
| 🎨 **AI-Generated Art** | Every chapter is illustrated by Stable Diffusion, producing a unique artwork from the narrative you co-created in real time. |
| 🔊 **Audio Narration** | Listen to your entire saga with browser-native text-to-speech. Play, pause, or stop — your story, your pace. |
| 🧠 **Stateful Memory** | The app remembers your full story arc, world lore, and every decision — guaranteeing a continuous, coherent adventure. |

---

## 🛠️ Tech Stack & Architecture

This project orchestrates multiple AI services to create a seamless multimodal experience.

| Layer | Technology | Role |
|-------|-----------|------|
| **UI Framework** | [Streamlit](https://streamlit.io/) | Interactive web application |
| **Narrative Engine** | [Google Gemini 1.5 Flash](https://ai.google.dev/) | Story director & world builder |
| **Image Generation** | [Stable Diffusion v1.6](https://stability.ai/) via Stability.ai API | Chapter artwork creation |
| **Audio** | Browser `window.speechSynthesis` Web API | Text-to-speech narration |
| **Language** | Python 3.8+ | Core backend |

### ⚙️ How It Works

The app runs a powerful 4-step loop per chapter:

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   I. User chooses a path  ──►  II. Gemini acts as Director │
│                                         │                  │
│                                         ▼                  │
│   IV. Streamlit renders  ◄──  III. Stability.ai paints     │
│       the full chapter                  the scene          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Gemini returns a structured JSON per chapter:**

```json
{
  "narrative_chapter": "The next story segment...",
  "next_choices": ["Choice A", "Choice B", "⚡ Wildcard"],
  "image_prompt": "A descriptive prompt for Stable Diffusion..."
}
```

---

## 🚀 Getting Started

### Prerequisites

- Python **3.8** or newer
- `pip` for package installation
- API keys from [Google AI Studio](https://makersuite.google.com/app/apikey) and [Stability.ai](https://platform.stability.ai/account/keys)

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/Karthik-1221/Multimodal-story-Teller-V2.git
cd Multimodal-story-Teller-V2
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Configure API keys**

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY="your_google_api_key_here"
STABILITY_API_KEY="your_stability_api_key_here"
```

> 💡 **New to Stability.ai?** New accounts receive free credits — perfect for development and experimentation.

**4. Run the application**

```bash
streamlit run app.py
```

---

## 📜 Usage Guide

| Step | Action |
|------|--------|
| **Forge Your World** | Select a theme, archetype, and contradiction to generate your world's lore and atmosphere. |
| **Begin Your Saga** | Write the opening sentence — the spark that ignites your story. |
| **Weave the Story** | Read each chapter, admire the generated artwork, then choose one of three paths. Click **"Weave Next Chapter"** to proceed. |
| **Narrate** | Use the audio controls to play, pause, or stop the text-to-speech narration of your full saga. |
| **New Saga** | Hit **"Start a New Saga (Restart)"** at any time to wipe the slate and begin a fresh adventure. |

---

## 👤 Author

**Karthik Boodidha** — Data Scientist & Backend Developer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/karthik-boodidha)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/Karthik-1221)
[![Portfolio](https://img.shields.io/badge/Portfolio-FF6B35?style=flat-square&logo=codeforces&logoColor=white)](https://codebasics.io/portfolio/Karthik-Boodidha)
[![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=flat-square&logo=kaggle&logoColor=white)](https://www.kaggle.com/boodidhakarthik)

---

## 🙏 Acknowledgements

- **[Google](https://ai.google.dev/)** — For the powerful Gemini language model that acts as the narrative brain behind every chapter.
- **[Stability AI](https://stability.ai/)** — For providing a robust, high-quality image generation API.
- **[Streamlit](https://streamlit.io/)** — For making interactive AI apps incredibly fun and fast to build.

---

<div align="center">

✦ &nbsp; *Every great saga begins with a single choice.* &nbsp; ✦

**[⭐ Star this repo](https://github.com/Karthik-1221/Multimodal-story-Teller-V2)** if you found it interesting!

</div>
