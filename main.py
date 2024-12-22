# IMPORTS
import discord
from discord_secrets import secrets
import os
import random
import time

# VARIABLES
# Token, Admin Id, and Client
TOKEN = secrets.get("TOKEN")
ADMIN_ID = secrets.get("ADMIN_ID")
bot_intents = discord.Intents.default()
bot_intents.message_content = True
client = discord.Client(intents = bot_intents)
# Directories
DIRECTORY_USER_DATA = "User Data"
DIRECTORY_BOT_DATA = "Bot Data\\"
DIRECTORY_ADMIN_DATA = "Admin Data\\"
DIRECTORY_UPDATE_LOGS = "Update Logs\\"
DIRECTORY_DELETION_REQUESTS = "Deletion Requests\\"
DIRECTORY_PERSONAL_MESSAGES = "Personal Messages\\"
# Tip List
tip_list = (
    "Tips appear at the bottom of many messages.",
    "Fences prevent robberies."
)
# Cooldown Variables
cooldown_amount = 10.0
last_executed = time.time() - cooldown_amount

# FUNCTIONS
def assert_cooldown(): # From Eric Jin on stackoverflow.com
    global last_executed
    if last_executed + cooldown_amount < time.time():
        last_executed = time.time()
        return True
    else:
        return False

def format_num(num):
    return f"{num:,}".replace(",", " ")

def generateMissingParamsEmbed(missing_params,aditional_description_content,
color):
    title_content = "Missing Parameter(s):"
    for param in missing_params:
        title_content += " <" + param + ">"
    return discord.Embed(
        title = title_content,
        description = (
            "Please add the missing parameters and try again." +
            aditional_description_content
        ), color = color
    )

