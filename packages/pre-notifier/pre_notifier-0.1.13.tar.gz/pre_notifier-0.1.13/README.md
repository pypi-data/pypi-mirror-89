# Notifier

This tool provides you ability to send yourself information about looong executed command when it is done. Information will be sent using Telegram Bot, which you can generate for yourself with Telegram BotFather.


## Prerequisites
1. First of all register your bot at [@BotFather](https://telegram.me/BotFather). He will give you back your bot Telegram TOKEN. We'll use it later

2. Get your Telegram ID. You can get it from [@userinfobot](https://telegram.me/userinfobot). Save it too.

## Installation and running
```shell
>>> pip install pre_notifier
>>> pre_notifier config --telegram_id=YOUR_TELEGRAM_ID --token=YOUR_BOT_TOKEN
>>> pre_notifier notify [your_command_here]
```
