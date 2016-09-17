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

json_dict={}
color_dict={}
hexColors=['#8000ff','#8c19ff','#9932ff','#a64cff','#b266ff','#bf7fff','#cc99ff','#d8b2ff','#e5ccff','#f2e5ff','#ffffff']
def get_voting_info(class_name, info_type):
	state_name = ""
	num_value=None

	roi_table = soup.find_all('div',{'class':class_name})

	roi_table_soup = bs4.BeautifulSoup(str(roi_table),'html.parser')

	i=0;
	for state in roi_table_soup.find_all(['div','span'],{'class':['long','pct']}):
		if i%2==0:
			state_name=state.get_text().strip("<").rstrip()
		else: 
			num_value=state.get_text().strip("<").rstrip()

		if state_name and num_value:
			stateName = state_name.encode('utf=8')
			if "Nebraska" in stateName:
				print "Nebraska!"
				stateName="Nebraska"
			if "Maine" in stateName:
				stateName="Maine"
			if stateName in us_state_abbrev:
				state_abbrev = us_state_abbrev[stateName]
				if state_abbrev in json_dict:
					json_dict[state_abbrev][info_type]= num_value.encode('utf-8')
				else:
					json_dict[state_abbrev]={info_type:num_value.encode('utf-8')}

				json_dict[state_abbrev]["fillKey"]=num_value.encode('utf-8')
				if class_name=='tipping-table':
					print "filling colors"
					#num_value=num_value.strip("%")
					if float(num_value.strip('%'))>15:
						color_dict[num_value.encode('utf-8')]=hexColors[0]
					elif float(num_value.strip('%'))>10:
						color_dict[num_value.encode('utf-8')]=hexColors[1]
					elif float(num_value.strip('%'))>9:
						color_dict[num_value.encode('utf-8')]=hexColors[2]
					elif float(num_value.strip('%'))>8:
						color_dict[num_value.encode('utf-8')]=hexColors[3]
					elif float(num_value.strip('%'))>7:
						color_dict[num_value.encode('utf-8')]=hexColors[4]
					elif float(num_value.strip('%'))>6:
						color_dict[num_value.encode('utf-8')]=hexColors[5]
					elif float(num_value.strip('%'))>5:
						color_dict[num_value.encode('utf-8')]=hexColors[6]
					elif float(num_value.strip('%'))>4:
						color_dict[num_value.encode('utf-8')]=hexColors[7]
					elif float(num_value.strip('%'))>3:
						color_dict[num_value.encode('utf-8')]=hexColors[8]
					elif float(num_value.strip('%'))>2:
						color_dict[num_value.encode('utf-8')]=hexColors[9]
					else:
						color_dict[num_value.encode('utf-8')]=hexColors[10]
					#else:
					#	color_dict[num_value.encode('utf-8')]=hexColors[11]
			'''
			else:
				if "Nebraska" in state_name.encode('utf-8'):
					if "Nebraska" in json_dict:
						json_dict[state_name.encode('utf-8')][info_type]=num_value.encode('utf-8')
					else:
						json_dict[state_name.encode('utf-8')]={info_type:num_value.encode('utf-8')}
			'''
			#reset to none
			state_name=None
			num_value=None
		i=i+1
	write_data_to_file(color_dict, "colors.txt")
	return json_dict
		
def populateData():
	get_voting_info('roi-table','votingPowerIndex')
	get_voting_info('tipping-table','tippingPower')
	return json_dict

def write_data_to_file(data, filename):
	text_file = open(filename, "w")
	text_file.write(str(data))
	text_file.close()


write_data_to_file(str(populateData()), "voting_data.txt")


