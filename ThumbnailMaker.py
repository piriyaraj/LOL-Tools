from io import BytesIO
from PIL import Image
import os
import random
from time import sleep

import requests
from data_scrapper import DataScrapper
from match_data import MatchData
from progress import print_progress
from bs4 import BeautifulSoup

from scrap_lol_data import ScrapLolData

def change_champion_name(champion):
    champion = champion.replace("'", "& ")
    champion = champion.replace("&", "")
    if (len(champion.split()) == 2):
        champion = champion.replace(" ", "-")
    
    champion = champion.replace(" ", "").lower()

    return champion

def iconReplace(champion):
    name = champion.replace(" ","")
    name = name.replace("'","")
    if (name == "KaiSa"):
        return "Kaisa"
    elif (name == "VelKoz"):
        return "Velkoz"
    elif (name == "KhaZix"):
        return "Khazix"
    elif (name == "NunuWillump"):
        return "Nunu"
    elif (name == "BelVeth"):
        return "Belveth"
    elif (name == "RenataGlasc"):
        return "Renata"
    elif (name == "RekSai"):
        return "RekSai"
    elif (name == "Wukong"):
        return "MonkeyKing"
    elif (name == "Dr.Mundo"):
        return "DrMundo"
    else:
        return name

class CreateThumbnail:
    def __init__(self, driver, data: MatchData) -> None:
        self.driver = driver
        self.lol_data = data
        self.__thumb_path = os.path.abspath(r'../media/thumb/thumb.png')
        os.makedirs('../media/thumb', exist_ok=True)
        # print_progress(1, 100, prefix='Creating Thumbnail:')
        self.skins = {
            "Yuumi": [0, 1, 11, 19, 28, 37, 39],
        }

    def exceptionHandle(self, name):
        if (name == "KaiSa"):
            return "Kai-sa"
        elif (name == "VelKoz"):
            return "vel-koz"
        elif (name == "KhaZix"):
            return "kha-zix"
        elif (name == "NunuWillump"):
            return "Nunu"
        elif (name == "BelVeth"):
            return "bel-veth"
        elif (name == "RenataGlasc"):
            return "Renata"
        elif (name == "TwistedFate"):
            return "Twisted-fate"
        elif (name == "LeeSin"):
            return "lee-sin"
        elif (name == "RekSai"):
            return "rek-sai"
        elif (name == "K'Sante"):
            return "k-sante"
        elif (name == "KogMaw"):
            return "Kog-maw"
        elif (name == "JarvanIV"):
            return "jarvan-iv"
        elif (name == "MasterYi"):
            return "Master-yi"
        elif (name == "Dr.Mundo"):
            return "dr-mundo"
        elif (name == "Dr.Mundo"):
            return "dr-mundo"
        elif (name == "Nidalee"):
            return "nidalee"
        elif (name == "Evelynn"):
            return "evelynn"
        else:
            return name

    def getSkin(self, name):
        # url = "https://www.leagueoflegends.com/en-gb/champions/{name}/"
        # make get request and use beautifulsoup and find the skin img urls
        url = "https://www.leagueoflegends.com/en-gb/champions/{}/".format(
            name)
        # print(url)
        r = requests.get(url)
        # if r.status_code is '404':
        #     url = "https://www.leagueoflegends.com/en-pl/champions/{}/".format(name)
        #     r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        skinsImgTag = soup.find_all('img')
        skinsUrls = list(set([skin.get('src') for skin in skinsImgTag]))
        filtered_urls = [
            skinUrl for skinUrl in skinsUrls if skinUrl is not None and "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/" in skinUrl]
        
        return filtered_urls
    
    def all_champion(self):
        champions = []
        kda = []
        name = []
        rank = []
        spell = []
        for player in self.lol_data['team1']['players']:
            champions.append(player['champion'])
            kda.append(player['kda'])
            name.append(player['name'])
            rank.append(player['rank'])
            spell.append(player['spell'])
        for player in self.lol_data['team2']['players']:
            champions.append(player['champion'])
            kda.append(player['kda'])
            name.append(player['name'])
            rank.append(player['rank'])
            spell.append(player['spell'])
        
        for index, player in enumerate(champions):
            print(f"{index} : {player}")
        
        selection = int(input("Enter the players number:"))
        positionLOL = ['TOP',"JUG","MID","ADC","SUP"][selection%5]
        loserPosition = selection+5 if selection<5 else selection-5
        loser = champions[loserPosition]
        return champions[selection], positionLOL, loser ,kda[selection], name[selection], rank[selection], spell[selection]
    
    def create_thumbnail(self):
        champion, positionLOL, loser, kda, name, rank, spell = self.all_champion()
        # exit()
        print_progress(5, 100, prefix='Creating Thumbnail:')
        # champion = self.lol_data['mvp']['champion']
        championRaw = champion
        champion = change_champion_name(champion)
        
        championTemp = champion
        champion = self.exceptionHandle(champion)
        print_progress(8, 100, prefix='Creating Thumbnail:')
        # if champion=="KaiSa":
        #     champion=="Kaisa"
        ranks = {
            "Iron": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/1.png",
            "Bronze": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/2.png",
            "Silver": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/3.png",
            "Gold": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/4.png",
            "Platinum": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/5.png",
            "Diamond": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/6.png",
            "Master": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/7.png",
            "GrandMaster": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/8.png",
            "Challenger": "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/9.png"
        }
        print_progress(12, 100, prefix='Creating Thumbnail:')
        rankIcon = ranks.get(rank)
        if (rankIcon is None):
            rankIcon = "https://lolg-cdn.porofessor.gg/img/s/league-icons-v3/160/9.png"
        spellImgs = os.listdir("assets/img/spell")
        print_progress(19, 100, prefix='Creating Thumbnail:')
        spellImg = random.sample(spellImgs, 3)
        spellImgNew = spell
        spellImgNew = [s+'.png' for s in spellImgNew]
        spellImg = spellImgNew
        print_progress(25, 100, prefix='Creating Thumbnail:')

        # loser = self.lol_data['loser']
        imgUrl = ""
        count = 0
        # print(champion)
        # print("match region:",self.lol_data['region'],os.path.exists(f"assets/img/{self.lol_data['region']}.png"))
        if (os.path.exists(f"assets/img/{self.lol_data['region']}.png")):
            region = self.lol_data['region']
        else:
            region = "EUW"
        # print(champion)
        skins = self.getSkin(champion)
        # print(skins)
        if (len(skins) == 0):
            print("\n==> Thumbnail creation failed \n==> Sent message to developer!\n==> Take a screenshot and sent mail to : tamilcomway@gmail.com")
            # print("==> Champion Temp: " + champonTemp)
            print("==> Champion name: " + str(champion))
            print("==> Raw Champion name: " + str(championRaw))
            print("==> URL:", imgUrl)
            return False
        imgUrl = random.choice(skins)

        print_progress(40, 100, prefix='Creating Thumbnail:')
        oppIconImg = iconReplace(championRaw)
        loserIcon = iconReplace(loser)
        # print(f"https://opgg-static.akamaized.net/meta/images/lol/14.11.1/champion/{loserIcon}.png'")
        self.__create_html(
            kda=kda.split("/"),
            imgUrl=imgUrl,
            mvp=name,
            vs=loser,
            rank=rank.upper(),
            patch=self.lol_data['patch'],
            rankIcon=rankIcon,
            spellImg=spellImg,
            opponentIcon=f'https://opgg-static.akamaized.net/meta/images/lol/14.11.1/champion/{oppIconImg}.png',
            region=region,
            loserIcon=f'https://opgg-static.akamaized.net/meta/images/lol/14.11.1/champion/{loserIcon}.png',
            positionLOL = positionLOL
        )
        print_progress(50, 100, prefix='Creating Thumbnail:')
        html_path = os.path.abspath('assets/thumbnail.html')
        self.driver.get('file://' + html_path)
        timer = 51
        for i in range(10):
            sleep(0.5)
            print_progress(timer+i*2, 100, prefix='Creating Thumbnail:')
        self.driver.set_window_size(1280, 805)
        print_progress(81, 100, prefix='Creating Thumbnail:')
        screenshot = self.driver.get_screenshot_as_png()
        print_progress(91, 100, prefix='Creating Thumbnail:')
        with Image.open(BytesIO(screenshot)) as img:
            img = img.convert('RGB')
            img = img.resize((1280, 720))
            img.save(self.__thumb_path, quality=70)
            # img.save(self.__static_thumb_path, quality=70)
        print_progress(100, 100, prefix='Creating Thumbnail:')

        self.driver.quit()
        return True

    def __create_html(self, kda: str, mvp: str, vs: str, rank: str, patch: str, imgUrl: str, rankIcon: str, spellImg: list, opponentIcon: str, region, loserIcon, positionLOL):
        none_vars = []
        if kda is None:
            none_vars.append('kda')
        if mvp is None:
            none_vars.append('mvp')
        if vs is None:
            none_vars.append('vs')
        if rank is None:
            none_vars.append('rank')
        if patch is None:
            none_vars.append('patch')
        if imgUrl is None:
            none_vars.append('imgUrl')
        if rankIcon is None:
            none_vars.append('rankIcon')
        if spellImg is None:
            none_vars.append('spellImg')
        if none_vars:
            # print(f"One or more arguments are None: {', '.join(none_vars)}")
            return
        with open("./assets/template_new.html", "r", encoding='utf-8') as f:
            HTML = f.read()
            # print(HTML)
        
        HTML = HTML.replace("backgroundImageLOL", imgUrl.replace("'", ""))
        HTML = HTML.replace("positionLOL", positionLOL)
        HTML = HTML.replace("rankIconLOL", rankIcon)
        HTML = HTML.replace("loserIconLOL", loserIcon)
        HTML = HTML.replace("opponentIconLOL", opponentIcon)
        HTML = HTML.replace("patchLOL", patch)
        HTML = HTML.replace("rankLOL", rank)
        HTML = HTML.replace("regionLOL", region)
        HTML = HTML.replace("spellImg0LOL", spellImg[0])
        HTML = HTML.replace("spellImg1LOL", spellImg[1])
        HTML = HTML.replace("spellImg2LOL", spellImg[2])
        HTML = HTML.replace("mvpLOL", mvp)
        HTML = HTML.replace("kda0LOL", kda[0])
        HTML = HTML.replace("kda1LOL", kda[1])
        HTML = HTML.replace("kda2LOL", kda[2])

        with open("./assets/thumbnail.html", "w", encoding='utf-8') as f:
            f.write(HTML)

