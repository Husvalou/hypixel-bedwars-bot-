import os
import discord
from discord import app_commands
from discord.ext import commands
import requests
from dotenv import load_dotenv
import datetime
from PIL import Image, ImageDraw, ImageFont
import io

# Load environment variables
load_dotenv()

# Bot configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
HYPIXEL_API_KEY = os.getenv('HYPIXEL_API_KEY')

# Create bot with slash commands
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} is connected and ready!')
    await bot.tree.sync()
    print("Commands synced")

@bot.tree.command(name="bw", description="Display Bedwars statistics for a player")
@app_commands.describe(
    username="Minecraft username",
)
async def bedwars_stats(interaction: discord.Interaction, username: str):
    await interaction.response.defer()
    
    try:
        # Get player UUID via Mojang API
        mojang_response = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{username}')
        if mojang_response.status_code != 200:
            await interaction.followup.send("Player not found!")
            return
        
        uuid = mojang_response.json()['id']
        
        # Get stats via Hypixel API for embed style
        hypixel_response = requests.get(f'https://api.hypixel.net/player?key={HYPIXEL_API_KEY}&uuid={uuid}')
        if hypixel_response.status_code != 200:
            await interaction.followup.send("Error while retrieving Hypixel data!")
            return
        
        player_data = hypixel_response.json()
        
        if not player_data['success']:
            await interaction.followup.send("Error while retrieving data!")
            return
            
        # Extract Bedwars statistics
        bedwars_stats = player_data['player']['stats']['Bedwars']
        
        # Get Bedwars level directly from API
        bedwars_level = player_data['player'].get('achievements', {}).get('bedwars_level', 0)
        
        # Create image with stats
        def create_stats_image(stats_data, username):
            # Open the template image
            img = Image.open("embed.jpg")
            draw = ImageDraw.Draw(img)
            
            # Try to use Minecraft font, fallback to default if not available
            try:
                font = ImageFont.truetype("fonts/Minecraft.ttf", 24)
                title_font = ImageFont.truetype("fonts/Minecraft.ttf", 28)
            except:
                font = ImageFont.load_default()
                title_font = font
            
            # Colors
            GREEN = (0, 255, 0)
            RED = (255, 0, 0)
            YELLOW = (255, 255, 0)
            WHITE = (255, 255, 255)
            SHADOW = (45, 45, 45)  # Dark grey for shadow
            
            # Prestige colors based on level
            def get_prestige_color(level):
                if level < 100:  # Stone [50★]
                    return (170, 170, 170)  # Grey
                elif level < 200:  # Iron [100★]
                    return (255, 255, 255)  # White
                elif level < 300:  # Gold [200★]
                    return (255, 170, 0)  # Gold
                elif level < 400:  # Diamond [300★]
                    return (85, 255, 255)  # Aqua
                elif level < 500:  # Emerald [400★]
                    return (0, 255, 0)  # Green
                elif level < 600:  # Sapphire [500★]
                    return (85, 85, 255)  # Blue
                elif level < 700:  # Ruby [600★]
                    return (255, 85, 85)  # Red
                elif level < 800:  # Crystal [700★]
                    return (255, 85, 255)  # Pink
                elif level < 900:  # Opal [800★]
                    return (85, 85, 255)  # Blue
                elif level < 1000:  # Amethyst [900★]
                    return (170, 0, 170)  # Purple
                elif level < 1100:  # Rainbow [1000★]
                    return (255, 85, 255)  # Light Purple
                elif level < 1200:  # Iron Prime [1100★]
                    return (255, 255, 255)  # White
                elif level < 1300:  # Gold Prime [1200★]
                    return (255, 170, 0)  # Gold
                elif level < 1400:  # Diamond Prime [1300★]
                    return (85, 255, 255)  # Aqua
                elif level < 1500:  # Emerald Prime [1400★]
                    return (0, 255, 0)  # Green
                elif level < 1600:  # Sapphire Prime [1500★]
                    return (85, 85, 255)  # Blue
                elif level < 1700:  # Ruby Prime [1600★]
                    return (255, 85, 85)  # Red
                elif level < 1800:  # Crystal Prime [1700★]
                    return (255, 85, 255)  # Pink
                elif level < 1900:  # Opal Prime [1800★]
                    return (85, 85, 255)  # Blue
                elif level < 2000:  # Amethyst Prime [1900★]
                    return (170, 0, 170)  # Purple
                elif level < 2100:  # Mirror [2000★]
                    return (170, 170, 170)  # Grey
                elif level < 2200:  # Light [2100★]
                    return (255, 255, 85)  # Yellow
                elif level < 2300:  # Dawn [2200★]
                    return (255, 170, 0)  # Orange
                elif level < 2400:  # Dusk [2300★]
                    return (170, 0, 170)  # Purple
                elif level < 2500:  # Air [2400★]
                    return (170, 170, 170)  # Grey
                elif level < 2600:  # Wind [2500★]
                    return (85, 255, 85)  # Light Green
                elif level < 2700:  # Nebula [2600★]
                    return (170, 0, 0)  # Dark Red
                elif level < 2800:  # Thunder [2700★]
                    return (255, 255, 85)  # Yellow
                elif level < 2900:  # Earth [2800★]
                    return (170, 85, 0)  # Brown
                elif level < 3000:  # Water [2900★]
                    return (85, 85, 255)  # Blue
                else:  # Fire [3000★]
                    return (255, 85, 85)  # Red
            
            def draw_text_with_shadow(x, y, text, color, font, center=False):
                # Get text width for centering
                bbox = font.getbbox(str(text))
                text_width = bbox[2] - bbox[0]
                
                if center:
                    x = (img.width - text_width) // 2
                
                # Draw shadow
                draw.text((x + 2, y + 2), str(text), SHADOW, font=font)
                # Draw main text
                draw.text((x, y), str(text), color, font=font)
            
            # Calculate stats
            wins = stats_data.get('wins_bedwars', 0)
            losses = stats_data.get('losses_bedwars', 0)
            final_kills = stats_data.get('final_kills_bedwars', 0)
            final_deaths = stats_data.get('final_deaths_bedwars', 0)
            beds_broken = stats_data.get('beds_broken_bedwars', 0)
            beds_lost = stats_data.get('beds_lost_bedwars', 0)
            
            # Calculate ratios
            fkdr = round(final_kills / max(final_deaths, 1), 2)
            wlr = round(wins / max(losses, 1), 2)
            bblr = round(beds_broken / max(beds_lost, 1), 2)
            
            # Get prestige color based on level
            prestige_color = get_prestige_color(bedwars_level)
            
            # Draw centered header with prestige color
            level_text = f"[{bedwars_level}★] {username}"
            draw_text_with_shadow(0, 20, level_text, prestige_color, title_font, center=True)
            
            # Adjust base positions
            y_start = 80
            y_spacing = 40
            x_left = 50
            x_mid = img.width//2 - 50
            x_right = img.width - 150
            
            # Column 1 - Wins/Kills/Beds
            draw_text_with_shadow(x_left, y_start, "Wins", GREEN, font)
            draw_text_with_shadow(x_left, y_start + y_spacing, str(wins), GREEN, font)
            
            draw_text_with_shadow(x_left, y_start + y_spacing*3, "Final Kills", GREEN, font)
            draw_text_with_shadow(x_left, y_start + y_spacing*4, str(final_kills), GREEN, font)
            
            draw_text_with_shadow(x_left, y_start + y_spacing*6, "Beds Broken", GREEN, font)
            draw_text_with_shadow(x_left, y_start + y_spacing*7, str(beds_broken), GREEN, font)
            
            # Column 2 - Losses/Deaths/Beds Lost
            draw_text_with_shadow(x_mid, y_start, "Losses", RED, font)
            draw_text_with_shadow(x_mid, y_start + y_spacing, str(losses), RED, font)
            
            draw_text_with_shadow(x_mid, y_start + y_spacing*3, "Final Deaths", RED, font)
            draw_text_with_shadow(x_mid, y_start + y_spacing*4, str(final_deaths), RED, font)
            
            draw_text_with_shadow(x_mid, y_start + y_spacing*6, "Beds Lost", RED, font)
            draw_text_with_shadow(x_mid, y_start + y_spacing*7, str(beds_lost), RED, font)
            
            # Column 3 - Ratios
            draw_text_with_shadow(x_right, y_start, "WLR", YELLOW, font)
            draw_text_with_shadow(x_right, y_start + y_spacing, str(wlr), YELLOW, font)
            
            draw_text_with_shadow(x_right, y_start + y_spacing*3, "FKDR", YELLOW, font)
            draw_text_with_shadow(x_right, y_start + y_spacing*4, str(fkdr), YELLOW, font)
            
            draw_text_with_shadow(x_right, y_start + y_spacing*6, "BBLR", YELLOW, font)
            draw_text_with_shadow(x_right, y_start + y_spacing*7, str(bblr), YELLOW, font)
            
            # Save to bytes
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            return discord.File(img_byte_arr, 'stats.png')
        
        # Create Discord embed
        embed = discord.Embed(
            title=f" {username}'s Bedwars Statistics ",
            color=discord.Color.dark_grey()
        )

        # Add Overall Level field
        embed.add_field(
            name="Overall Bedwars Level",
            value=f" {bedwars_level} ",
            inline=False
        )

        # First row: Final Kills, Beds Broken, Wins
        embed.add_field(
            name="Final Kills",
            value=bedwars_stats.get('final_kills_bedwars', 0),
            inline=True
        )
        embed.add_field(
            name="Beds Broken",
            value=bedwars_stats.get('beds_broken_bedwars', 0),
            inline=True
        )
        embed.add_field(
            name="Wins",
            value=bedwars_stats.get('wins_bedwars', 0),
            inline=True
        )

        # Second row: Final Deaths, Beds Lost, Losses
        embed.add_field(
            name="Final Deaths",
            value=bedwars_stats.get('final_deaths_bedwars', 0),
            inline=True
        )
        embed.add_field(
            name="Beds Lost",
            value=bedwars_stats.get('beds_lost_bedwars', 0),
            inline=True
        )
        embed.add_field(
            name="Losses",
            value=bedwars_stats.get('losses_bedwars', 0),
            inline=True
        )

        # Third row: Ratios (FKDR, BBLR, WLR)
        fkdr = round(bedwars_stats.get('final_kills_bedwars', 0) / max(bedwars_stats.get('final_deaths_bedwars', 1), 1), 2)
        bblr = round(bedwars_stats.get('beds_broken_bedwars', 0) / max(bedwars_stats.get('beds_lost_bedwars', 1), 1), 2)
        wlr = round(bedwars_stats.get('wins_bedwars', 0) / max(bedwars_stats.get('losses_bedwars', 1), 1), 2)

        embed.add_field(
            name="FKDR",
            value=fkdr,
            inline=True
        )
        embed.add_field(
            name="BBLR",
            value=bblr,
            inline=True
        )
        embed.add_field(
            name="WLR",
            value=wlr,
            inline=True
        )

        # Add timestamp and footer
        embed.set_footer(text=f"Today at {datetime.datetime.now().strftime('%H:%M')}")
        
        # Create the stats image
        stats_image = create_stats_image(bedwars_stats, username)
        
        # Add the embed image
        embed.set_image(url="attachment://stats.png")
        
        # Send the embed with the image file
        await interaction.followup.send(embed=embed, file=stats_image)
        
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {str(e)}")

@bot.tree.command(name="ping", description="Display bot's latency")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)  # Convert to milliseconds
    await interaction.response.send_message(f"Bot latency is {latency}ms")

# Start the bot
bot.run(DISCORD_TOKEN)
