import requests


def getEpisode(saisonLink):
    saisonVostfr = requests.get(saisonLink.replace("vf", "vostfr"))
    saisonVf = requests.get(saisonLink.replace("vostfr", "vf"))
    VfEpisode = []
    VostFrEpisode = []

    try:
        VfEpRequest = requests.get( saisonVf.url + "episodes.js?filever="+ saisonVf.text.split("src='episodes.js?filever=")[1].split("'")[0] )
        for x in VfEpRequest.text.split(";")[:-1]:
            try:
                if "sibnet" in x.split("[")[1].split("]")[0] or "vk" in x.split("[")[1].split("]")[0]:
                    urls = x.split("[")[1].split("]")[0]
                    for v in urls.split(","):
                        if v == "": continue

                        VfEpisode.append(v.replace("'", "").replace("'", "").replace("\n", "").replace("\t", "").replace("\r", ""))
                    break
            except Exception:
                pass
    except Exception:
        pass
    try:
        VostfrEpRequest = requests.get( saisonVostfr.url + "episodes.js?filever="+ saisonVostfr.text.split("src='episodes.js?filever=")[1].split("'")[0] )
        for x in VostfrEpRequest.text.split(";")[:-1]:
            try:
                if "sibnet" in x.split("[")[1].split("]")[0] or "vk" in x.split("[")[1].split("]")[0]:
                    urls = x.split("[")[1].split("]")[0]
                    for v in urls.split(","):
                        if v == "": continue
                        VostFrEpisode.append(v.replace("'", "").replace("'", "").replace("\n", "").replace("\t", "").replace("\r", ""))
                    break
            except Exception:
                pass
    except Exception:
        pass

    results = []
    for i in range(max(len(VostFrEpisode), len(VfEpisode))):
        episodeArray = []
        try:
            ep = VostFrEpisode[i]
            episodeArray.append((ep, "VOSTFR"))
        except Exception:
            pass

        try:
            ep = VfEpisode[i]
            episodeArray.append((ep, "VF"))
        except Exception:
            pass
        results.append(episodeArray)

    return results
        

