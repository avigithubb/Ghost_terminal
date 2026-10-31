
import io
import os
import time
from queue import Queue
from threading import Thread
import re


import pygame
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs


class VoiceEngine:
    def __init__(self):
        load_dotenv()

        api_key = os.getenv("ELEVENLABS_API_KEY")
        self.voice_id = os.getenv("ELEVENLABS_VOICE_ID")

        if not api_key or not self.voice_id:
            raise ValueError(
                "ElevenLabs API key or Voice ID is missing from .env"
            )

        self.client = ElevenLabs(api_key=api_key)

        self.model_id = "eleven_flash_v2_5"
        self.enabled = True
        self.audio_queue = Queue()

        pygame.mixer.init()

        self.worker = Thread(
            target=self._process_queue,
            daemon=True
        )
        self.worker.start()

    def enqueue(self, text):
        if self.enabled and text.strip():
            self.audio_queue.put(text.strip())

    def _process_queue(self):
        while True:
            text = self.audio_queue.get()

            try:
                speech_text = self.prepare_for_tts(text)
                if not speech_text:
                    continue

                audio_stream = self.client.text_to_speech.stream(
                    text=speech_text,
                    voice_id=self.voice_id,
                    model_id=self.model_id,
                    output_format="mp3_22050_32"
                )
               

                # Collect the generated audio chunks.
                audio_data = b"".join(audio_stream)

                if not audio_data:
                    continue

                # Play the generated MP3 using Pygame.
                pygame.mixer.music.load(
                    io.BytesIO(audio_data),
                    "mp3"
                )

                pygame.mixer.music.play()

                # Wait until playback finishes.
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)

            except Exception as error:
                print(f"\n[ELEVENLABS ERROR] {error}")

            finally:
                self.audio_queue.task_done()

    def prepare_for_tts(self, text):
        # Convert our custom pause markers into ElevenLabs SSML.
        def replace_pause(match):
            duration = float(match.group(1))

            # Keep pauses within ElevenLabs' supported range.
            duration = max(0.1, min(duration, 3.0))

            return f'<break time="{duration}s" />'

        text = re.sub(
            r"\[PAUSE:(\d+(?:\.\d+)?)\]",
            replace_pause,
            text,
            flags=re.IGNORECASE
        )

        # Remove any remaining parenthetical stage directions.
        text = re.sub(r"\([^)]*\)", "", text)

        return text.strip()

    def wait_until_done(self):
        self.audio_queue.join()

    def toggle(self):
        self.enabled = not self.enabled
        return self.enabled

    def close(self):
        self.audio_queue.join()
        self.audio_queue.put(None)
        self.worker.join()
        pygame.mixer.quit()
