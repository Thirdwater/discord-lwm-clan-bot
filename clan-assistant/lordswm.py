import re as regex
import requests
from lxml import html


class LWMInterface:

    NUMBER_PATTERN = regex.compile(r"[0-9]+$")
    REQUEST_HEADER = {'User-Agent': "Mozilla/5.0"}

    COM_DOMAIN = "https://www.lordswm.com"
    RU_DOMAIN = "https://www.heroeswm.ru"
    DOMAIN_REGEX = r".*(?:lordswm\.com|heroeswm\.ru)\/?(.*)"
    COM_DOMAIN_REGEX = r".*lordswm\.com\/?(.*)"
    RU_DOMAIN_REGEX = r".*heroeswm\.ru\/?(.*)"
    BASE_PATTERN = regex.compile(DOMAIN_REGEX)
    COM_PATTERN = regex.compile(COM_DOMAIN_REGEX)
    RU_PATTERN = regex.compile(RU_DOMAIN_REGEX)

    PLAYER_PAGE = "pl_info.php"
    PLAYER_PAGE_REGEX = r".*(lordswm\.com|heroeswm\.ru)\/pl_info\.php\?(?:\w+(?:=\w+)?\&)*id=([0-9]+)"
    PLAYER_PAGE_PATTERN = regex.compile(PLAYER_PAGE_REGEX)
    PLAYER_PAGE_NAME_PLATE_XPATH = "//table[@class='wblight'][1]/descendant::td[@class='wb'][1]//b[1]/text()"
    PLAYER_PAGE_DESCRIPTION_XPATH = "//center/table[2]//table[@class='wblight'][last()]//tr[last()]/td//text()"
    PLAYER_PAGE_CLANS_XPATH = "//table[@class='wblight'][2]//td[@class='wb']/text()"

    CLAN_PAGE = "clan_info.php"
    CLAN_PAGE_TITLE_XPATH = "//td[@class='wblight']/b[1]/text()"
    CLAN_HASH_ID_PATTERN = regex.compile(r".*#([0-9]+)")
    CLAN_TITLE_PATTERN = regex.compile(r"#([0-9]+) (.*)")

    def get_player_new(self, player):
        url, player_id = self.format_profile_url(player)
        print("URL: " + str(url))
        if url is None:
            return None

        page = requests.get(url['com'], headers=self.REQUEST_HEADER)
        print("Status code: " + str(page.status_code))
        if page.status_code != 200:
            return None

        tree = html.fromstring(page.content)
        player_name = self.get_player_name(tree)
        print("Player name: " + str(player_name))
        if player_name is None:
            return None
        player_level = self.get_player_level(tree)
        print("Player level: " + str(player_level))
        player_description = self.get_player_description(tree)
        print("Player description: " + str(player_description))
        clans = self.get_player_clans(tree)
        
        return {
            'id': player_id,
            'name': player_name,
            'level': player_level,
            'description': player_description,
            'url': url,
            'clans': clans
        }

    def format_profile_url(self, player):
        url_match = self.PLAYER_PAGE_PATTERN.match(str(player))
        id_match = self.NUMBER_PATTERN.match(str(player))
        if url_match:
            player_id = url_match.group(2)
        elif id_match:
            player_id = player
        else:
            return None, None
        url = {}
        url['ru'] = f"{self.RU_DOMAIN}/{self.PLAYER_PAGE}?id={player_id}"
        url['com'] = f"{self.COM_DOMAIN}/{self.PLAYER_PAGE}?id={player_id}"
        return url, player_id

    def get_player_name(self, tree):
        name_plate = self.get_player_name_plate(tree)
        if not name_plate:
            return None
        name = name_plate.split('[')[0].strip()
        return name

    def get_player_level(self, tree):
        name_plate = self.get_player_name_plate(tree)
        if not name_plate:
            return None
        level = name_plate.split('[')[1].split(']')[0]
        return level

    def get_player_name_plate(self, tree):
        name_plate = tree.xpath(self.PLAYER_PAGE_NAME_PLATE_XPATH)
        if len(name_plate) == 0:
            return None
        return name_plate[0]

    def get_player_description(self, tree):
        description = tree.xpath(self.PLAYER_PAGE_DESCRIPTION_XPATH)
        if len(description) == 0:
            return None
        return '\n'.join(description)

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

if __name__ == '__main__':
    li = LWMInterface()
    li.get_player_new(4874384)
    li.get_player_new(8464564564848454646)
    li.get_player_new(545081)
    li.get_player_new(4366341)
