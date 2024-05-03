import requests
from urllib.parse import urlparse
import os
import time
from mysql import connector
import json
FILEMOON_API_KEY="API_KEY"
def getServer():
    res = requests.get(f"https://filemoonapi.com/api/upload/server?key={FILEMOON_API_KEY}")
    js = res.json()
    srv = js["result"]
    return srv
srv=getServer()
class processingEpisode():
    def __init__(self, url, tempFolder, database, parentId, animeDesc, animeGenre, animeTrailer, pic, episodeNumber) -> None:
        self.url = url
        self.folder = tempFolder
        self.episode = episodeNumber
        self.paths, self.fileNames = self._download()
        self.uploadFileCodes = self._upload()
        db = connector.connect(host=database["host"], user=database["user"], password=database["password"], database=database["database"] )
        self.cursor = db.cursor()
        self.default = self._getDefaultL()
        self.link = self._getLink()
        self.animeName = self.fileNames[0][0].lower().replace("_vostfr", "").replace("_vf", "").replace("_", " ").replace("'", "\\'").replace('"', '\\"')
        self.cursor.execute(f"INSERT INTO `video`(`name`, `description`, `actor`, `genre`, `dateofpublication`, `trailer`, `picture`, `link`, `during`, `type`, `episode`, `parent`, `id`) VALUES ('{self.animeName}','{animeDesc}','','{animeGenre}','{time.time()}','{animeTrailer}','{pic}','{json.dumps(self.link)}','','ANIME','{episodeNumber}', '{parentId}',NULL)")
        db.commit()
        pass

    def _download(self):
        l1 = self.url[0]
        l2 = self.url[1] if len(self.url) == 2 else None           
        hostl1 = self._getHost(l1)
        hostl2 = self._getHost(l2)
        paths = []
        fileNames = []

        if "sibnet" in hostl1:
            re1 = requests.get(l1[0])
            vid_link = "https://video.sibnet.ru" + re1.text.split(';player.src([{src: ')[1].split(',')[0].replace('"', "").replace('"', "")

            header ={
                "accept": "*/*",
                "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "range": "bytes=0-",
                "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Google Chrome\";v=\"122\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "video",
                "sec-fetch-mode": "no-cors",
                "sec-fetch-site": "same-origin",
                "Referer": "https://video.sibnet.ru/shell.php?videoid=4756806",
                "Referrer-Policy": "strict-origin-when-cross-origin"
 
            }
            re2 = requests.get(url=vid_link, headers=header, stream=True)
            videoId = re1.url.split("videoid=")[1]
            with open(f"./{self.folder}/{videoId}.mp4", "wb") as f:
                for chunck in re2.iter_content(chunk_size=8*1024):
                    if chunck:
                        f.write(chunck)
            paths.append((f"./{self.folder}/{videoId}.mp4", l1[1]))
            fileNames.append((re1.text.split('<meta property="og:title" content="')[1].split('"')[0], l1[1]))

        if hostl2 is not None and "sibnet" in hostl2:
            re1 = requests.get(l2[0])
            vid_link = "https://video.sibnet.ru" + re1.text.split(';player.src([{src: ')[1].split(',')[0].replace('"', "").replace('"', "")

            header ={
                "accept": "*/*",
                "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "range": "bytes=0-",
                "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Google Chrome\";v=\"122\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "video",
                "sec-fetch-mode": "no-cors",
                "sec-fetch-site": "same-origin",
                "Referer": "https://video.sibnet.ru/shell.php?videoid=4756806",
                "Referrer-Policy": "strict-origin-when-cross-origin"
 
            }
            re2 = requests.get(url=vid_link, headers=header, stream=True)
            videoId = re1.url.split("videoid=")[1]
            with open(f"./{self.folder}/{videoId}.mp4", "wb") as f:
                for chunck in re2.iter_content(chunk_size=1024*1024):
                    if chunck:
                        f.write(chunck)
            paths.append((f"./{self.folder}/{videoId}.mp4", l2[1]))
            fileNames.append((re1.text.split('<meta property="og:title" content="')[1].split('"')[0], l2[1]))

        return paths, fileNames


    def _getUrlUpload(self):
        
        res = requests.get(f"https://filemoonapi.com/api/upload/server?key=15216le6d6zs5cwsxkopi")
        js = res.json()
        return js['result']
    def _upload(self):
        urlD = srv
        res = []
        for i in range(len(self.paths)):
            print(f"  *  * Episode {self.episode} en cours d'upload!")
            with open(self.paths[i][0], 'rb') as fichier:
                post = {'key': FILEMOON_API_KEY}
                fichiers = {'file': fichier}
                crash = True
                while crash:
                    try:
                        response = requests.post(urlD, data=post, files=fichiers, stream=True)
                        crash = False
                    except:
                        urlD = getServer()
                        crash = True
                js2 = response.json()
            os.unlink(self.paths[i][0])
            res.append((js2["files"][0]["filecode"], self.paths[i][1]))
        return res
 

    def _getHost(self, l):
        if l is None:
            return None
        
        return urlparse(l[0]).netloc
    def _getDefaultL(self):
        d = "VF"
        for i in self.paths:
            if i[1] == "VOSTFR":
                d= "VOSTFR"
        return d
    def _getLink(self):
        link = {"default": self.default}

        for i in self.uploadFileCodes:
            link[i[1]] = f"https://filemoon.sx/e/" + i[0]

        return link



