class ChannelView:

    def __init__(self):
        pass

    def to_string(self, channel):
        category_string = ""
        channel_name = channel['name']
        if channel['category']['id'] is not None:
            category_name = channel['category']['name']
            category_string = " in category \"{category_name}\""
        channel_string = "\"{channel_name}\"{category_string}"
        return channel_string