# MAIN FUNCTION
def main():
    @client.event
    async def on_ready():
        print(client.user.name + " is online.")

    @client.event
    async def on_message(message):

        if(message.content.startswith("/farm") and
        message.author != client.user):
            
            command = message.content.replace("/farm ", "")

            # Gathering and/or creating data about the user
            author_id = str(message.author.id)
            user_file_name = DIRECTORY_USER_DATA + "\\id" + author_id + ".txt"
            if not os.path.isfile(user_file_name):
                with open(user_file_name, "w") as file:
                    file.write(
                        "(Use \"/farm name\" to change name)\n0\ngreen" +
                        "\nfalse\nfalse\nfalse\n500\n1\n2\n1\n1\n5\n6\n2" +
                        "\n30\n1\n3\n1\n0\n0\n0\n0\n0\n0\n0\n50\nNone"
                    )
            with open(user_file_name, "r") as file:
                user_accnt_name = file.readline().strip()
                user_cmd_count = int(file.readline().strip())
                match file.readline():
                    case "red":
                        user_color = 0xff0000
                    case "orange":
                        user_color = 0xff8000
                    case "yellow":
                        user_color = 0xffff00
                    case "green":
                        user_color = 0x00ff00
                    case "blue":
                        user_color = 0x0000ff
                    case "purple":
                        user_color = 0x800080
                    case "white":
                        user_color = 0xffffff
                    case _:
                        user_color = 0x000000
                user_read_announcement = file.readline().strip()
                user_claimed_daily = file.readline().strip()
                user_seen_report = file.readline().strip()
                user_money = int(file.readline().strip())
                user_rock = int(file.readline().strip())
                user_wood = int(file.readline().strip())
                user_axes = int(file.readline().strip())
                user_pickaxes = int(file.readline().strip())
                user_seeds = int(file.readline().strip())
                user_peanuts = int(file.readline().strip())
                user_wheat = int(file.readline().strip())
                user_potatoes = int(file.readline().strip())
                user_corn = int(file.readline().strip())
                user_melons = int(file.readline().strip())
                user_fields_empty = int(file.readline().strip())
                user_fields_peanut = int(file.readline().strip())
                user_fields_wheat = int(file.readline().strip())
                user_fields_corn = int(file.readline().strip())
                user_fields_potato = int(file.readline().strip())
                user_fields_melon = int(file.readline().strip())
                user_mines = int(file.readline().strip())
                user_printers = int(file.readline().strip())
                user_fence_lvl = int(file.readline().strip())
                user_report = ""
                for line in file:
                    user_report += line
                user_report = user_report.strip()
            user_cmd_count += 1

            # Checking if the user should be warned of unread announcement
            if user_read_announcement == "no" and command != "announcement":
                embed = discord.Embed(
                    title = "Unread Announcement!!",
                    description = (
                        "You have an unread annoucement." + 
                        "\nUse \"/farm announcement\" to read it"
                    ), color = user_color
                )
                await message.channel.send(embed = embed)

            # Checking if the user has a personal message
            entry_name = (
                DIRECTORY_PERSONAL_MESSAGES + "id" + author_id + ".txt"
            )
            if os.path.isfile(entry_name):
                with open(entry_name) as file:
                    content = file.read()
                os.remove(entry_name)
                embed = discord.Embed(
                    title = "Personal Message From the Admin",
                    description = content, color = user_color
                )
                await message.author.send(embed = embed)
            
            # Checking cooldown for "farm" and "chop" commands
            if(not assert_cooldown() and
            (command == "mine" or command == "chop")):
                time_remainging = (
                    str(round(last_executed +
                    cooldown_amount - time.time(), 2))
                )
                embed = discord.Embed(
                    title = "Please Wait: Cooldown",
                    description = (
                        "Time remainging: " + time_remainging + " seconds."
                    ), color = user_color
                )
                await message.channel.send(embed = embed)
                return

            # COMMANDS
            # --FARMING AND RELATED--
            # INVENTORY
            if command.startswith("inv"):
                net_worth = (
                    user_money + user_melons * 30 + user_corn * 15 +
                    user_potatoes * 10 + user_wheat * 5 + user_peanuts +
                    user_rock * 50 + user_wood * 25
                )
                content_money = (
                    "Money: " + format_num(user_money) + ":coin:" +
                    "\nNet Worth: " + format_num(net_worth) + ":coin:"
                )
                content_crops = (
                    "\n:red_envelope: Seeds: " + format_num(user_seeds) +
                    "\n:peanuts: Peanuts: " + format_num(user_peanuts) +
                    "\n:ear_of_rice: Wheat: " + format_num(user_wheat) +
                    "\n:potato: Potatoes: " + format_num(user_potatoes) +
                    "\n:corn: Corn: " + format_num(user_corn) +
                    ":watermelon: Melons: " + format_num(user_melons)
                )
                content_fields = (
                    "Empty: " + format_num(user_fields_empty) +
                    "\nPeanuts: " + format_num(user_fields_peanut) +
                    "\nWheat: " + format_num(user_fields_wheat) +
                    "\nPotato: " + format_num(user_fields_potato) +
                    "\nCorn: " + format_num(user_fields_corn) +
                    "\nMelon: " + format_num(user_fields_melon)
                )
                content_other = (
                    "Materials" +
                    "\n:rock: Rock: " + format_num(user_rock) +
                    "\n:wood: Wood: " + format_num(user_wood) +
                    "\nTools" +
                    "\n:axe: Axes: " + format_num(user_axes) +
                    "\n:pick: Pickaxes: " + format_num(user_pickaxes) +
                    "\nMachines" +
                    "\nAutomatic Mines: " + format_num(user_mines) +
                    "\nMoney Printers: " + format_num(user_printers) +
                    "\nFence Level: " + format_num(user_fence_lvl)
                )
                embed = discord.Embed(
                    title = user_accnt_name + "'s Inventory",
                    color = user_color
                )
                embed.set_thumbnail(url = message.author.avatar)
                embed.add_field(
                    name = "Money and Net Worth", value = content_money,
                    inline = False
                )
                embed.add_field(
                    name = "Crops and Seeds", value = content_crops,
                    inline = True
                )
                embed.add_field(
                    name = "Fields", value = content_fields, inline = True
                )
                embed.add_field(
                    name = "Other", value = content_other, inline = True
                )
                embed.set_footer(text = random.choice(tip_list))
                await message.channel.send(embed = embed)

            # MINE
            elif command == "mine":
                if user_money >= 200 and user_pickaxes > 0:
                    user_money -= 200
                    amount_mined = random.randint(0, 16)
                    user_rock += amount_mined
                    embed = discord.Embed(
                        title = user_accnt_name + " Went Mining!",
                        description = (
                            "They spent 200 :coin: and mined " +
                            str(amount_mined) + " rock."
                        ), color = user_color
                    )
                elif user_pickaxes == 0:
                    embed = discord.Embed(
                        title = "Tool Needed",
                        description = (
                            "You need a pickaxe to go mining." +
                            "\nUse \"/farm buy pickaxe\" to buy one."
                        ), color = user_color
                    )
                else:
                    embed = discord.Embed(
                        title = "Money Needed",
                        description = (
                            "You need 200 :coin: to go mining." +
                            "\nYou only have " + format_num(user_money) +
                            " :coin:."
                        ), color = user_color
                    )
                await message.channel.send(embed = embed)

            # CHOP
            elif command == "chop":
                if user_money >= 200 and user_axes > 0:
                    user_money -= 200
                    amount_chopped = random.randint(0, 32)
                    user_wood += amount_chopped
                    embed = discord.Embed(
                        title = user_accnt_name + " Went Logging!",
                        description = (
                            "They spent 200 :coin: and got " +
                            str(amount_chopped) + " wood."
                        ), color = user_color
                    )
                elif user_pickaxes == 0:
                    embed = discord.Embed(
                        title = "Tool Needed",
                        description = (
                            "You need an axe to go logging." +
                            "\nUse \"/farm buy axe\" to buy one."
                        ), color = user_color
                    )
                else:
                    embed = discord.Embed(
                        title = "Money Needed",
                        description = (
                            "You need 200 :coin: to go logging." +
                            "\nYou only have " + format_num(user_money) +
                            " :coin:."
                        ), color = user_color
                    )
                await message.channel.send(embed = embed)

            # BUY
            elif command.startswith("buy"):
                passed_content = command.replace("buy", "").strip().split(" ")
                if len(passed_content) > 0 and passed_content[0] != "":
                    item = passed_content[0].lower()
                    if len(passed_content) > 1:
                        try:
                            quantity = int(passed_content[1])
                        except ValueError:
                            quantity = 1
                    else:
                        quantity = 1
                    match(item):
                        case "field":
                            cost = 10000
                        case "seeds":
                            cost = 300
                        case "axe":
                            cost = 500
                        case "pickaxe":
                            cost = 500
                        case "rock":
                            cost = 60
                        case "wood":
                            cost = 30
                        case _:
                            cost = -1
                    cost *= quantity
                    if cost != -1 and cost <= user_money:
                        user_money -= cost
                        title_content = (
                            user_accnt_name + " bought " + str(quantity)
                        )
                        match(item):
                            case "field":
                                user_fields_empty += 1
                                title_content += " field(s)."
                            case "seeds":
                                user_seeds += 1
                                title_content += " packet(s) of seeds."
                            case "axe":
                                user_axes += 1
                                title_content += " axe(s)."
                            case "pickaxe":
                                user_pickaxes += 1
                                title_content += " pickaxe(s)."
                            case "rock":
                                user_rock += 1
                                title_content += " rock."
                            case "wood":
                                user_wood += 1
                                title_content += " wood."
                        embed = discord.Embed(
                            title = title_content,
                            description = "Cost: " + str(cost) + " :coin:",
                            color = user_color
                        )
                    elif cost == -1:
                        embed = discord.Embed(
                            title = "This Item Does Not Exist.",
                            description = (
                                "List of items that can be bought:" +
                                "\n• Empty Field (\"field\") " +
                                "- 10 000 :coin:" +
                                "\n• Seeds - 300 :coin:" +
                                "\n• Axe - 500 :coin:" +
                                "\n• Pickaxe - 500 :coin:" +
                                "\n• Rock - 60 :coin:" +
                                "\n• Wood - 30 :coin:" +
                                "\nAll items must be singlular" +
                                "and all-lowercase"
                            ), color = user_color
                        )
                    else:
                        embed = discord.Embed(
                            title = "You Do Not Have Enough Money.",
                            description = (
                                "Cost: " + str(cost) + " :coin:\nYou have: " +
                                str(user_money) + ":coin:" + "\nMissing: " +
                                str(cost - user_money) + " :coin:"
                            ), color = user_color
                        )
                else:
                    description_content = (
                        "\nList of items that can be bought:" +
                        "\n• Empty Field (\"field\") " +
                        "- 10 000 :coin:" +
                        "\n• Seeds - 300 :coin:" +
                        "\n• Axe - 500 :coin:" +
                        "\n• Pickaxe - 500 :coin:" +
                        "\n• Rock - 60 :coin:" +
                        "\n• Wood - 30 :coin:" +
                        "\nAll items must be singlular (axe not axes)."
                    )
                    embed = generateMissingParamsEmbed(
                        ["item"], description_content, user_color
                    )
                await message.channel.send(embed = embed)

            # SELL
            elif command.startswith("sell"):
                passed_content = (
                    command.replace("sell", "").strip().split(" ")
                )
                if len(passed_content) > 0 and passed_content[0] != "":
                    item = passed_content[0].lower()
                    if len(passed_content) > 1:
                        try:
                            quantity = int(passed_content[1])
                        except ValueError:
                            quantity = 1
                    else:
                        quantity = 1
                    match(item):
                        case "crop":
                            cost = (
                                user_peanuts + user_wheat * 5 +
                                user_potatoes * 10 + user_corn * 15 +
                                user_melons * 30
                            )
                            quantity = num = (
                                user_peanuts + user_wheat + user_potatoes +
                                user_corn + user_melons
                            )
                        case "peanut":
                            cost = 1
                            if(len(passed_content) > 1 and
                            passed_content[1] == "all"):
                                quantity = user_peanuts
                            num = user_peanuts
                        case "wheat":
                            cost = 5
                            if(len(passed_content) > 1 and
                            passed_content[1] == "all"):
                                quantity = user_wheat
                            num = user_wheat
                        case "potato":
                            cost = 10
                            if(len(passed_content) > 1 and
                            passed_content[1] == "all"):
                                quantity = user_potatoes
                            num = user_potatoes
                        case "corn":
                            cost = 15
                            if(len(passed_content) > 1 and
                            passed_content[1] == "all"):
                                quantity = user_corn
                            num = user_corn
                        case "melon":
                            cost = 30
                            if(len(passed_content) > 1 and
                            passed_content[1] == "all"):
                                quantity = user_melons
                            num = user_melons
                        case "rock":
                            cost = 50
                            if(len(passed_content) > 1 and
                            passed_content[1] == "all"):
                                quantity = user_rock
                            num = user_rock
                        case "wood":
                            cost = 25
                            if(len(passed_content) > 1 and
                            passed_content[1] == "all"):
                                quantity = user_wood
                            num = user_wood
                        case "axe":
                            cost = 300
                            num = user_axes
                        case "pickaxe":
                            cost = 300
                            num = user_pickaxes
                        case _:
                            cost = -1
                            num = -1
                    cost *= quantity
                    if cost != -1 and quantity <= num:
                        user_money += cost
                        title_content = (
                            user_accnt_name + " Sold " + str(quantity)
                        )
                        match(item):
                            case "crop":
                                user_peanuts = 0
                                user_wheat = 0
                                user_potatoes = 0
                                user_corn = 0
                                user_melons = 0
                                title_content += " Crop(s)."
                            case "peanut":
                                user_peanuts -= quantity
                                title_content += " Peanut(s)."
                            case "wheat":
                                user_wheat -= quantity
                                title_content += " Wheat."
                            case "potato":
                                user_potatoes -= quantity
                                title_content += " Potato(es)."
                            case "corn":
                                user_corn -= quantity
                                title_content += " Corn."
                            case "melon":
                                user_melons -= quantity
                                title_content += " Melon(s)."
                            case "rock":
                                user_rock -= quantity
                                title_content += " Rock."
                            case "wood":
                                user_wood -= quantity
                                title_content += " Wood."
                            case "axe":
                                user_axes -= quantity
                                title_content += " Axe(s)."
                            case "pickaxe":
                                user_pickaxes -= quantity
                                title_content += " Pickaxe(s)."
                        embed = discord.Embed(
                            title = title_content,
                            description = "Profit: " + str(cost) + " :coin:",
                            color = user_color
                        )
                    elif cost == -1:
                        embed = discord.Embed(
                            title = "This Item Does Not Exist.",
                            description = (
                                "\nList of items that can be sold:" +
                                "\n• Rock - 60 :coin:" +
                                "\n• Wood - 30 :coin:" +
                                "\n• Crops - Sell all crops" +
                                "\n• Peanuts - 1 :coin:" +
                                "\n• Wheat - 5 :coin:" +
                                "\n• Potatoes - 10 :coin:" +
                                "\n• Corn - 15 :coin:" +
                                "\n• Melons - 30 :coin:" +
                                "\n• Axe - 500 :coin:" +
                                "\n• Pickaxe - 500 :coin:"
                                "\nAll items must be singlular " +
                                "(axe not axes)."
                            ), color = user_color
                        )
                    else:
                        embed = discord.Embed(
                            title = (
                                "You Don’t Have " + format_num(quantity) +
                                " " + item.capitalize() + "(e)(s)."
                            ),
                            description = (
                                "You have: " + str(num) +
                                "\nYou tried to sell: " + str(quantity) +
                                "\nMissing: " + str(quantity - num)
                            ), color = user_color
                        )
                else:
                    description_content = (
                        "\nList of items that can be sold:" +
                        "\n• Rock - 60 :coin:" +
                        "\n• Wood - 30 :coin:" +
                        "\n• Crops - Sell all crops" +
                        "\n• Peanuts - 1 :coin:" +
                        "\n• Wheat - 5 :coin:" +
                        "\n• Potatoes - 10 :coin:" +
                        "\n• Corn - 15 :coin:" +
                        "\n• Melons - 30 :coin:" +
                        "\n• Axe - 500 :coin:" +
                        "\n• Pickaxe - 500 :coin:"
                        "\nAll items must be singlular (axe not axes)."
                    )
                    embed = generateMissingParamsEmbed(
                        ["item"], description_content, user_color
                    )
                await message.channel.send(embed = embed)

            # UPDATING USER DATA
            match user_color:
                case 0xff0000:
                    user_color = "red"
                case 0xff8000:
                    user_color = "orange"
                case 0xffff00:
                    user_color = "yellow"
                case 0x00ff00:
                    user_color = "green"
                case 0x0000ff:
                    user_color = "blue"
                case 0x800080:
                    user_color = "purple"
                case 0xffffff:
                    user_color = "white"
                case _:
                    user_color = "black"
            with open(user_file_name, "w") as file:
                file.write(
                    user_accnt_name + "\n" +
                    str(user_cmd_count) + "\n" +
                    user_color + "\n" +
                    user_read_announcement + "\n" +
                    user_claimed_daily + "\n" +
                    user_seen_report + "\n" +
                    str(user_money) + "\n" +
                    str(user_rock) + "\n" +
                    str(user_wood) + "\n" +
                    str(user_axes) + "\n" +
                    str(user_pickaxes) + "\n" +
                    str(user_seeds) + "\n" +
                    str(user_peanuts) + "\n" +
                    str(user_wheat) + "\n" +
                    str(user_potatoes) + "\n" +
                    str(user_corn) + "\n" +
                    str(user_melons) + "\n" +
                    str(user_fields_empty) + "\n" +
                    str(user_fields_peanut) + "\n" +
                    str(user_fields_wheat) + "\n" +
                    str(user_fields_potato) + "\n" +
                    str(user_fields_corn) + "\n" +
                    str(user_fields_melon) + "\n" +
                    str(user_mines) + "\n" +
                    str(user_printers) + "\n" +
                    str(user_fence_lvl) + "\n" +
                    user_report
                )

# RUN MAIN FUNCTION
main()
client.run(TOKEN)