import os
import asyncio
from pathlib import Path
from lunaris_core import LunarisEngine
from rag_ingest import DocumentIngestionEngine

DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

class LunarisDiscordBot:
    """
    Self-hosted Discord bot connector for Lunaris AI.
    """
    def __init__(self, token: str | None = None):
        self.token = token or DISCORD_TOKEN
        self.agent = LunarisEngine()
        self.ingest_engine = DocumentIngestionEngine()
        self.docs_dir = Path("./documents")
        self.docs_dir.mkdir(parents=True, exist_ok=True)

    def run(self):
        if not self.token:
            print("[Discord Bot] DISCORD_BOT_TOKEN not found in environment variables.")
            print("[Discord Bot] Set DISCORD_BOT_TOKEN in .env to activate the Discord bot.")
            return

        try:
            import discord
            from discord.ext import commands
        except ImportError:
            print("[Discord Bot] 'discord.py' not installed. Install with: pip install discord.py")
            return

        intents = discord.Intents.default()
        intents.message_content = True
        bot = commands.Bot(command_prefix="!", intents=intents)

        @bot.event
        async def on_ready():
            print(f"🌕 Lunaris Discord Bot connected as {bot.user}")

        @bot.command(name="ask")
        async def ask(ctx, *, question: str):
            async with ctx.typing():
                res = self.agent.run_react_agent(user_query=question)
                # Split if response exceeds Discord 2000 char limit
                response = res["response"]
                for i in range(0, len(response), 1900):
                    await ctx.reply(response[i:i+1900])

        @bot.command(name="docs")
        async def docs(ctx):
            docs_list = self.ingest_engine.list_indexed_documents()
            if not docs_list:
                await ctx.reply("📚 Local Knowledge Base is currently empty.")
                return
            lines = ["📚 **Indexed Documents in Lunaris AI:**"]
            for d in docs_list:
                lines.append(f"• `{d['title']}` ({d['file_type']}) - {d['chunk_count']} chunks")
            await ctx.reply("\n".join(lines))

        @bot.event
        async def on_message(message):
            if message.author == bot.user:
                return

            # Check if document attached
            if message.attachments:
                for attachment in message.attachments:
                    file_path = self.docs_dir / attachment.filename
                    await attachment.save(str(file_path))
                    await message.reply(f"📥 Ingesting `{attachment.filename}` into Lunaris vector store...")
                    res = self.ingest_engine.ingest_file(str(file_path), title=file_path.stem, force_reindex=True)
                    if res.get("status") == "success":
                        await message.reply(f"✅ Successfully indexed `{attachment.filename}` ({res.get('chunks_indexed')} chunks)!")
                    else:
                        await message.reply(f"⚠️ {res.get('message', 'Failed to index.')}")

            await bot.process_commands(message)

        bot.run(self.token)

if __name__ == "__main__":
    bot = LunarisDiscordBot()
    bot.run()
