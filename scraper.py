# scrapes fivethiryeight to get voter power data

'''
“Tipping-point chance” is the probability that a state will provide the decisive vote in the Electoral College. 
“Voter power index” is the relative likelihood that an individual voter in a state will determine the Electoral College winner.
'''
import requests, bs4

res=requests.get('http://projects.fivethirtyeight.com/2016-election-forecast/')
res.raise_for_status

soup=bs4.BeautifulSoup(res.text,'html.parser')

def get_voting_info(class_name):
	roi_table = soup.find_all('div',{'class':class_name})

	roi_table_soup = bs4.BeautifulSoup(str(roi_table),'html.parser')

	for state in roi_table_soup.find_all(['div','span'],{'class':['long','pct']}):
		print state.get_text().strip("<")


get_voting_info('roi-table')

print "--------------------------"

get_voting_info('tipping-table')
