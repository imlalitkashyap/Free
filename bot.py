from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import os

TOKEN = os.getenv("TOKEN")  # Render env variable

def convert_txt_links_to_html(text: str) -> str:
    items = []
    for line in text.splitlines():
        line = line.strip()
        if not line or "http" not in line:
            continue
        try:
            title, link = line.split(":", 1)
            items.append(f'<p><a href="{link.strip()}" target="_blank">{title.strip()}</a></p>')
        except ValueError:
            continue

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <title>LalitxStark - HTML</title>
      <style>
        body {{
          font-family: Arial, sans-serif;
          background-color: #f4f4f4;
          text-align: center;
          padding: 20px;
        }}
        h1 {{
          color: #222;
        }}
        .btn {{
          background: #007bff;
          padding: 10px 20px;
          color: white;
          border-radius: 10px;
          text-decoration: none;
          display: inline-block;
          margin: 10px;
        }}
        .section {{
          margin-top: 30px;
        }}
        a {{
          color: #0066cc;
          text-decoration: none;
        }}
        a:hover {{
          text-decoration: underline;
        }}
      </style>
    </head>
    <body>
      <h1>📘 Maths Spl - 36 (Pre + Mains)</h1>
      <div class="section">
        <a class="btn" href="#videos">🎥 Videos</a>
      </div>
      <div class="section" id="videos">
        <h2>🎬 Video Links</h2>
        {"".join(items) if items else "<p>No videos found</p>"}
      </div>
    </body>
    </html>
    """
    return html

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    if document.file_name.endswith(".txt"):
        file = await context.bot.get_file(document.file_id)
        file_path = await file.download_to_drive()
        with open(file_path, "r", encoding='utf-8') as f:
            content = f.read()

        html_content = convert_txt_links_to_html(content)
        html_file = "converted.html"
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        await update.message.reply_document(document=open(html_file, "rb"))
        os.remove(html_file)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.Document.ALL, handle_file))

if __name__ == "__main__":
    print("Bot is running...")
    app.run_polling()
