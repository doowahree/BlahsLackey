# Intro

Very rough work of bot for the Aegis group. Anyone in Aegis Channel who wants to edit it may edit. This is deployed thru
Heroku.

Does not use off the shelf discord solution because its support was discontinued, so just using custom solution using
Discord's direct gateway apis.

Horrible code quality and barely any comments.
May add comments if I get more motivation.


# Main format for listeners
Each listener is under `/listeners` directory. All listener should
be registered inside the `Listeners.py` with an identifier.

This allows users to enable that listener on the channel by doing
`@BotId listen <identifier>`.

## Listener commands

Listener commands uses a home brewed solution because I got too lazy
to use a proper library like ANTLR or any other lexical parsing
library.

See `listeners/wordle/WordleListener.py` for example on how to use
`CommandSets` which are used to register function with string commands.