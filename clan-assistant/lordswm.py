import re as regex
import requests
from lxml import html


class LWMInterface:

    NUMBER_PATTERN = regex.compile(r"[0-9]+$")

    COM_DOMAIN = "https://www.lordswm.com"
    RU_DOMAIN = "https://www.heroeswm.ru"
    DOMAIN_REGEX = r".*(?:lordswm\.com|heroeswm\.ru)\/?(.*)"
    COM_DOMAIN_REGEX = r".*lordswm\.com\/?(.*)"
    RU_DOMAIN_REGEX = r".*heroeswm\.ru\/?(.*)"
    BASE_PATTERN = regex.compile(DOMAIN_REGEX)
    COM_PATTERN = regex.compile(COM_DOMAIN_REGEX)
    RU_PATTERN = regex.compile(RU_DOMAIN_REGEX)

    PLAYER_PAGE = "pl_info.php"
    PLAYER_PAGE_NAME_XPATH = "//td[@class='wb'][1]//b[1]/text()"
    PLAYER_PAGE_CLANS_XPATH = "//table[@class='wblight'][2]//td[@class='wb']/text()"
    PLAYER_PAGE_REGEX = r".*(lordswm\.com|heroeswm\.ru)\/pl_info\.php\?(?:\w+(?:=\w+)?\&)*id=([0-9]+)"
    PLAYER_PAGE_PATTERN = regex.compile(PLAYER_PAGE_REGEX)
    PLAYER_URL_ID_PATTERN = regex.compile(r".*id=([0-9]+)")

    CLAN_PAGE = "clan_info.php"
    CLAN_PAGE_TITLE_XPATH = "//td[@class='wblight']/b[1]/text()"
    CLAN_HASH_ID_PATTERN = regex.compile(r".*#([0-9]+)")
    CLAN_TITLE_PATTERN = regex.compile(r"#([0-9]+) (.*)")

    def get_player_new(self, player):
        url, player_id = self.format_profile_url(player)
        if url is None:
            return None

        page = requests.get(url['com'])
        if page.status_code != 200:
            return None

        tree = html.fromstring(page.content)
        player_name = self.get_player_name(tree)
        if player_name is None:
            return None
        player_description = self.get_player_description(tree)
        clans = self.get_player_clans(tree)
        
        return {
            'id': player_id,
            'name': player_name,
            'description': player_description,
            'url': url,
            'clans': clans
        }

    def format_profile_url(self, player):
        url_match = self.PLAYER_PAGE_PATTERN.match(player)
        id_match = self.NUMBER_PATTERN.match(player)
        if url_match:
            player_id = url_match.group(2)
        else if id_match:
            player_id = player
        else:
            return None, None
        url = {}
        url['ru'] = f"{self.RU_DOMAIN}/{self.PLAYER_PAGE}?id={player_id}"
        url['com'] = f"{self.COM_DOMAIN}/{self.PLAYER_PAGE}?id={player_id}"
        return url, player_id

    def get_player_name(self, tree):
        return None

    def get_player_description(self, tree):
        return None

    def get_player_clans(self, tree):
        return None

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
