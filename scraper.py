# scrapes fivethiryeight to get voter power data

'''
'Tipping-point chance' is the probability that a state will provide the decisive vote in the Electoral College. 
'Voter power index' is the relative likelihood that an individual voter in a state will determine the Electoral College winner.
'''
import requests, bs4

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}
res=requests.get('http://projects.fivethirtyeight.com/2016-election-forecast/')
res.raise_for_status

soup=bs4.BeautifulSoup(res.text,'html.parser')

def get_voting_info(class_name, info_type):
	state_name = ""
	num_value=None
	json_dict={}

	roi_table = soup.find_all('div',{'class':class_name})

	roi_table_soup = bs4.BeautifulSoup(str(roi_table),'html.parser')

	i=0;
	for state in roi_table_soup.find_all(['div','span'],{'class':['long','pct']}):
		if i%2==0:
			state_name=state.get_text().strip("<").rstrip()
		else: 
			num_value=state.get_text().strip("<").rstrip()

		if state_name and num_value:
			#print state_name +","+num_value
			if state_name.encode('utf=8') in us_state_abbrev:
				json_dict[us_state_abbrev[state_name.encode('utf=8')]]={info_type: num_value.encode('utf-8')}
			else:
				json_dict[state_name.encode('utf=8')]={info_type:num_value.encode('utf-8')}
			#reset to none
			state_name=None
			num_value=None
		i=i+1
	return json_dict
		
def write_data_to_file(data, filename):
	text_file = open(filename, "w")
	text_file.write(str(data))
	text_file.close()

print get_voting_info('roi-table','votingPowerIndex')
write_data_to_file(get_voting_info('roi-table','votingPowerIndex'), "voting_power.txt")

print "--------------------------"

print get_voting_info('tipping-table','tippingPower')
write_data_to_file(get_voting_info('tipping-table','tippingPower'), "tipping_power.txt")

#def format_data_json(data):
