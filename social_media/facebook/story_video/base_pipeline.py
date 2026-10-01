"""Facebook Story — main orchestrator."""
import os
import traceback
from mutagen.mp3 import MP3

from base_pipeline import BasePipeline
from logger import log_file_start, log_file_end, log_step, log_error
from ai_provider import AIProvider
from translator import Translator
from tts import TTS
from music import Music
from background import Background
from logo import Logo
from frames import Frames
from subtitles import write_ass
from composer import Composer
from hadith import Hadith
from drive import Drive
from upload_story import StoryUploader


class StoryPipeline(BasePipeline):

    def run(self):
        from telegram import send_tg, header

        log_file_start("story_pipeline.py", "Orchestrate full pipeline")
        header("FACEBOOK MORNING STORY")

        try:
            ai = AIProvider(self)
            translator = Translator(self, ai)
            tts = TTS(self)
            music = Music(self)
            bg = Background(self)
            logo = Logo()
            frames = Frames()
            composer = Composer(self)
            hadith = Hadith(self)
            drive = Drive(self)
            uploader = StoryUploader(self)

            header("STEP 1: Fetch Hadith")
            h = hadith.fetch()
            log_step("story_pipeline.py", f"Hadith fetched", "ok",
                     f"{h['collection']} #{h['number']}")

            header("STEP 2: Hindi Translation")
            hindi = translator.to_hindi(h["english"])
            log_step("story_pipeline.py", "Translation done", "ok")

            header("STEP 3: Text-to-Speech")
            tts.generate(f"हदीस शरीफ। {hindi}", "s_raw.mp3")
            self.run_cmd(
                'ffmpeg -y -i s_raw.mp3 -af '
                '"atempo=0.88,loudnorm=I=-16:TP=-1.5:LRA=11,volume=1.35" s_v.mp3')
            voice_dur = MP3("s_v.mp3").info.length
            log_step("story_pipeline.py", f"Voice ready", "ok",
                     f"{voice_dur:.1f}s")

            header("STEP 4: Background Music")
            music.get("music_soft.mp3")
            fade = max(voice_dur - 3.0, 1.0)
            self.run_cmd(
                f'ffmpeg -y -i s_v.mp3 -i music_soft.mp3 -filter_complex '
                f'"[1:a]volume=0.20,afade=t=in:st=0:d=2,'
                f'afade=t=out:st={fade:.2f}:d=3[bg];'
                f'[0:a][bg]amix=inputs=2:duration=first:dropout_transition=2[aout]" '
                f'-map "[aout]" -c:a libmp3lame -b:a 192k s_voice.mp3')
            log_step("story_pipeline.py", "Voice + music mixed", "ok")

            header("STEP 5: Background Video")
            bg_file = bg.get(voice_dur + 3.5)

            header("STEP 6: Logo")
            has_logo = logo.make("avatar.png")

            header("STEP 7: Subtitles")
            write_ass(h.get("arabic", ""), hindi, h["english"],
                      voice_dur, "s_subs.ass")

            header("STEP 8: Overlay Frames")
            total = frames.generate(voice_dur, has_logo, "s_frames")

            header("STEP 9: Compose Final Video")
            final = composer.compose(
                bg_file, "s_frames", "s_voice.mp3", "s_subs.ass",
                total, "Final_Story.mp4")
            log_step("story_pipeline.py", "Video composed", "ok",
                     f"{total:.1f}s | {os.path.getsize(final)/1024/1024:.1f} MB")

            header("STEP 10: Google Drive Backup")
            drive.upload(final, "Story")

            header("STEP 11: Facebook Story Upload")
            if self.cfg.should_post_social:
                uploader.upload(final)
            else:
                log_step("story_pipeline.py", "FB upload skipped", "skip",
                         "Manual run")

            header("STEP 12: Cleanup")
            self.cleanup(
                ["s_raw.mp3", "s_v.mp3", "s_voice.mp3", "s_subs.ass",
                 "tmp.mp4", "music_raw.mp3"],
                folder="s_frames")

            header("FACEBOOK MORNING STORY COMPLETED")
            log_file_end("story_pipeline.py", "success", f"Total {total:.1f}s")

        except Exception as e:
            tb = traceback.format_exc()
            log_error("story_pipeline.py", str(e), tb)
            raise
