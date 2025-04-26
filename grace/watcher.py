import sys
import asyncio
import importlib.util

from pathlib import Path
from typing import Callable, Coroutine, Any, Union
from logging import WARNING, getLogger, info, error
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer


# Suppress verbose watchdog logs
getLogger("watchdog").setLevel(WARNING)


ReloadCallback = Callable[[], Coroutine[Any, Any, None]]


class Watcher:
    """
    Wrapper around the watchdog observer that watches a specified
    directory (./bot) for Python file changes and manages event handling.

    :param bot: The bot instance, must implement `on_reload()` and `unload_extension()`.
    :type bot: Callable
    """
    def __init__(self, callback: ReloadCallback) -> None:
        self.callback: ReloadCallback = callback
        self.observer: Observer = Observer()
        self.watch_path: str = "./bot"

        self.observer.schedule(
            BotEventHandler(self.callback, self.watch_path),
            self.watch_path,
            recursive=True
        )

    def start(self) -> None:
        """Starts the file system observer."""
        info("Starting file watcher...")
        self.observer.start()

    def stop(self) -> None:
        """Stops the file system observer and waits for it to shut down."""
        info("Stopping file watcher...")
        self.observer.stop()
        self.observer.join()


class BotEventHandler(FileSystemEventHandler):
    """
    Handles file events in the bot directory and calls the provided 
    async callback.

    :param callback: Async function to call with the module name.
    :type callback: Callable[[str], Coroutine]
    :param base_path: Directory path to watch.
    :type base_path: Path or str
    """
    def __init__(self, callback: ReloadCallback, base_path: Union[Path, str]):
        self.callback = callback
        self.bot_path = Path(base_path).resolve()

    def path_to_module_name(self, path: Path) -> str:
        """
        Converts a file path to a Python module name.

        :param path: Full path to the Python file.
        :type path: Path
        :return: Dotted module path (e.g., 'bot.module.sub').
        :rtype: str
        """
        relative_path = path.resolve().relative_to(self.bot_path)
        parts = relative_path.with_suffix('').parts
        return '.'.join(['bot'] + list(parts))

    def reload_module(self, module_name: str) -> None:
        """
        Reloads a module if it's already in sys.modules.

        :param module_name: Dotted module name to reload.
        :type module_name: str
        """
        try:
            if module_name in sys.modules:
                info(f"Reloading module '{module_name}'")
                importlib.reload(sys.modules[module_name])
        except Exception as e:
            error(f"Failed to reload module {module_name}: {e}")

    def run_callback(self) -> None:
        """Runs a coroutine callback in the current or a new event loop."""
        try:
            loop = asyncio.get_running_loop()
            asyncio.ensure_future(self.callback())
        except RuntimeError:
            asyncio.run(self.callback())

    def on_modified(self, event: FileSystemEvent) -> None:
        """
        Handles modified Python files by reloading them and calling the callback.

        :param event: The filesystem event.
        :type event: FileSystemEvent
        """
        try:
            if event.is_directory:
                return

            module_path = Path(event.src_path)
            if module_path.suffix != '.py':
                return

            module_name = self.path_to_module_name(module_path)
            if not module_name:
                return

            self.reload_module(module_name)
            self.run_callback()
        except Exception as e:
            error(f"Failed to reload module {module_name}: {e}")


    def on_deleted(self, event: FileSystemEvent) -> None:
        """
        Handles deleted Python files by calling the callback with the module name.

        :param event: The filesystem event.
        :type event: FileSystemEvent
        """
        try:
            module_path = Path(event.src_path)
            if module_path.suffix != '.py':
                return

            module_name = self.path_to_module_name(module_path)
            if not module_name:
                return

            self.run_coro(self.callback())
        except Exception as e:
            error(f"Failed to reload module {module_name}: {e}")