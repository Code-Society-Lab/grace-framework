<div align="center" style="margin-bottom: 20px">
  <em>Build powerful <a href="https://discord.com">Discord</a> bots, without the boilerplate.</em>
</div>

<div align="center" markdown>

[Get Started](guides/installation.md){ .md-button .md-button--primary }
[Reference](reference/bot.md){ .md-button }

</div>

<div align="center">

<p>
  <a href="https://discord.gg/code-society-823178343943897088">
    <img
      src="https://discordapp.com/api/guilds/823178343943897088/widget.png?style=shield"
      alt="Join Discord"
    />
  </a>

  <a href="https://github.com/Code-Society-Lab/grace-framework/actions/workflows/grace_framework.yml">
    <img
      src="https://github.com/Code-Society-Lab/grace-framework/actions/workflows/grace_framework.yml/badge.svg?branch=main"
      alt="Tests"
    />
  </a>

  <a href="https://pypi.org/project/grace-framework/">
    <img
      src="https://img.shields.io/pypi/v/grace-framework"
      alt="PyPI"
    />
  </a>
</p>

</div>
---

Grace Framework is an opinionated, extensible Discord bot framework built on top of [discord.py](https://github.com/Rapptz/discord.py). It comes with the tools you need to rapidly build scalable, feature-rich Discord bots with minimal boilerplate.

- **Quick to start** — generate a full-featured bot in seconds
- **Modular architecture** — clean separation of features via extensions (cogs)
- **Database integration** — opt-in, per-project persistence backed by SQLModel and Alembic migrations
- **Built-in generators** — scaffold extensions, models, and migrations with a single command

## Quickstart

=== "Install"

    **Requirements:** Python 3.12+

    ```bash
    pip install grace-framework
    ```

    Using a virtual environment is strongly recommended:

    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    pip install grace-framework
    ```

=== "Generate"

    Scaffold a new bot project:

    ```bash
    grace new my-awesome-bot
    cd my-awesome-bot
    ```

    Set your bot token in `.env`:

    ```
    DISCORD_TOKEN=your token here
    ```

=== "Run"

    ```bash
    grace run
    ```

    Add `--watch` during development to enable hot reload:

    ```bash
    grace run --watch
    ```

## Where to go next

<div class="grid cards" markdown>

-   :fontawesome-solid-book-open: **Guides**

    ---

    Step-by-step tutorials covering installation, models, extensions, configuration, and more.

    [:octicons-arrow-right-24: Start with Installation](guides/installation.md)

-   :fontawesome-solid-code: **Reference**

    ---

    Complete API documentation for every class and function in the framework.

    [:octicons-arrow-right-24: Browse the Reference](reference/bot.md)

-   :fontawesome-solid-terminal: **Examples**

    ---

    Full walkthroughs demonstrating common patterns and use cases.

    [:octicons-arrow-right-24: View Examples](examples/index.md)

-   :fontawesome-brands-github: **Source Code**

    ---

    Browse the source, open issues, and contribute on GitHub.

    [:octicons-arrow-right-24: View on GitHub](https://github.com/Code-Society-Lab/grace-framework)

</div>

## Inspiration

Grace Framework was inspired by the evolution of our community Discord bot, [Grace](https://github.com/Code-Society-Lab/grace), which grew to support modular extensions, database integrations, and rapid feature development — it began to resemble a standalone framework. Recognizing its potential, we extracted its architecture into Grace Framework, making its ease-of-use and flexibility available to developers everywhere.

## Contributing

We welcome everyone to contribute! Whether it's fixing bugs, suggesting features, or improving the docs — every bit helps.

- [Submit an issue](https://github.com/Code-Society-Lab/grace-framework/issues)
- [Open a pull request](https://github.com/Code-Society-Lab/grace-framework/blob/main/CONTRIBUTING.md)
- Hop into our [Discord community](https://discord.gg/code-society-823178343943897088) and say hi!

Please read the [CONTRIBUTING.md](https://github.com/Code-Society-Lab/grace-framework/blob/main/CONTRIBUTING.md) and follow the [code of conduct](https://github.com/Code-Society-Lab/grace-framework/blob/main/CODE_OF_CONDUCT.md).

## License

Released under the [MIT License](https://github.com/Code-Society-Lab/grace-framework/blob/main/LICENSE).
