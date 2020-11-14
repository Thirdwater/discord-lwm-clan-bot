from discord.ext import commands


class ChannelController(commands.Cog):

    def __init__(self, bot, model, view):
        self.bot = bot
        self.model = model
        self.view = view

    async def log_to_output(self, message):
        channel_model = await self.model.persistence.get_output_channel()
        if channel_model['id'] is None:
            return
        channel = self.bot.get_channel(channel_model['id'])
        await channel.send(message)

    @commands.group(name='channel', invoke_without_command=True)
    @commands.has_permissions(manage_channels=True)
    async def channel(self, context):
        await context.send_help(context.command)

    @channel.command(name='set-verification')
    @commands.has_permissions(manage_channels=True)
    async def set_verification_channel(self, context):
        "Assigns the channel for member verification"
        channel = self.get_channel_from_context(context)
        channel_string = self.view.channel.to_string(channel)
        previous_channel = await self.model.persistence.get_verification_channel()
        previous_channel_string = self.view.channel.to_string(previous_channel)
        previous_string = f" (was previously {previous_channel_string})"
        if previous_channel_string == "":
            previous_string = ""
        if self.is_same_channel(channel, previous_channel):
            await context.send(f"Verification channel has already been set to {channel_string}.")
            return
        await self.model.persistence.set_verification_channel(channel)
        await self.model.persistence.save_config()
        await context.send(f"Verification channel has been set to {channel_string}{previous_string}.")
        await self.log_to_output(
                f"{context.message.author.display_name} set the verification channel to {channel_string}{previous_string}.")

    @channel.command(name='get-verification')
    @commands.has_permissions(manage_channels=True)
    async def get_verification_channel(self, context):
        "Displays the channel assigned for member verification"
        channel = await self.model.persistence.get_verification_channel()
        if channel['id'] is None:
            await context.send("Verification channel has not been set.")
            await context.send_help(self.bot.get_command('channel set-verification'))
            return
        channel_string = self.view.channel.to_string(channel)
        await context.send(f"Verification channel is {channel_string}.")

    @channel.command(name='set-output')
    @commands.has_permissions(manage_channels=True)
    async def set_output_channel(self, context):
        "Assigns the channel to log bot outputs"
        channel = self.get_channel_from_context(context)
        channel_string = self.view.channel.to_string(channel)
        previous_channel = await self.model.persistence.get_output_channel()
        previous_channel_string = self.view.channel.to_string(previous_channel)
        previous_string = f" (was previously {previous_channel_string})"
        if previous_channel_string == "":
            previous_string = ""
        if self.is_same_channel(channel, previous_channel):
            await context.send(f"Output channel has already been set to {channel_string}.")
            return
        await self.model.persistence.set_output_channel(channel)
        await self.model.persistence.save_config()
        await context.send(f"Output channel has been set to {channel_string}{previous_string}.")
        await self.log_to_output(
                f"{context.message.author.display_name} set the output channel to {channel_string}{previous_string}.")

    @channel.command(name='get-output')
    @commands.has_permissions(manage_channels=True)
    async def get_output_channel(self, context):
        "Displays the channel assigned to log bot outputs"
        channel = await self.model.persistence.get_output_channel()
        if channel['id'] is None:
            await context.send("Output channel has not been set.")
            await context.send_help(self.bot.get_command('channel set-output'))
            return
        channel_string = self.view.channel.to_string(channel)
        await context.send(f"Output channel is {channel_string}.")

    @channel.error
    @set_verification_channel.error
    @get_verification_channel.error
    @set_output_channel.error
    @get_output_channel.error
    async def command_errors(self, context, error):
        # Normal users don't need to know that these commands exist.
        pass

    def get_channel_from_context(self, context):
        channel = context.channel
        category = self.bot.get_channel(channel.category_id)
        category_id = None
        category_name = None
        if category is not None:
            category_id = category.id
            category_name = category.name
        channel_model = {
                'id': channel.id,
                'name': channel.name,
                'category': {
                        'id': category_id,
                        'name': category_name}}
        return channel_model

    def is_same_channel(self, channel1, channel2):
        channel1_id = channel1['id']
        channel2_id = channel2['id']
        category1_id = channel1['category']['id']
        category2_id = channel2['category']['id']
        same_channel = channel1_id == channel2_id
        same_category = category1_id == category1_id
        return same_channel and same_category
