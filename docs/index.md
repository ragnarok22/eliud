# Welcome to Eliud Framework

A simple Framework to create Telegram Bots as fast you can.

[![Tests](https://github.com/ragnarok22/eliud/actions/workflows/tests.yml/badge.svg)](https://github.com/ragnarok22/eliud/actions/workflows/tests.yml)
![GitHub](https://img.shields.io/github/license/ragnarok22/eliud)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)

## Commands

* `eliud startproject [dir-name]` - Create a new project.
* `eliud startapp [app-name]` - Create a new app inside a project.
* `eliud runbot` - Start the live-reloading development server.
* `eliud help` - Print help message and exit.


## Requirements

Python 3.8+

## Example
Create a project named `myproject`:

    eliud startproject myproject

Enter the project:

    cd myproject

set your Bot token (created in [@BotFather](https://t.me/BotFather)) in settings.py:

    echo "TELEGRAM_TOKEN=wers***" >> myproject/settings.py

Run your bot:

    python manage.py runbot
