"""

"""

from __future__ import annotations
import royalnet.royaltyping as t

import discord
import logging
import asyncio
import royalnet.engineer as engi
import royalnet.engineer.wrench as w

from . import bullets
from .royaltyping import MsgChannel

log = logging.getLogger(__name__)


class DiscordPDA(discord.AutoShardedClient):
    def __init__(self, *args, **kwargs):
        log.debug(f"Creating new DiscordPDA")

        intents: discord.Intents
        if intents := kwargs.get("intents"):
            log.debug(f"Captured intents, force-enabling them")
            intents.guild_messages = True
            intents.dm_messages = True
        else:
            log.debug(f"No intents passed, manually selecting them")
            intents = discord.Intents.default()
            intents.guild_messages = True
            intents.dm_messages = True

        super().__init__(*args, intents=intents, **kwargs)
        self.dispensers: t.Dict[bullets.DiscordChannel, engi.Dispenser] = {}
        """
        A :class:`dict` which maps :class:`bullets.DiscordChannel`s to :class:`royalnet.engineer.dispenser.Dispenser`s.
        """

        self.conversations: t.List[t.Conversation] = []
        """
        A :class:`list` of conversations to run before a new event is :meth:`.put` in a 
        :class:`~royalnet.engineer.dispenser.Dispenser`.
        """

    @staticmethod
    async def on_shard_connect(shard_id):
        log.info(f"Shard #{shard_id} connected to Discord")

    @staticmethod
    async def on_shard_disconnect(shard_id):
        log.warning(f"Shard #{shard_id} disconnected from Discord")

    @staticmethod
    async def on_shard_ready(shard_id):
        log.info(f"Shard #{shard_id} is ready")

    @staticmethod
    async def on_shard_resumed(shard_id):
        log.info(f"Shard #{shard_id} resumed connection")

    async def on_error(self, event_method, *args, **kwargs):
        # TODO: we might want to change this behaviour
        raise

    async def on_message(self, message: discord.Message):
        log.debug(f"Received a new message: {message}")

        if message.type != discord.MessageType.default:
            log.debug(f"Ignoring message because type is: {message.type}")
            return

        bullet = bullets.DiscordMessage(_msg=message)
        channel = await bullet.channel()
        await self.put_bullet(channel=channel, bullet=bullet)

    def register_conversation(self, conv: t.Conversation) -> None:
        """
        Register a new command in the PDA.

        :param conv: The conversation to register.
        """
        log.info(f"Registering conversation: {conv}")
        self.conversations.append(conv)

    def unregister_conversation(self, conv: t.Conversation) -> None:
        """
        Unregister a command from the PDA.

        :param conv: The conversation to unregister.
        """
        log.info(f"Unregistering conversation: {conv}")
        self.conversations.remove(conv)

    async def put_bullet(self, channel: bullets.DiscordChannel, bullet: engi.Bullet) -> None:
        """
        Insert a new bullet into the dispenser corresponding to the specified channel.

        :param channel: The channel associated to the dispenser the bullet should be put in.
        :param bullet: The bullet to put in the dispenser.
        """
        log.debug(f"Finding dispenser for channel: {channel}")
        dispenser = self.dispensers.get(channel)
        if not dispenser:
            log.debug(f"Dispenser not found, creating one")
            dispenser = engi.Dispenser()
            self.dispensers[channel] = dispenser

        loop = asyncio.get_running_loop()
        for conversation in self.conversations:
            loop.create_task(dispenser.run(conversation), name=f"{repr(conversation)}")

        log.debug(f"Putting message bullet in the dispenser: {bullet}")
        await dispenser.put(bullet)
