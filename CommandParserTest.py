import unittest

from CommandParser import CommandSet, Command, TokenMatcherSet, TokenMatcher


class TestObject(object):
    def __init__(self):
        self.data = {}

    def CreateFnToSet(self, key, val):
        def SetFn():
            self.SetValue(key, val)

        return SetFn

    def SetValue(self, key, val):
        print('%s: %s' % (key, val))
        self.data[key] = val


class CommandParserTest(unittest.TestCase):
    def test_something(self):
        obj = TestObject()
        cs = CommandSet(
            commands=[
                Command(
                    [obj.SetValue],
                    TokenMatcherSet(
                        [
                            TokenMatcher('bot'),
                            TokenMatcher('music', additional_args={'key': 'music show', 'val': 'empty'}),
                            TokenMatcher('show', is_optional=True, additional_args={'val': 'full'})
                        ]
                    )
                ),
                Command(
                    [obj.SetValue],
                    TokenMatcherSet(
                        [
                            TokenMatcher('bot'),
                            TokenMatcher('music'),
                            TokenMatcher('change', additional_args={'key': 'music'}),
                            TokenMatcher('.+', token_parsing=('val', str))
                        ]
                    )
                ),
                Command(
                    [obj.SetValue],
                    TokenMatcherSet(
                        [
                            TokenMatcher('bot'),
                            TokenMatcher('music', is_optional=True),
                            TokenMatcher('list', additional_args={'key': 'list'}),
                            TokenMatcher('\\d+', token_parsing=('val', int))
                        ]
                    )
                ),
            ]
        )
        cs.Apply('bot music show')
        cs.Apply('bot music')
        cs.Apply('bot music change song asdasd')
        cs.Apply('bot music list 50')
        cs.Apply('bot list 49')


if __name__ == '__main__':
    unittest.main()
