# Discord Poetry Bot

A simple yet elegant Discord bot that brings the beauty of poetry into your server. It can fetch classic Arabic and English poems or write a new one for you in any language using AI.

### Features

* **Arabic Poems:** Fetches a random classical Arabic poem from `aldiwan.net`.

* **English Poems:** Retrieves a random English poem from the `PoetryDB` API.

* **AI-Generated Poems:** Generates a creative poem on any topic you provide, powered by the Gemini AI.

* **Always On:** Uses a lightweight Flask web server to ensure the bot remains online.

### How to Use

The bot uses **slash commands** for all its functions. Simply type a forward slash (`/`) in a Discord channel to see the available commands.

| Command | Description                                                                  | 
 | ----- |------------------------------------------------------------------------------| 
| `/qafiyah` | Get a random Arabic poem.                                                    | 
| `/poem` | Get a random English poem.                                                   | 
| `/aipoem [topic]` | Get a creative AI poem about a specific topic (in the language of the text). | 

### 🔗 Invite the Bot

You can invite the bot to your Discord server using the following link.

**Invite Link:**
[Qafiyah: Drop some bars.!](https://discord.com/oauth2/authorize?client_id=1400298955467788399&permissions=1689659461987392&integration_type=0&scope=bot+applications.commands)

### Installation

To run this bot, you will need to set up a few things first.

#### Prerequisites

* Python 3.8 or higher

* A Discord bot token from the [Discord Developer Portal](https://discord.com/developers/applications)

* A Gemini API key from the [Google AI Studio](https://aistudio.google.com/)

#### Steps

1. **Clone the repository:**

   ```
   git clone [your-repo-url]
   cd [your-repo-folder]
   
   ```

2. **Install dependencies:**

   ```
   pip install -r requirements.txt
   
   ```

   *Note: You may need to create a `requirements.txt` file from your imports.*

3. **Create a `.env` file:**
   Create a file named `.env` in the project's root directory and add your bot tokens.

   ```
   TOKEN="YOUR_DISCORD_BOT_TOKEN"
   TOKEN2="YOUR_GEMINI_API_KEY"
   
   ```

4. **Run the bot:**

   ```
   cd [src-folder]
   python your_bot_file.py
   
   ```

   *(Replace `your_bot_file.py` with the actual name of your Python file.)*

### Credits

* **Arabic Poems:** `aldiwan.net`

* **English Poems:** `poetrydb.org`

* **AI Generation:** Google's Gemini API
