import re as regex
import requests
from lxml import html


class LWMInterface:

    NUMBER_PATTERN = regex.compile(r"[0-9]+$")

    COM_DOMAIN = "https://www.lordswm.com"
    RU_DOMAIN = "https://www.heroeswm.ru"
    DOMAIN_REGEX = r".*(?:lordswm\.com|heroeswm\.ru)\/?(.*)"
    BASE_PATTERN = regex.compile(DOMAIN_REGEX)

    PLAYER_PAGE = "pl_info.php"
    PLAYER_PAGE_NAME_XPATH = "//td[@class='wb'][1]//b[1]/text()"
    PLAYER_PAGE_CLANS_XPATH = "//table[@class='wblight'][2]//td[@class='wb']/text()"
    PLAYER_URL_ID_PATTERN = regex.compile(r".*id=([0-9]+)")

    CLAN_PAGE = "clan_info.php"
    CLAN_PAGE_TITLE_XPATH = "//td[@class='wblight']/b[1]/text()"
    CLAN_HASH_ID_PATTERN = regex.compile(r".*#([0-9]+)")
    CLAN_TITLE_PATTERN = regex.compile(r"#([0-9]+) (.*)")

    def __init__(self):
        self.clans = {}

    def get_player(self, player):
        if LWMInterface.NUMBER_PATTERN.match(player):
            url = self.add_query(
                    f"{LWMInterface.COM_DOMAIN}/{LWMInterface.PLAYER_PAGE}",
                    'id',
                    player)
        else:
            url = player
        if not url.startswith("http"):
            url = "https://" + url
        page = requests.get(url)
        if page.status_code != 200:
            return None

        tree = html.fromstring(page.content)
        name = tree.xpath(LWMInterface.PLAYER_PAGE_NAME_XPATH)
        clans = tree.xpath(LWMInterface.PLAYER_PAGE_CLANS_XPATH)
        if len(name) >= 1:
            name = repr(name[0]).split("\\")[0].strip("'")
        else:
            return None
        clan_ids = []
        for text in clans:
            match = LWMInterface.CLAN_HASH_ID_PATTERN.match(text)
            if match:
                clan_ids.append(match.group(1))
        player_id = LWMInterface.PLAYER_URL_ID_PATTERN.match(url).group(1)
        print(player_id)
        print(name)
        print(clan_ids)
        return {'id': player_id, 'name': name, 'clan_ids': clan_ids}

    def get_clan(self, clan):
        if LWMInterface.NUMBER_PATTERN.match(clan):
            url = self.add_query(
                    f"{LWMInterface.COM_DOMAIN}/{LWMInterface.CLAN_PAGE}",
                    'id',
                    clan)
        else:
            url = clan
        if not url.startswith("http"):
            url = "https://" + url
        page = requests.get(url)
        if page.status_code != 200:
            return None

        tree = html.fromstring(page.content)
        title = tree.xpath(LWMInterface.CLAN_PAGE_TITLE_XPATH)
        if len(title) == 1:
            title = title[0]
        else:
            return None
        match = LWMInterface.CLAN_TITLE_PATTERN.match(title)
        clan_id = match.group(1)
        clan_name = match.group(2)
        return {
                'id': clan_id,
                'name': clan_name,
                'qualified_name': f"#{clan_id} {clan_name}",
                'url': {
                        'com': self.add_query(
                                f"{LWMInterface.COM_DOMAIN}/{LWMInterface.CLAN_PAGE}",
                                'id',
                                clan_id),
                        'ru': self.add_query(
                                f"{LWMInterface.RU_DOMAIN}/{LWMInterface.CLAN_PAGE}",
                                'id',
                                clan_id)}}

    def get_clan_url(self, clan_id):
        return {
                'ru': "",
                'com': ""}

    def add_query(self, base:str, key:str, value):
        connector = "&"
        if base[-3:] == "php":
            connector = "?"
        return f"{base}{connector}{key}={str(value)}"
