## IMPORTING LIBRARIES ##

import json
import datetime
import statsapi
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

## LIST OF AVAILABLE COMMANDS ##

commands = [
    '/hr_leaders [season, default is current]',
    '/hr_leaders_rookies [season, default is current]',
    '/era_leaders [season, default is current]',
    '/era_leaders_rookies [season, default is current',
    '/today_schedule',
    '/player [first name or last name]'
]

## READING THE TOKEN FROM THE JSON FILE ##

f = open('token.json',)
reading = json.load(f)
token = reading['token']
f.close

## DEFAULT FUNCTIONS ##

def extract_number(text):
    return text.split()[1].strip()

## COMMANDS FUNCTIONS ##

def start(update, context): ## START COMMAND ##
    update.message.reply_text(f'Bot is started! Use /help.')

def help(update, context): ## HELP COMMAND ##
    data = 'Available commands: \n'
    for p in commands:
        data += p + '\n'
    update.message.reply_text(f'{data}')

def hr_leaders(update, context): ## HOMERUNS LEADERS ##
    flag = True
    try:
        s = int(extract_number(update.message.text))
    except:
        flag = False
    if flag is False:
        currentDateTime = datetime.datetime.now()
        date = currentDateTime.date()
        year = date.strftime('%Y')
        currentseason = int(year)
        header = 'USE YOUR PHONE HORIZONTALLY!\n\nHR Leaders for current season:\n\n'
        data = statsapi.league_leaders('homeRuns', season = currentseason, limit = 5)
    else:
        header = f'USE YOUR PHONE HORIZONTALLY!\n\nHR Leaders for {s} season:\n\n'
        data = statsapi.league_leaders('homeRuns', season = s, limit = 5)
    data.split('\n')
    msg = header + data
    update.message.reply_text(f'{msg}')

def hr_leaders_rookies(update, context): ## ROOKIES HOMERUNS LEADERS ##
    flag = True
    try:
        s = int(extract_number(update.message.text))
    except:
        flag = False
    if flag is False:
        currentDateTime = datetime.datetime.now()
        date = currentDateTime.date()
        year = date.strftime('%Y')
        currentseason = int(year)
        header = 'USE YOUR PHONE HORIZONTALLY!\n\nHR Rookies Leaders for current season:\n\n'
        data = statsapi.league_leaders('homeRuns', season = currentseason, playerPool = 'rookies', limit = 5)
    else:
        header = f'USE YOUR PHONE HORIZONTALLY!\n\nHR Rookies Leaders for {s} season:\n\n'
        data = statsapi.league_leaders('homeRuns', season = s, playerPool = 'rookies', limit = 5)
    data.split('\n')
    msg = header + data
    update.message.reply_text(f'{msg}')

def era_leaders(update, context): ## ERA LEADERS ##
    flag = True
    try:
        s = int(extract_number(update.message.text))
    except:
        flag = False
    if flag is False:
        currentDateTime = datetime.datetime.now()
        date = currentDateTime.date()
        year = date.strftime('%Y')
        currentseason = int(year)
        header = 'USE YOUR PHONE HORIZONTALLY!\n\nERA Leaders for current season:\n\n'
        data = statsapi.league_leaders('earnedRunAverage', season = currentseason, limit = 5)
    else:
        header = f'USE YOUR PHONE HORIZONTALLY!\n\nERA Leaders for {s} season:\n\n'
        data = statsapi.league_leaders('earnedRunAverage', season = s, limit = 5)
    data.split('\n')
    msg = header + data
    update.message.reply_text(f'{msg}')

def era_leaders_rookies(update, context): ## ROOKIES ERA LEADERS ##
    flag = True
    try:
        s = int(extract_number(update.message.text))
    except:
        flag = False
    if flag is False:
        currentDateTime = datetime.datetime.now()
        date = currentDateTime.date()
        year = date.strftime('%Y')
        currentseason = int(year)
        header = 'USE YOUR PHONE HORIZONTALLY!\n\nERA Rookies Leaders for current season:\n\n'
        data = statsapi.league_leaders('earnedRunAverage', season = currentseason, playerPool = 'rookies', limit = 5)
    else:
        header = f'USE YOUR PHONE HORIZONTALLY!\n\nERA Rookies Leaders for {s} season:\n\n'
        data = statsapi.league_leaders('earnedRunAverage', season = s, playerPool = 'rookies', limit = 5)
    data.split('\n')
    msg = header + data
    update.message.reply_text(f'{msg}')

def today_schedule(update, context): ## TODAY'S SCHEDULE ##
    header = 'USE YOUR PHONE HORIZONTALLY!\n\nToday\'s games schedule:\n\n'
    data = statsapi.schedule()
    finaldata = header
    for game in data:
        finaldata += game['summary'] + ' - ' + game['game_datetime'].split('T', 1)[1] + '\n\n'
    update.message.reply_text(f'{finaldata}') 

def player(update, context): ## LOOKUP PLAYER INFORMATION ##
    try:
        n = extract_number(update.message.text)
    except:
        update.message.reply_text('No player name given.')
        return
    header = 'USE YOUR PHONE HORIZONTALLY!\n\nPlayers found: \n\n'
    data = statsapi.lookup_player(n)
    if not data:
        update.message.reply_text(f'No players found with name \'{n}\'.')
    else:
        finaldata = header
        for player in data:
            finaldata += ('Full name: {}\nNumber: {}\nPosition: {}\nMLB Debut: {}\n\n'.format(player['fullFMLName'], player['primaryNumber'], player['primaryPosition']['abbreviation'], player['mlbDebutDate']))
        update.message.reply_text(f'{finaldata}')

## BOT STARTUP ##

def main():
    upd = Updater(token, use_context = True)
    disp = upd.dispatcher

    ## COMMAND HANDLERS ##

    disp.add_handler(CommandHandler('start', start))
    disp.add_handler(CommandHandler('help', help))
    disp.add_handler(CommandHandler('hr_leaders', hr_leaders))
    disp.add_handler(CommandHandler('hr_leaders_rookies', hr_leaders_rookies))
    disp.add_handler(CommandHandler('era_leaders', era_leaders))
    disp.add_handler(CommandHandler('era_leaders_rookies', era_leaders_rookies))
    disp.add_handler(CommandHandler('today_schedule', today_schedule))
    disp.add_handler(CommandHandler('player', player))
    
    upd.start_polling()
    print('BOT STARTED AT https://t.me/MLBStats_Bot')
    upd.idle()

if __name__ == '__main__':
    main()