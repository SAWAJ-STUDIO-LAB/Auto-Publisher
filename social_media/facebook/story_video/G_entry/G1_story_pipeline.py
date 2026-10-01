# ============================================================
# 📄 FILE:      G1_story_pipeline.py
# 📁 PATH:      social_media/facebook/story_video/G_entry/G1_story_pipeline.py
# 🎯 PURPOSE:   Orchestrate all steps — main pipeline
# ============================================================

import os
import traceback
from mutagen.mp3 import MP3

from A_core.A5_base_pipeline import BasePipeline
from A_core.A2_logger import log_file_start, log_file_end, log_step, log_error
from C_content.C1_hadith import Hadith
from C_content.C2_ai_provider import AIProvider
from C_content.C3_translator import Translator
from C_content.C4_tts import TTS
from C_content.C5_music import Music
from C_content.C6_background import Background
from C_content.C7_logo_processor import LogoProcessor
from C_content.C8_thumbnail import Thumbnail
from D_video.D4_frames import Frames
from D_video.D6_composer import Composer
from E_audio.E1_voice_ducking import VoiceDucking
from E_audio.E3_mastering import Mastering
from F_upload.F1_drive import Drive
from F_upload.F2_upload_story import StoryUploader


# ─────────────────────────────────────────────────────────────
# ① STORY PIPELINE CLASS
# ─────────────────────────────────────────────────────────────
class StoryPipeline(BasePipeline):
    """Main orchestrator for Facebook Story generation."""

    # ─────────────────────────────────────────────────────────
    # ② RUN — main pipeline
    # ─────────────────────────────────────────────────────────
    def run(self):
        from A_core.A3_telegram import header

        log_file_start("G1_story_pipeline.py", "Full pipeline orchestration")
        header("FACEBOOK MORNING STORY")

        try:
            # ═══════════════ INIT MODULES ═══════════════
            ai = AIProvider(self)
            translator = Translator(self, ai)
            tts = TTS(self)
            music = Music(self)
            bg = Background(self)
            logo_proc = LogoProcessor()
            frames = Frames()
            composer = Composer(self)
            hadith = Hadith(self)
            drive = Drive(self)
            uploader = StoryUploader(self)
            thumbnail = Thumbnail(self)
            ducking = VoiceDucking(self)
            mastering = Mastering(self)

            # ═══════════════ STEP 1: FETCH HADITH ═══════════════
            header("STEP 1: Fetch Hadith")
            h = hadith.fetch()
            log_step("G1_story_pipeline.py", "Hadith fetched", "ok",
                     f"{h['collection']} #{h['number']}")

            # ═══════════════ STEP 2: TRANSLATE ═══════════════
            header("STEP 2: Hindi Translation")
            hindi = translator.to_hindi(h["english"])
            log_step("G1_story_pipeline.py", "Translation done", "ok")

            # ═══════════════ STEP 3: TTS ═══════════════
            header("STEP 3: Text-to-Speech")
            tts.generate(f"हदीस शरीफ। {hindi}", "s_raw.mp3")
            mastering.master_voice("s_raw.mp3", "s_v.mp3")
            voice_dur = MP3("s_v.mp3").info.length
            log_step("G1_story_pipeline.py", "Voice ready", "ok",
                     f"{voice_dur:.1f}s")

            # ═══════════════ STEP 4: MUSIC ═══════════════
            header("STEP 4: Background Music")
            music.get("music_soft.mp3")
            ducking.mix("s_v.mp3", "music_soft.mp3", "s_voice.mp3", voice_dur)

            # ═══════════════ STEP 5: BACKGROUND ═══════════════
            header("STEP 5: Background Video")
            bg_dur = voice_dur + 2.0 + 2.0 + 0.5  # voice + intro + outro + buffer
            bg_file = bg.get(bg_dur)

            # ═══════════════ STEP 6: LOGO ═══════════════
            header("STEP 6: Logo Processing")
            has_logo = logo_proc.make("avatar.png")

            # ═══════════════ STEP 7: FRAMES ═══════════════
            header("STEP 7: Generate Frames")
            hadith_label = f"#{h['number']} · {h['collection']}"
            total = frames.generate(
                voice_dur, has_logo,
                hindi=hindi,
                urdu=h.get("arabic", ""),
                english=h["english"],
                hadith_label=hadith_label,
                out_dir="s_frames")

            # ═══════════════ STEP 8: COMPOSE VIDEO ═══════════════
            header("STEP 8: Compose Final Video")
            final = composer.compose(
                bg_file, "s_frames", "s_voice.mp3",
                total, "output/final/Final_Story.mp4")
            log_step("G1_story_pipeline.py", "Video composed", "ok",
                     f"{os.path.getsize(final)/1024/1024:.1f} MB")

            # ═══════════════ STEP 9: THUMBNAIL ═══════════════
            header("STEP 9: Thumbnail")
            thumbnail.make(hindi, h.get("arabic", ""),
                           h["english"], hadith_label,
                           "output/final/thumbnail.jpg")

            # ═══════════════ STEP 10: DRIVE BACKUP ═══════════════
            header("STEP 10: Google Drive Backup")
            drive.upload(final, "Story")

            # ═══════════════ STEP 11: FACEBOOK UPLOAD ═══════════════
            header("STEP 11: Facebook Story Upload")
            if self.cfg.should_post_social:
                uploader.upload(final)
            else:
                log_step("G1_story_pipeline.py", "FB upload skipped", "skip")

            # ═══════════════ STEP 12: CLEANUP ═══════════════
            header("STEP 12: Cleanup")
            self.cleanup(
                ["s_raw.mp3", "s_v.mp3", "s_voice.mp3",
                 "tmp.mp4", "music_raw.mp3"],
                folder="s_frames")

            header("FACEBOOK MORNING STORY COMPLETED")
            log_file_end("G1_story_pipeline.py", "success",
                         f"Total {total:.1f}s")

        except Exception as e:
            tb = traceback.format_exc()
            log_error("G1_story_pipeline.py", str(e), tb)
            raise
