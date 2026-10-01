<!-- ============================================================
     📄 FILE:      README.md
     📁 PATH:      social_media/facebook/story_video/README.md
     🎯 PURPOSE:   Documentation for Facebook Story pipeline
     ============================================================ -->

# 📘 Facebook Story Video

Automated daily Facebook Story video generation with **3-language display** (Hindi + Arabic + English).

---

## ✨ Features

1. Hadith fetch (multi-API, 50-100 word filter)
2. Hindi translation (DeepL + AI fallback)
3. Voice generation (ElevenLabs + edge-tts)
4. Background music (Freesound + Pixabay)
5. Background video (Pexels + Pixabay)
6. 3-Language word-by-word display
7. Intro (Bismillah + Logo + Gold line)
8. Outro (JazakAllah + CTA buttons)
9. Sparkles + Progress bar
10. Google Drive backup
11. Facebook Story upload
12. Combined Telegram report

---

## ⏱️ Timing

| Section | Duration |
|---------|----------|
| Intro   | 2 seconds |
| Main    | 50-55 seconds |
| Outro   | 2 seconds |
| **Total** | **54-59 seconds** |

---

## 🚀 Run Locally

```bash
pip install -r requirements.txt
python3 G_entry/G2_run_story.py
