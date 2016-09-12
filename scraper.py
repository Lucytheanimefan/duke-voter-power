# scrapes fivethiryeight to get voter power data

'''
'Tipping-point chance' is the probability that a state will provide the decisive vote in the Electoral College. 
'Voter power index' is the relative likelihood that an individual voter in a state will determine the Electoral College winner.
'''
import requests, bs4

res=requests.get('http://projects.fivethirtyeight.com/2016-election-forecast/')
res.raise_for_status

soup=bs4.BeautifulSoup(res.text,'html.parser')

def get_voting_info(class_name):
	state_name = ""
	num_value=None
	json_dict={}

	roi_table = soup.find_all('div',{'class':class_name})

	roi_table_soup = bs4.BeautifulSoup(str(roi_table),'html.parser')

	i=0;
	for state in roi_table_soup.find_all(['div','span'],{'class':['long','pct']}):
		if i%2==0:
			state_name=state.get_text().strip("<")
		else: 
			num_value=state.get_text().strip("<")

		if state_name and num_value:
			#print state_name +","+num_value
			json_dict[state_name.encode('utf=8')]=num_value.encode('utf-8')
			#reset to none
			state_name=None
			num_value=None
		i=i+1
	return json_dict
		


print get_voting_info('roi-table')

print "--------------------------"

print get_voting_info('tipping-table')


#def format_data_json(data):
