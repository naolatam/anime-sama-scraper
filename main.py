from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
from mysql import connector
from threading import Thread
import fileTransferor
import utils
import requests
import re

dbCredit = {
    "host":"DB_HOST",
  "user":"DB_USERNAME",
  "password":"DB_PASSWORD",
  "database":"DB_NAME"
}
def download(link, path):

# Send a GET request to the image URL
    response = requests.get(link)

# Check if the request was successful (status code 200)
    if response.status_code == 200:
    # Get the content of the image
        image_content = response.content

    # Specify the local file path where you want to save the image
        local_file_path = path

    # Save the image to the local file
        with open(local_file_path, 'wb') as file:
            file.write(image_content)



db = connector.connect(
    host=dbCredit["host"],
  user=dbCredit["user"],
  password=dbCredit["password"],
  database=dbCredit["database"]
)

wd = webdriver.Chrome()

print("Récupération des animes...")
wd.get("https://anime-sama.fr/catalogue/index.php")
links = []
pics = []

try:
    wd.find_element(By.XPATH, '//*[text()="J\'ACCEPTE"]').click()
    time.sleep(0.1)
    wd.find_element(By.XPATH, '//*[text()="J\'ACCEPTE"]').click()
    print("Cookies accepted!")
    time.sleep(0.1)
except NoSuchElementException:
    print("Cookies already accepted")

wd.find_element(By.XPATH, "//*[@value='Anime']").click()
time.sleep(0.3)
wd.find_element(By.XPATH, "//*[@id='btnTriList']").click()
wd.find_element(By.XPATH, "//*[@id='btnTriList']").click()
time.sleep(0.3)
wd.find_element(By.XPATH, "//*[@id='btnTriList']").click()

print("  * " + str(wd.find_elements(By.CLASS_NAME, "cardListAnime").__len__()) + " Anime trouvés!")
print("  * Traitement des animes trouvés!")

for i in wd.find_elements(By.CLASS_NAME, "cardListAnime"):
    if i.value_of_css_property("display") != "none" :
        x=i.find_element(By.CSS_SELECTOR, "a")
        links.append(x.get_property("href"))
        pics.append(x.find_element(By.CSS_SELECTOR, "img").get_property("src"))
print("  * " + str(len(links)) + " animes après traitement")
print("  * Fermeture du webdriver")
wd.close()
print("Animes récupéré! ")
print("Début du traitement!")


for link in links:
    animePage = requests.get(link )
    print(animePage.url)
    animeName = animePage.text.split('<h4 id="titreOeuvre"')[1].split(">")[1].split("<")[0]
    animeOtherName = animePage.text.split('<h2 id="titreAlter"')[1].split(">")[1].split("<")[0]
    animeDesc = animePage.text.split('<p class="text-sm text-gray-400 mt-2"')[1].split(">")[1].split("<")[0]
    animeGenre = animePage.text.split('<a class="text-sm text-gray-300 mt-2">')[1].split('<')[0]
    animeTrailer = animePage.text.split('<iframe id="bandeannonce" class="h-64 w-full lg:w-full" scrolling="no" src="')[1].split('"')[0] if '<iframe id="bandeannonce" class="h-64 w-full lg:w-full" scrolling="no" src="' in animePage.text else None
    animePanel = animePage.text.split("panneauAnime(")[1].split(")")[0]
    parametres = re.findall(r'panneauAnime\((.*?),\s*(.*?)\)', animePage.text)[2:]
    pic = ""

    print("  * " + animeName)
    print("  * " + animeOtherName)
    print("  * " + animeDesc)
    print("  * " + str(len(parametres)) + " saisons")
    obj = {
        "saisonCount": len(parametres),
        "saison": [
           
        ]
    }

    for i in parametres:
        if i[1] == '"url"': continue

        episodes = utils.getEpisode(animePage.url + i[1].replace('"', "").replace('"', ""))
        obj["saison"].append({
            "name": i[0].replace('"', "").replace('"', ""),
            "link": animePage.url + i[1].replace('"', "").replace('"', ""),
            "episode": episodes
        })

    animeName = animeName.replace('"', '\\"').replace("'", "\\'")
    animeOtherName = animeOtherName.replace('"', '\\"').replace("'", "\\'")
    animeDesc = animeDesc.replace('"', '\\"').replace("'", "\\'")

    cursor = db.cursor()
    cursor.execute("SELECT * FROM video WHERE name='{}'".format(animeName))
    res = cursor.fetchall()
    if len(res) == 0:
        imName = pics[links.index(link)].split(".")[-2].split("/")[-1] + "-IMAGE-AUTO-ADD-SCRIPT." + pics[links.index(link)].split(".")[-1]
        download(pics[links.index(link)], "./temp/" + imName)
        with open("./temp/" + imName, "rb") as file:
            requests.post("https://stream.doomoon.fr/admin/uploadImg.php", data={'code': '123AdminAUTO-ADD-Script-UPLOAD!*/'}, files={"image": file})
        pic = f"./img/carrousel/{imName}"
        cursor.execute(f"INSERT INTO `video`(`name`, `description`, `actor`, `genre`, `dateofpublication`, `trailer`, `picture`, `link`, `during`, `type`, `episode`, `parent`, `id`) VALUES ('{animeName}','Other name: {animeOtherName}<br>Synopsis: {animeDesc}','','{animeGenre}','{time.time()}','{animeTrailer}','{pic}','','','ANIME','0',NULL,NULL)")
        db.commit()
        print("  * Anime créé dans la base de données!")

        cursor.execute(f"SELECT * FROM video WHERE picture='{pic}'")
        animeID = cursor.fetchall()[0][-1]
        animeSaisonId = []
        for saisonI in range(len(obj["saison"])):
            # TO CONTINUE
            cursor.execute(f"INSERT INTO `video`(`name`, `description`, `actor`, `genre`, `dateofpublication`, `trailer`, `picture`, `link`, `during`, `type`, `episode`, `parent`, `id`) VALUES ('{obj['saison'][saisonI]['name']}','Other name: {animeOtherName}<br>Synopsis: {animeDesc}','','{animeGenre}','{time.time()}','{animeTrailer}','{pic}','','','ANIME','{saisonI+1}',{animeID},NULL)")
            db.commit()
            print(f"  *  * Saison {str(saisonI + 1)} créé dans la base de données!")

            cursor.execute(f"SELECT * FROM video WHERE picture='{pic}' AND episode='{saisonI +1}'")
            saisonId = cursor.fetchall()[0][-1]
            print(saisonId, animeID)
            thread = []
            for y in obj["saison"][saisonI]["episode"]:
                if y[0][0] == '': continue
                fileTransferor.processingEpisode(y, "temp", dbCredit, saisonId, f"Other name: {animeOtherName}<br>Synopsis: {animeDesc}", animeGenre, animeTrailer, pic, obj["saison"][saisonI]["episode"].index(y) + 1)

"""             for y in obj["saison"][saisonI]["episode"]:
                if y[0][0] == '': continue
                t = Thread(target=fileTransferor.processingEpisode, args=(y, "temp", dbCredit, saisonId, f"Other name: {animeOtherName}<br>Synopsis: {animeDesc}", animeGenre, animeTrailer, pic, obj["saison"][saisonI]["episode"].index(y) + 1))
                thread.append(t)
            activeThread = 0
            for t in thread:
                if activeThread <5:
                    t.start()
                else:
                    while activeThread >=5:
                        activeThread = 0
                        for t2 in thread:
                            if t2.is_alive(): activeThread +=1
                        time.sleep(0.2)
                    t.start()
 """             
time.sleep(800)