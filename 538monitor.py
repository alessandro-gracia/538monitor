import pandas, os, urllib.request, yagmail
from datetime import datetime
from os import path 

#Print current time for tracking changes if this script is output to a file for logging
now = datetime.now()
print('\nScript Run Time:', now)

#Choose your preference for winner as 'challenger' or 'incumbent'
desired_winner = ''
#Set your incoming/outgoing email addresses
to_email = ''
from_email = ''
from_email_oauth = ''
#Set the URL for the csv updates of the election you'd like to monitor
url = 'https://projects.fivethirtyeight.com/2020-general-data/presidential_national_toplines_2020.csv'

#Assigns variables based on candidate preference
if desired_winner == 'challenger':
    desired_winner = 'ecwin_chal'
    desired_winner_name = 'candidate_chal'
    desired_loser = 'ecwin_inc'
    desired_loser_name = 'candidate_inc'
elif desired_winner == 'incumbent':
    desired_winner = 'ecwin_inc'
    desired_winner_name = 'candidate_inc'
    desired_loser = 'ecwin_chal'
    desired_loser_name = 'candidate_chal'

#Download current status, extract desired values, delete downloaded file
urllib.request.urlretrieve(url, '538forecast.csv')
df_updatestat = pandas.read_csv('538forecast.csv', parse_dates=['timestamp'])
desired_winner_curstat = df_updatestat.loc[0, desired_winner]
desired_winner_name = df_updatestat.loc[0, desired_winner_name]
desired_loser_curstat = df_updatestat.loc[0, desired_loser]
desired_loser_name = df_updatestat.loc[0, desired_loser_name]
time_stamp_cur = df_updatestat.loc[0, 'timestamp']
os.remove('538forecast.csv')

#Add updated stats to pandas dataframe and print for log
dict_curstat  = {desired_winner_name: [desired_winner_curstat],
				desired_loser_name: [desired_loser_curstat],
				'Time Stamp': [time_stamp_cur]
				}
df_curstat = pandas.DataFrame(dict_curstat, columns = [desired_winner_name, desired_loser_name, 'Time Stamp'])
print('\nCurrent:')
print(df_curstat)

#Check if this is first run of script, if so print current values to file csv file for comparison on subsequent runs
if not path.exists("538lastupdate.csv"):
	print('\nThis is the first run of the script so there are no changes to detect\nPrinting csv file to use for future comparisons\n')
	df_curstat.to_csv('538lastupdate.csv')
	exit()

#Add previous stats to pandas dataframe and print for log 
df_oldstat = pandas.read_csv('538lastupdate.csv', index_col=0, parse_dates=['Time Stamp'])
print('\nPrevious:')
print(df_oldstat)

#Assign previous stats to variables and format statistics for comparison/readability
desired_winner_oldstat = df_oldstat.loc[0, desired_winner_name]
desired_loser_oldstat = df_oldstat.loc[0, desired_loser_name]
time_stamp_old = df_oldstat.loc[0, 'Time Stamp']
desired_winner_curstat = round(float(desired_winner_curstat) * float(100), 1)
desired_winner_oldstat = round(float(desired_winner_oldstat) * float(100), 1)
desired_loser_curstat = round(float(desired_loser_curstat) * float(100), 1)
desired_loser_oldstat = round(float(desired_loser_oldstat) * float(100), 1)

#Check if forecast has been updated before continuing to comparison
if time_stamp_cur == time_stamp_old:
	print('\nNo update to forecast since last check, exiting.\n')
	print(desired_winner_name +' Status:')
	print(desired_winner_curstat)
	print(desired_loser_name +' Status:')
	print(desired_loser_curstat)
	print()
	exit()
else:
	print('\nForecast update detected, checking for changes...\n')

#Compare stats and generate email if warranted, remove record of previous stats and replace with updated stats for next comparison
if (desired_winner_curstat > desired_winner_oldstat) and (desired_loser_curstat < desired_loser_oldstat):
	print('Detected movement for both candidates\n')
	combined_status = '<strong>' + desired_winner_name + ' Change:</strong> <br>' + \
	'Current:  ' + str(desired_winner_curstat) + '%' + '<br>' + \
	'Previous: ' + str(desired_winner_oldstat) + '%' + '<br>' + \
	'<strong>' + desired_loser_name + ' Change:</strong> <br>' + \
	'Current:  ' + str(desired_loser_curstat) + '%' + '<br>' + \
	'Previous: ' + str(desired_loser_oldstat) + '%'
	yag = yagmail.SMTP(from_email, oauth2_file=from_email_oauth)
	yag.send(to=to_email, subject='538 Forecast Update: ' + desired_winner_name + ' Up/' + desired_loser_name + ' Down', contents='%s' % combined_status)
	os.remove('538lastupdate.csv')
	df_curstat.to_csv('538lastupdate.csv')
	exit()
if (desired_winner_curstat > desired_winner_oldstat):
	print('Detected movement for ' + desired_winner_name + '\n')
	combined_status = '<strong>' + desired_winner_name + ' Change:</strong> <br>' + \
	'Current:  ' + str(desired_winner_curstat) + '%' + '<br>' + \
	'Previous: ' + str(desired_winner_oldstat) + '%'
	yag = yagmail.SMTP(from_email, oauth2_file=from_email_oauth)
	yag.send(to=to_email, subject='538 Forecast Update: ' + desired_winner_name + ' Up', contents='%s' % combined_status)
	os.remove('538lastupdate.csv')
	df_curstat.to_csv('538lastupdate.csv')
	exit()
if (desired_loser_curstat < desired_loser_oldstat):
	print('Detected movement for ' + desired_loser_name + '\n')
	combined_status = '<strong>' + desired_loser_name + ' Change:</strong> <br>' + \
	'Current:  ' + str(desired_loser_curstat) + '%' + '<br>' + \
	'Previous: ' + str(desired_loser_oldstat) + '%'
	yag = yagmail.SMTP(from_email, oauth2_file=from_email_oauth)
	yag.send(to=to_email, subject='538 Forecast Update: ' + desired_loser_name + ' Down', contents='%s' % combined_status)
	os.remove('538lastupdate.csv')
	df_curstat.to_csv('538lastupdate.csv')
	exit()

#Print status to log if no significant changes were detected from last update
print('No desirable changes detected\n')
print(desired_winner_name +' Status:')
print(desired_winner_curstat)
print(desired_loser_name +' Status:')
print(desired_loser_curstat)
print()
