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
    QUERY_STRING_ID_REGEX = r".*id=([0-9]+)"
    BASE_PATTERN = regex.compile(DOMAIN_REGEX)
    COM_PATTERN = regex.compile(COM_DOMAIN_REGEX)
    RU_PATTERN = regex.compile(RU_DOMAIN_REGEX)
    QUERY_STRING_ID_PATTERN = regex.compile(QUERY_STRING_ID_REGEX)

    PLAYER_PAGE = "pl_info.php"
    PLAYER_PAGE_REGEX = r".*(lordswm\.com|heroeswm\.ru)\/pl_info\.php\?(?:\w+(?:=\w+)?\&)*id=([0-9]+)"
    PLAYER_PAGE_PATTERN = regex.compile(PLAYER_PAGE_REGEX)
    PLAYER_PAGE_NAME_PLATE_XPATH = "//table[@class='wblight'][1]/descendant::td[@class='wb'][1]//b[1]/text()"
    PLAYER_PAGE_DESCRIPTION_XPATH = "//center/table[2]//table[@class='wblight'][last()]//tr[last()]/td//text()"
    PLAYER_PAGE_CLANS_XPATH = "//table[@class='wblight'][2]//following-sibling::tr[//b/text() = 'Clans']//td/a"

    CLAN_PAGE = "clan_info.php"
    CLAN_PAGE_REGEX = r".*(lordswm\.com|heroeswm\.ru)\/clan_info\.php\?(?:\w+(?:=\w+)?\&)*id=([0-9]+)"
    CLAN_PAGE_PATTERN = regex.compile(CLAN_PAGE_REGEX)
    CLAN_PAGE_NAME_PLATE_XPATH = "//td[@class='wblight']/b[1]/text()"
    CLAN_PAGE_DESCRIPTION_XPATH = "(//center/table[2]//table[@class='wb'][1]//td[@class='wbwhite'])[last()]//text()"
    CLAN_PAGE_MEMBERS_XPATH = "(//table[@class='wb'])[last()]//tr"

    CLAN_PAGE_TITLE_XPATH = "//td[@class='wblight']/b[1]/text()"
    CLAN_HASH_ID_PATTERN = regex.compile(r".*#([0-9]+)")
    CLAN_TITLE_PATTERN = regex.compile(r"#([0-9]+) (.*)")

    def get_player_new(self, player):
        url, player_id = self.format_profile_url(player)
        if url is None:
            return None

        page = requests.get(url['com'], headers=self.REQUEST_HEADER)
        if page.status_code != 200:
            return None

        tree = html.fromstring(page.content)
        player_name = self.get_player_name(tree)
        if player_name is None:
            return None
        player_level = self.get_player_level(tree)
        player_description = self.get_player_description(tree)
        clans = self.get_player_clans(tree)
        
        return {
            'id': player_id,
            'name': player_name,
            'level': player_level,
            'description': player_description,
            'url': url,
            'clans': clans}

    def get_clan_new(self, clan):
        url, clan_id = self.format_clan_url(clan)
        if url is None:
            return None

        page = requests.get(url['com'], headers=self.REQUEST_HEADER)
        if page.status_code != 200:
            return None

        tree = html.fromstring(page.content)
        clan_name = self.get_clan_name(tree)
        if clan_name is None:
            return None
        clan_description = self.get_clan_description(tree)
        members = self.get_clan_members(tree)

        return {
                'id': clan_id,
                'name': clan_name,
                'description': clan_description,
                'url': url,
                'members': members}

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

    def format_clan_url(self, clan):
        url_match = self.CLAN_PAGE_PATTERN.match(str(clan))
        id_match = self.NUMBER_PATTERN.match(str(clan))
        if url_match:
            clan_id = url_match.group(2)
        elif id_match:
            clan_id = clan
        else:
            return None, None
        url = {}
        url['ru'] = f"{self.RU_DOMAIN}/{self.CLAN_PAGE}?id={clan_id}"
        url['com'] = f"{self.COM_DOMAIN}/{self.CLAN_PAGE}?id={clan_id}"
        return url, clan_id

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
        clan_links = tree.xpath(self.PLAYER_PAGE_CLANS_XPATH)
        clans = []
        for link in clan_links:
            clan_name = link.findtext('b')
            clan_page = link.get('href')
            clan_id = self.QUERY_STRING_ID_PATTERN.match(clan_page).group(1)
            url = {}
            url['ru'] = f"{self.RU_DOMAIN}/{clan_page}"
            url['com'] = f"{self.COM_DOMAIN}/{clan_page}"
            clan = {
                    'id': clan_id,
                    'name': clan_name,
                    'url': url}
            clans.append(clan)
        return clans

    def get_clan_name(self, tree):
        name_plate = self.get_clan_name_plate(tree)
        if not name_plate:
            return None
        name = name_plate.split(' ', 1)[1]
        return name

    def get_clan_name_plate(self, tree):
        name_plate = tree.xpath(self.CLAN_PAGE_NAME_PLATE_XPATH)
        if len(name_plate) == 0:
            return None
        return name_plate[0]

    def get_clan_description(self, tree):
        description = tree.xpath(self.CLAN_PAGE_DESCRIPTION_XPATH)
        if len(description) == 0:
            return None
        return '\n'.join(description)

    def get_clan_members(self, tree):
        member_rows = tree.xpath(self.CLAN_PAGE_MEMBERS_XPATH)
        members = []
        for row in member_rows:
            row_items = row.getchildren()
            order = row_items[0].text.split('.')[0]
            name_plate = row_items[2].getchildren()[-2]
            name = name_plate.text
            profile_page = name_plate.get('href')
            member_id = self.QUERY_STRING_ID_PATTERN.match(profile_page).group(1)
            level = row_items[3].text
            description = row_items[4].text.strip()
            event_points = None
            event_status = None
            if len(row_items) == 6:
                event_element = row_items[5].getchildren()
                if len(event_element) > 0:
                    event_element = event_element[0]
                    event_status = event_element.get('color')
                    if event_status == 'green':
                        event_points = event_element.text
                    else:
                        event_points = event_element.findtext('b')
                else:
                    event_points = 0
                    event_status = 'green'
            url = {}
            url['ru'] = f"{self.RU_DOMAIN}/{profile_page}"
            url['com'] = f"{self.COM_DOMAIN}/{profile_page}"
            
            member = {
                    'clan_order': order,
                    'id': member_id,
                    'name': name,
                    'level': level,
                    'description': description,
                    'event_points': event_points,
                    'event_status': event_status,
                    'url': url}
            members.append(member)
        return members

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
    # li.get_player_new(4874384)
    # li.get_player_new(8464564564848454646)
    # li.get_player_new(545081)
    # li.get_player_new(4366341)
    # li.get_player_new(45644)
    li.get_clan_new(7440)
    li.get_clan_new(1271)
