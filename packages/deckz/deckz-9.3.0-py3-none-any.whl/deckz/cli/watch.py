from logging import getLogger
from pathlib import Path
from threading import Thread
from time import time
from typing import List, Optional

from typer import Argument
from watchdog.events import FileSystemEvent
from watchdog.observers import Observer

from deckz.cli import app
from deckz.exceptions import DeckzException
from deckz.paths import Paths
from deckz.runner import run


@app.command()
def watch(
    targets: Optional[List[str]] = Argument(None),
    handout: bool = False,
    presentation: bool = True,
    print: bool = False,
    minimum_delay: int = 5,
    deck_path: str = ".",
) -> None:
    """Compile on change."""

    class LatexCompilerEventHandler:
        def __init__(
            self,
            minimum_delay: int,
            paths: Paths,
            build_handout: bool,
            build_presentation: bool,
            build_print: bool,
            target_whitelist: List[str],
        ):
            self._minimum_delay = minimum_delay
            self._last_compile = 0.0
            self._paths = paths
            self._build_handout = build_handout
            self._build_presentation = build_presentation
            self._build_print = build_print
            self._target_whitelist = target_whitelist
            self._worker: Optional[Thread] = None

        def work(self) -> None:
            try:
                self._compiling = True
                logger.info("Detected changes, starting a new build")
                try:
                    run(
                        paths=self._paths,
                        build_handout=self._build_handout,
                        build_presentation=self._build_presentation,
                        build_print=self._build_print,
                        target_whitelist=self._target_whitelist,
                    )
                    logger.info("Build finished")
                except Exception as e:
                    logger.critical("Build failed. Error: %s", str(e))
            finally:
                self._compiling = False

        def dispatch(self, event: FileSystemEvent) -> None:
            for d in [paths.build_dir, paths.pdf_dir]:
                if d in Path(event.src_path).parents:
                    return
            current_time = time()
            if self._last_compile + self._minimum_delay > current_time:
                return
            elif self._worker is not None and self._worker.is_alive():
                logger.info("Still on last build, not starting a new build")
                return
            else:
                self._last_compile = current_time
                self._worker = Thread(target=self.work)
                self._worker.start()

    logger = getLogger(__name__)
    logger.info("Watching current and shared directories")
    paths = Paths(deck_path)
    observer = Observer()
    event_handler = LatexCompilerEventHandler(
        minimum_delay,
        paths=paths,
        build_handout=handout,
        build_print=print,
        build_presentation=presentation,
        target_whitelist=targets,
    )
    paths_to_watch = [
        (p, False) for p in paths.shared_dir.glob("**/*") if p.resolve().is_dir()
    ]
    paths_to_watch.append((paths.jinja2_dir, True))
    paths_to_watch.append((paths.current_dir, True))
    for path, recursive in paths_to_watch:
        observer.schedule(event_handler, str(path.resolve()), recursive=recursive)
    observer.start()
    try:
        while observer.isAlive():
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
        logger.info("Stopped watching")
    else:
        observer.join()
        raise DeckzException("Stopped watching abnormally")
