# SawajStudio — Facebook Story Module (01)

Morning Islamic Story video generator (5:00 AM IST daily).

## Features
- Fetches random Hadith (Bukhari/Muslim/AbuDawud/Tirmidhi)
- Translates to Hindi (DeepL + AI fallback)
- Generates voiceover (ElevenLabs → edge-tts fallback)
- Auto background, music, subtitles, frames
- Uploads to Facebook Story + Instagram Story
- Uploads final to Google Drive

## Run Locally
```bash
pip install -r requirements.txt
cp env.example .env
# fill .env with your keys
python -m runners.run_story
