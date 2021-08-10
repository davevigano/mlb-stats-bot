## IMPORTING LIBRARIES ##

import json
import statsapi
import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

## LIST OF AVAILABLE COMMANDS ##

commands = [
    '/hr_leaders [season, default is current]',
    '/hr_leaders_rookies [season, default is current]'
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
        header = f'HR Leaders for {s} season: \n\n'
        data = statsapi.league_leaders('homeRuns', season = s, limit = 5)
    # data.split('\n')
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
        header = f'HR Rookies Leaders for {s} season: \n\n'
        data = statsapi.league_leaders('homeRuns', season = s, playerPool = 'rookies', limit = 5)
    data.split('\n')
    msg = header + data
    update.message.reply_text(f'{msg}')

## BOT STARTUP ##

def main():
    upd = Updater(token, use_context = True)
    disp = upd.dispatcher

    ## COMMAND HANDLERS ##

    disp.add_handler(CommandHandler('start', start))
    disp.add_handler(CommandHandler('help', help))
    disp.add_handler(CommandHandler('hr_leaders', hr_leaders))
    disp.add_handler(CommandHandler('hr_leaders_rookies', hr_leaders_rookies))
    
    upd.start_polling()
    print('BOT STARTED AT https://t.me/MLBStats_Bot')
    upd.idle()

if __name__ == '__main__':
    main()