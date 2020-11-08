class ChannelView:

    def __init__(self):
        pass

    def to_string(self, channel):
        if channel['id'] is None:
            return ""
        category_string = ""
        channel_name = channel['name']
        if channel['category']['id'] is not None:
            category_name = channel['category']['name']
            category_string = f" in category \"{category_name}\""
        channel_string = f"\"{channel_name}\"{category_string}"
        return channel_string
