import urllib.request
from bs4 import BeautifulSoup



def readStateAbb():
	f = open("stateAbb.txt","r")
	return f.read().split('\n')


def readTable(table,file, type):
	lists = table.find_all("tr")[1:]
	file.write("status, species, listing name, link, spcode\n")
	for l in lists:
		[t, n] = l.find_all("td")
		link = "https://ecos.fws.gov" + n.find_all("a")[0].get('href')
		code = link.split("spcode=")[1]
		if (type == "a"):
			species = n.contents[0].split("\xa0")[0]
			a_total.add(code)
		else:
			species = n.contents[0].split(" (")[0]
			p_total.add(code)
		
		line = t.contents[0] + ",\"" + species + "\",\"" + n.find("i").contents[0] + "\"," + link + ","+ code + "\n"
		file.write(line)

	return len(lists)
def getStateList(state):
	file_animal = open("%s_animal_list.csv"%state, "w")
	file_plant = open("%s_plant_list.csv"%state, "w")
	content = urllib.request.urlopen("https://ecos.fws.gov/ecp0/reports/species-listed-by-state-report?state=%s&status=listed"%state).read()
	soup = BeautifulSoup(content, 'html.parser')
	[animal, plant] = soup.find_all("table")
	aNum = readTable(animal, file_animal, "a")
	pNum = readTable(plant, file_plant, "p")
	stateSummary.write(state + "," + str(aNum) + "," + str(pNum) + "\n")

states = readStateAbb()
stateSummary = open("summary.csv", "w")
stateSummary.write("state, animal, plant\n")
total_animal = open("distinct_animal.csv", "w")
total_plant = open("distinct_plant.csv", "w")
a_total = set()
p_total = set()

for state in states:
	getStateList(state)


for a in a_total:
	total_animal.write(a + "\n")

for p in p_total:
	total_plant.write(p + "\n")

