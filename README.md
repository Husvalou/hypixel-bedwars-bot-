# Hypixel Discord Bot

A Discord bot that displays Hypixel Bedwars statistics for Minecraft players.

## Features

- Display Bedwars statistics with `/bw <username>` command
- Check bot latency with `/ping` command
- Shows:
  - ⭐ Bedwars Level (Stars)
  - Wins
  - Losses
  - FKDR (Final Kill/Death Ratio)
  - Beds Broken
  - Final Kills
  - Final Deaths

## Requirements

- Python 3.6 or higher
- Discord Bot Token
- Hypixel API Key

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/hypixel-discord-bot.git
cd hypixel-discord-bot
```

2. Install required packages:
```bash
pip install discord.py requests python-dotenv
```

3. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

4. Configure your `.env` file:
- Get your Discord Bot Token from [Discord Developer Portal](https://discord.com/developers/applications)
- Get your Hypixel API Key by signing up and using `https://developer.hypixel.net` 
```env
DISCORD_TOKEN=your_discord_bot_token
HYPIXEL_API_KEY=your_hypixel_api_key
```

5. Enable required bot intents and features:
- Go to [Discord Developer Portal](https://discord.com/developers/applications)
- Select your application
- Go to "Bot" section
- Enable "Message Content Intent"
- Make sure "applications.commands" scope is enabled when inviting the bot

## Usage

1. Start the bot:
```bash
python bot.py
```

2. In Discord, use the slash command:
```
/bw username:<minecraft_username>
```
The bot will display the Bedwars statistics for the specified player in a Discord embed.

## Note

Make sure to keep your Discord Token and Hypixel API Key private. Never share them or commit them to version control.
