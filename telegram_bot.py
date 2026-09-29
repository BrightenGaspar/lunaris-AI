import os
import asyncio
from pathlib import Path
from lunaris_core import LunarisEngine
from rag_ingest import DocumentIngestionEngine
from voice_engine import LunarisVoiceEngine

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

class LunarisTelegramBot:
    """
    Self-hosted Telegram bot connector for Lunaris AI.
    Allows interacting with the sovereign ReAct agent, indexing files, and voice notes.
    """
    def __init__(self, token: str | None = None):
        self.token = token or TELEGRAM_TOKEN
        self.agent = LunarisEngine()
        self.ingest_engine = DocumentIngestionEngine()
        self.voice_engine = LunarisVoiceEngine()
        self.docs_dir = Path("./documents")
        self.docs_dir.mkdir(parents=True, exist_ok=True)

    def run(self):
        if not self.token:
            print("[Telegram Bot] TELEGRAM_BOT_TOKEN not found in environment variables.")
            print("[Telegram Bot] Set TELEGRAM_BOT_TOKEN in .env to activate the Telegram bot.")
            return

        try:
            from telegram import Update
            from telegram.ext import (
                ApplicationBuilder,
                CommandHandler,
                MessageHandler,
                ContextTypes,
                filters
            )
        except ImportError:
            print("[Telegram Bot] 'python-telegram-bot' not installed. Install with: pip install python-telegram-bot")
            return

        async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
            welcome_msg = (
                "🌕 **Welcome to Lunaris AI Sovereign Bot**\n\n"
                "I am your self-hosted private AI assistant with autonomous ReAct reasoning.\n\n"
                "• Send any text query to reason and answer.\n"
                "• Send a **voice message** for voice-in / voice-out interaction.\n"
                "• Send a **file/document** (PDF, CSV, DOCX, Code) to index into the knowledge base.\n\n"
                "**Commands:**\n"
                "/docs - List indexed documents\n"
                "/clear - Start a fresh conversation session\n"
                "/help - View assistance"
            )
            await update.message.reply_text(welcome_msg, parse_mode="Markdown")

        async def docs_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
            docs = self.ingest_engine.list_indexed_documents()
            if not docs:
                await update.message.reply_text("📚 Local Knowledge Base is currently empty.")
                return
            lines = ["📚 **Indexed Documents in Lunaris AI:**"]
            for d in docs:
                lines.append(f"• `{d['title']}` ({d['file_type']}) - {d['chunk_count']} chunks")
            await update.message.reply_text("\n".join(lines), parse_mode="Markdown")

        async def clear_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
            context.user_data["session_id"] = None
            await update.message.reply_text("🔄 Conversation session reset.")

        async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
            user_text = update.message.text
            session_id = context.user_data.get("session_id")
            
            # Send typing status
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
            
            # Run ReAct reasoning loop
            result = self.agent.run_react_agent(user_query=user_text, session_id=session_id)
            context.user_data["session_id"] = result["session_id"]
            
            # Reply with response
            await update.message.reply_text(result["response"])

        async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
            voice_file = await update.message.voice.get_file()
            local_audio_path = f"voice_temp_{update.effective_user.id}.ogg"
            await voice_file.download_to_drive(local_audio_path)

            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="record_voice")

            # 1. Transcribe voice
            transcribed_text = self.voice_engine.transcribe_audio(local_audio_path)
            if not transcribed_text or "[" in transcribed_text:
                await update.message.reply_text(f"🎤 Transcribed: '{transcribed_text}'")

            # 2. Run ReAct Agent
            session_id = context.user_data.get("session_id")
            result = self.agent.run_react_agent(user_query=transcribed_text, session_id=session_id)
            context.user_data["session_id"] = result["session_id"]

            # 3. Synthesize Voice Output
            speech_wav = self.voice_engine.synthesize_speech(result["response"])

            # 4. Reply with text and audio voice note
            await update.message.reply_text(f"🗣️ *Transcription:* {transcribed_text}\n\n{result['response']}", parse_mode="Markdown")
            if speech_wav and os.path.exists(speech_wav):
                with open(speech_wav, "rb") as audio:
                    await update.message.reply_voice(voice=audio)
                try:
                    os.remove(speech_wav)
                except Exception:
                    pass

            if os.path.exists(local_audio_path):
                try:
                    os.remove(local_audio_path)
                except Exception:
                    pass

        async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
            doc = update.message.document
            file_path = self.docs_dir / doc.file_name
            telegram_file = await doc.get_file()
            await telegram_file.download_to_drive(str(file_path))

            await update.message.reply_text(f"📥 Ingesting `{doc.file_name}` into sovereign vector store...", parse_mode="Markdown")
            res = self.ingest_engine.ingest_file(str(file_path), title=file_path.stem, force_reindex=True)
            
            if res.get("status") == "success":
                await update.message.reply_text(f"✅ Successfully indexed `{doc.file_name}` ({res.get('chunks_indexed')} chunks)!", parse_mode="Markdown")
            else:
                await update.message.reply_text(f"⚠️ {res.get('message', 'Failed to index file.')}")

        print("🌕 Starting Lunaris Telegram Bot polling...")
        app = ApplicationBuilder().token(self.token).build()
        app.add_handler(CommandHandler("start", start_cmd))
        app.add_handler(CommandHandler("docs", docs_cmd))
        app.add_handler(CommandHandler("clear", clear_cmd))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
        app.add_handler(MessageHandler(filters.VOICE, handle_voice))
        app.add_handler(MessageHandler(filters.Document.ALL, handle_document))

        app.run_polling()

if __name__ == "__main__":
    bot = LunarisTelegramBot()
    bot.run()
