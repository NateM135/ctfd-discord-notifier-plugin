#  ctfd-discord-notifier-plugin

Inspirired by [sigpwny's plugin](https://github.com/sigpwny/ctfd-discord-webhook-plugin/tree/master) that no longer worked in ctfd version 3.5.3.

This plugin allows you to setup a discord webhook that will be used to send notifications about solves in Discord.

It works by adding a decorator to the function that handles challenge attempts. We can grab information from the request object as well as the response object to determine:

- Challenge ID (From the request)
- Submission Accuracy (From the response)
- Current Team/User (using ctfd util functions)

If a user gets the challenge correct, the challenge id can be retrieved to determine solve count, which then based on configurable options will send a customized message in Discord.

The message sent to the user is hardcoded in `src.py`. The webhook config URL as well as the threshold for notifications can be found in `config.py`.

WIP:
- Modify discord url during program execution