import requests
from bs4 import BeautifulSoup
import csv

page = requests.get("https://www.yallakora.com/match-center")

def main(page):

  src = page.content
  soup = BeautifulSoup(src, "lxml")
  matches_details = []
  all_championships = soup.find_all("div", {'class' : 'matchCard'})

  def get_match_info(championship):
    championship_title = championship.contents[1].find('h2').text.strip()
    matches_data = championship.contents[3].find_all('li')
    for i in range(len(matches_data)):
      teamA = matches_data[i].find('div', {'class' : 'teamA'}).text.strip()
      teamB = matches_data[i].find('div', {'class' : 'teamB'}).text.strip()
      scores = matches_data[i].find('div', {'class' : 'MResult'}).find_all('span', {'class' : 'score'})
      score = f"{scores[0].text.strip()} - {scores[1].text.strip()}"
      time = matches_data[i].find('div', {'class' : 'MResult'}).find('span', {'class' : 'time'}).text.strip()
      matches_details.append({"البطولة" : championship_title, "الفريق المستضيف" : teamA, "القريق الضيف" : teamB, "النتيجة" : score, "التوقيت" : time})

  for i in range(len(all_championships)):
    get_match_info(all_championships[i])
  #print(matches_details)

  keys = matches_details[0].keys()
  with open("matches.csv", "w") as file:
    writer = csv.DictWriter(file, keys)
    writer.writeheader()
    writer.writerows(matches_details)
  

  print("done")

main(page)