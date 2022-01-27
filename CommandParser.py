import re
from re import Pattern
from typing import Union, Callable, Tuple, Dict, Any, List


class TokenMatcher(object):
    def __init__(self, pattern: Union[str, Pattern], token_parsing: Tuple[str, Callable] = None,
                 additional_args: Dict = None,
                 is_optional: bool = False, descriptor: str = ''):
        if type(pattern) == str:
            pattern = re.compile(pattern)
        self.pattern: Pattern = pattern
        self.token_parsing: Tuple[str, Callable] = token_parsing
        self.is_optional: bool = is_optional
        self.descriptor: str = descriptor
        self.additional_args = additional_args or {}

    def try_match(self, text: str, arg_holder: Dict[str, Any]) -> Tuple[bool, str]:
        matcher = self.pattern.match(text)
        if matcher:
            matched_item = matcher.group(0)
            if self.token_parsing:
                arg_holder[self.token_parsing[0]] = self.token_parsing[1](matched_item)
            if self.additional_args:
                arg_holder.update(self.additional_args)
            remaining_text = text[matcher.end():].strip()
            return True, remaining_text
        else:
            if self.is_optional:
                return True, text
            else:
                return False, text


class TokenMatcherSet(object):
    def __init__(self, matchers: List[TokenMatcher]):
        self.matchers: List[TokenMatcher] = matchers

    def is_satisfied(self, text: str) -> Tuple[bool, Dict[str, Any], str]:
        possible_arg_holder = {}
        remaining_text = text.strip()
        for matcher in self.matchers:
            matched, remaining_text = matcher.try_match(remaining_text, possible_arg_holder)
            if not matched:
                return False, {}, text
        return True, possible_arg_holder, remaining_text


class Command(object):
    def __init__(self, commands: List[Callable], *matcher_set):
        self.commands: List[Callable] = commands
        self.matcher_sets: List[TokenMatcherSet] = matcher_set

    def is_eligible(self, text: str) -> Tuple[bool, Dict[str, Any], str]:
        smallest = (False, {}, text)
        for matcher_set in self.matcher_sets:
            matched, args, remaining_text = matcher_set.is_satisfied(text)
            if matched and len(remaining_text) < len(smallest[2]):
                smallest = (matched, args, remaining_text)
        return smallest


class CommandSet(object):
    """Very crappy attempt at serial token parsing and function caller.

    Context: Rolled out my own because the time it takes to learn a prebuilt library exceeds rolling one out.
    Replace with antlr or some other elegant lexical parsing algorithms or something.
    """
    def __init__(self, commands: List[Command]):
        self.commands = commands

    def Apply(self, text: str, additional_args: Dict = None):
        additional_args = additional_args or {}
        eligible_commands: List[Tuple[Command, Dict, str]] = []
        for command in self.commands:
            matched, args, remaining_text = command.is_eligible(text)
            if matched:
                eligible_commands.append((command, args, remaining_text))

        if eligible_commands:
            eligible_commands.sort(key=lambda x: len(x[2]))
            command, args, _ = eligible_commands[0]
            args.update(additional_args)
            for command in command.commands:
                command(**args)
