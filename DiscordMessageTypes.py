from enum import Enum
from traceback import print_exc
from typing import Dict, List

from attr import define, asdict


@define
class User(object):
    username: str
    id: str
    bot: bool = False


class DiscordEmoji(Enum):
    """
    Freaking discord uses actual emoji codes instead of string text ffs....
    """
    x = '❌'
    o = '⭕'
    num_1 = '1️⃣'
    num_2 = '2️⃣'
    num_3 = '3️⃣'
    num_4 = '4️⃣'
    num_5 = '5️⃣'
    num_6 = '6️⃣'
    num_7 = '7️⃣'
    num_8 = '8️⃣'
    num_9 = '9️⃣'
    symbol_exclamation = '❗'
    symbol_question = '❓'
    symbol_exquestion = '⁉️'
    symbol_nope = '🚫'
    symbol_warning = '⚠️'
    symbol_ok = '👌'
    symbol_anger = '💢'
    symbol_perfect = '💯'
    symbol_dizzy = '💫'
    symbol_sweat = '💦'

    @staticmethod
    def GetNumber(num: int):
        """Manually generated"""
        if num == 1:
            return DiscordEmoji.num_1
        elif num == 2:
            return DiscordEmoji.num_2
        elif num == 3:
            return DiscordEmoji.num_3
        elif num == 4:
            return DiscordEmoji.num_4
        elif num == 5:
            return DiscordEmoji.num_5
        elif num == 6:
            return DiscordEmoji.num_6
        elif num == 7:
            return DiscordEmoji.num_7
        elif num == 8:
            return DiscordEmoji.num_8
        elif num == 9:
            return DiscordEmoji.num_9
        return DiscordEmoji.symbol_dizzy


class MessageCreate(object):
    def __init__(self, content: Dict):
        self.content: str = content['d']['content']
        self.mentions: List[User] = [User(d['username'], d['id'], d.get('bot', False)) for d in
                                     content['d']['mentions']]
        self.channel_id: str = content['d']['channel_id']
        self.guild_id: str = content['d']['guild_id']
        self.id: str = content['d']['id']

        author = content['d']['author']
        self.author: User = User(author['username'], author['id'], author.get('bot', False))