def test(link_list):
    for match_url in link_list:
        lol_data_scrapper = ScrapLolData()
        driver = lol_data_scrapper.get_match_data_and_download_replay(match_url)
        from data import load
        lol_data: MatchData = load()
        thumb_creator = CreateThumbnail(driver, data=lol_data)
        thumb_creator.create_thumbnail()
        driver.quit()
    
def run():
    match_url = input("Enter Match URL: ")
    lol_data_scrapper = ScrapLolData()
    driver = lol_data_scrapper.get_driver()
    driver = lol_data_scrapper.get_match_data_and_download_replay(match_url)
    from data import load
    lol_data: MatchData = load()
    thumb_creator = CreateThumbnail(driver, data=lol_data)
    thumb_creator.create_thumbnail()
    # driver.quit()
    
link_list = [
    # 'https://www.leagueofgraphs.com/match/na/5011563933',
    # 'https://www.leagueofgraphs.com/match/br/2946190822',
    'https://www.leagueofgraphs.com/match/euw/6961124219',
    # 'https://www.leagueofgraphs.com/match/na/5011537333',
    # 'https://www.leagueofgraphs.com/match/na/5011534961',
    # 'https://www.leagueofgraphs.com/match/br/2946173053'
]

    
def getSkin(name):
    # url = "https://www.leagueoflegends.com/en-gb/champions/{name}/"
    # make get request and use beautifulsoup and find the skin img urls
    url = "https://www.leagueoflegends.com/en-gb/champions/{}/".format(
        name)
    # print(url)
    r = requests.get(url)
    # if r.status_code is '404':
    #     url = "https://www.leagueoflegends.com/en-pl/champions/{}/".format(name)
    #     r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    skinsImgTag = soup.find_all('img')
    skinsUrls = list(set([skin.get('src') for skin in skinsImgTag]))
    filtered_urls = [
        skinUrl for skinUrl in skinsUrls if skinUrl is not None and "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/" in skinUrl]
    
    return filtered_urls


def get_icon(champion):
    print(f'https://opgg-static.akamaized.net/meta/images/lol/champion/{champion}.png')
    
if __name__ == "__main__":
    run()