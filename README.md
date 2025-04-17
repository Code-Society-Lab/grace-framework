# Grace Framework
> *Build powerful Discord bots, without the boilerplate.*

[![Static Badge](https://img.shields.io/badge/%F0%9F%93%9A-Documentation-%235c5c5c)](https://github.com/Code-Society-Lab/grace-framework/wiki)
[![Join on Discord](https://discordapp.com/api/guilds/823178343943897088/widget.png?style=shield)](https://discord.gg/code-society-823178343943897088)
[![Tests](https://github.com/Code-Society-Lab/grace-framework/actions/workflows/grace_framework.yml/badge.svg?branch=main)](https://github.com/Code-Society-Lab/grace-framework/actions/workflows/grace_framework.yml)


## What is Grace Framework
Grace Framework is an opinionated, extensible Discord bot framework built on top of [discord.py](https://github.com/Rapptz/discord.py). It comes with a various tools designed to help you rapidly build scalable, feature-rich Discord bots with minimal boilerplate.

#### Key features
- **Quick to start**: Generate a full-featured bot in seconds
- **Modular Architecture**: Clean separation of features via extensions
- **Database Integration**: Easily connect your bot to a persistent backend
- **Built-in Generators**: Create extensions, models and more with a single command

#### Inspiration
Grace Framework was inspired by the evolution of our community discord bot, [Grace](https://github.com/Code-Society-Lab/grace),  that evolved, gaining support for modular extensions, database integrations, and rapid feature development — it began to resemble a standalone framework. Recognizing its potential, we decided to extracted its architecture into Grace Framework, making its ease-of-use and flexibility available to developers everywhere.

## Getting Started
#### 1- Install the package
**requirements**
- Python 3.10 or higher
- SQLite (or Postgresql, MySQL & MariaDB, Oracle, and MS-SQL)

```
$ pip install grace-framework
```

To install the development version:
```
$ git clone https://github.com/Code-Society-Lab/grace-framework.git
$ cd grace-framework
$ pip install -e .
```

*Note*: It is recommended to use a [virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) when installing python packages.

#### 2- Generate a new bot
```
$ grace new my-awesome-bot
$ cd my-awesome-bot
```

#### 3- Set your bot token
Edit the `.env` in the project directory and set `DISCORD_TOKEN`.

```
DISCORD_TOKEN=YOUR TOKEN
```

#### 4- Run your bot
```
$ grace run
```

#### 5- Start building!
Check out the official [wiki](https://github.com/Code-Society-Lab/grace-framework/wiki) for guides, architecture, and API reference.

# Contributing
We welcome everyone to contribute! 

Whether it's fixing bugs, suggesting features, or improving the docs - every bit helps.
- Submit an issue
- Open a pull request
- Or just hop into our [Discord community](https://discord.gg/code-society-823178343943897088) and say hi!

If you intend to contribute, please read the [CONTRIBUTING.md](./CONTRIBUTING.md) first. Additionally, **every contributor** is expected to follow the [code of conduct](./CODE_OF_CONDUCT.md).

# License
Grace Framework is released under [GPL-3.0](https://opensource.org/license/gpl-3-0)