const teamColors = {
	'Arizona Diamondbacks': '#A71930',
	'Atlanta Braves': '#CE1141',
	'Baltimore Orioles': '#DF4601',
	'Boston Red Sox': '#BD3039',
	'Chicago White Sox': '#27251F',
	'Chicago Cubs': '#0E3386',
	'Cincinnati Reds': '#C6011F',
	'Cleveland Guardians': '#0C2340',
	'Colorado Rockies': '#33006F',
	'Detroit Tigers': '#0C2340',
	'Houston Astros': '#002D62',
	'Kansas City Royals': '#004687',
	'Los Angeles Angels': '#BA0021',
	'Los Angeles Dodgers': '#005A9C',
	'Miami Marlins': '#00A3E0',
	'Milwaukee Brewers': '#12284B',
	'Minnesota Twins': '#002B5C',
	'New York Yankees': '#003087',
	'New York Mets': '#FF5910',
	'Oakland Athletics': '#003831',
	'Philadelphia Phillies': '#E81828',
	'Pittsburgh Pirates': '#FDB827',
	'San Diego Padres': '#002D62',
	'San Francisco Giants': '#FD5A1E',
	'Seattle Mariners': '#0C2C56',
	'St. Louis Cardinals': '#C41E3A',
	'Tampa Bay Rays': '#092C5C',
	'Texas Rangers': '#C0111F',
	'Toronto Blue Jays': '#134A8E',
	'Washington Nationals': '#AB0003',
}

export function getTeamColor(team) {
	return teamColors[team] || '#000000'; // Default color if not found in the teamColors object
}

export default getTeamColor;