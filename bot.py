#!/usr/bin/env python
# -*- coding: utf-8 -*-


class TelMan:
    """Python-Telegram-Bot function manager."""

    def __init__(self):
        self.telegram_token = "6231502284:AAEgIa3GEXYUyg6UZ_YRAMFx4jgX2pX6bFk"


        import openai

        self.openai = openai
        self.openai.api_key = "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"


        from telegram.ext import Updater

        self.updater = Updater(self.telegram_token, use_context=True)

    def set_update(self, update):
        self.update = update

    def reply(self, msg):
        reply = self.update.message.reply_text
        reply(msg)

    def get_user(self):
        self.user = self.update.message.from_user.username

        return self.user


class MsgMan(TelMan):
    """Messages manager."""

    def process_text(self, text):
        completion = self.openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": text}]
        )
        response = completion['choices'][0]['message']["content"]
        print("RESPONSE FROM CHATGPT: " + response)

        self.reply(response)

    def process_audio(self, audio):
        text = self.openai.Audio.transcribe("whisper-1", audio)["text"]
        print("TRANSCRIPTION FROM WHISPER: " + text)

        self.process_text(text)


class Bot(MsgMan):
    """Bot commands manager."""

    def handle_text(self, update, context):
        self.set_update(update)
        text = update.message.text
        print(f"TEXT REQUEST FROM [{self.get_user()}]: " + text)

        self.process_text(text)

    def handle_audio(self, update, context):
        self.set_update(update)
        print("VOICE REQUEST FROM: " + self.get_user())

        audio_id = update.message.voice.file_id
        audio_info = self.updater.bot.get_file(audio_id)
        audio_info.download("audio.ogg")


        from pydub import AudioSegment

        with open("audio.ogg", "rb") as audio_oog:
            sound = AudioSegment.from_ogg(audio_oog)
            sound.export("audio.mp3", format="mp3")

        with open("audio.mp3", "rb") as audio:
            self.process_audio(audio)

        self.process_audio(audio_oog)


if __name__ == "__main__":
    bot = Bot()
    dp = bot.updater.dispatcher


    from telegram.ext import MessageHandler, Filters

    dp.add_handler(MessageHandler(Filters.text, bot.handle_text))
    dp.add_handler(MessageHandler(Filters.all, bot.handle_audio))

    bot.updater.start_polling()
    bot.updater.idle()
