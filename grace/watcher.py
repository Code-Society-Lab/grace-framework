import sys
import asyncio
import importlib.util

from pathlib import Path
from logging import WARNING, getLogger, info, error
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer


getLogger("watchdog").setLevel(WARNING)


class Watcher:
    def __init__(self, bot):
        self.bot = bot
        self.observer = Observer()
        self.watch_path = "./bot"

        self.observer.schedule(
            BotEventHandler(self.bot, self.watch_path),
            self.watch_path,
            recursive=True
        )

    def start(self):
        info("Starting file watcher...")
        self.observer.start()

    def stop(self):
        info("Stopping file watcher...")
        self.observer.stop()
        self.observer.join()


class BotEventHandler(FileSystemEventHandler):
    def __init__(self, bot, base_path: Path):
        self.bot = bot
        self.bot_path = Path(base_path).resolve()

    def path_to_module_name(self, path: Path) -> str:
        relative_path = path.resolve().relative_to(bot_path)
        parts = relative_path.with_suffix('').parts

        return '.'.join(['bot'] + list(parts))

    def reload_module(self, module_name: str):
        try:
            if module_name in sys.modules:
                info(f"Reloading module '{module_name}'")
                importlib.reload(sys.modules[module_name])
        except Exception as e:
            error(f"Failed to reload module {module_name}: {e}")

    def run_coro(self, coro):
        """Run coroutine safely inside running event loop."""
        try:
            loop = asyncio.get_running_loop()
            asyncio.ensure_future(coro)
        except RuntimeError:
            asyncio.run(coro)

    def on_modified(self, event):
        if event.is_directory:
            return

        module_path = Path(event.src_path)
        if module_path.suffix != '.py':
            return

        module_name = self.path_to_module_name(module_path)
        if not module_name:
            return

        self.reload_module(module_name)
        self.run_coro(self.bot.on_reload())

    def on_deleted(self, event):
        if event.is_directory:
            return

        module_path = Path(event.src_path)
        if module_path.suffix != '.py':
            return

        module_name = self.path_to_module_name(module_path)
        if not module_name:
            return

        self.run_coro(self.bot.unload_extension(module_name))