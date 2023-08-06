# coding: utf8
"""tankobon (漫画): Manga downloader and scraper."""

import abc
import collections
import concurrent.futures
import functools
import logging
import pathlib
import shutil
import time
from multiprocessing.pool import ThreadPool as Pool
from typing import Any, Dict, Generator, List, Optional, Tuple, Union

import bs4
import fpdf
import imagesize
import natsort
import requests
import requests_random_user_agent  # noqa: F401

from tankobon import utils
from tankobon.exceptions import TankobonError

_log = logging.getLogger("tankobon")


class GenericManga(abc.ABC):
    """A generic manga website.

    Args:
        database: The inital database of the manga as a dictionary.
            It must be in this format:
            {
                "title": "...",  # manga title/name
                "url": "...",  # manga index (chapter listing)
                "chapters": {...}  # cached chapter info, automatically generated
            }
            where 'title' and 'url' must be specified,
            and 'chapters' may be an empty dict.
        update: Whether or not to download and parse the index, adding any new
            chapters. Defaults to True.

    Attributes:
        database (dict): see args
        soup (bs4.BeautifulSoup): The soup of the HTML.
    """

    # you should overrride this
    DEFAULTS: Dict[str, Any] = {}

    def __init__(self, database: dict = {}, update: bool = False) -> None:
        self.database = self.DEFAULTS
        self.database.update(database)  # type: ignore

        self.database.setdefault("chapters", {})

        self.session = requests.Session()
        # hehe boi
        self.session.headers.update({"referer": self.database["url"]})

        # monkeypatch for convinence in client code
        self.session.get = functools.partial(self.session.get, timeout=5)  # type: ignore[assignment]

        self.soup = self.get_soup(self.database["url"])
        if update:
            self.update()

    def __getattr__(self, key):
        value = self.database.get(key)
        if value is None:
            raise AttributeError
        return value

    def sorted(self) -> List[str]:
        return natsort.natsorted(self.database["chapters"])

    def update(self) -> None:
        """Add all (new) chapters to the database."""
        self.database["title"] = self.get_title()
        self.database["covers"] = self.get_covers()
        for chapter, chapter_info in self.get_chapters():
            if chapter in self.database["chapters"]:
                continue

            if not chapter_info.get("volume"):
                chapter_info["volume"] = "0"
            self.database["chapters"][chapter] = chapter_info

    def get_soup(self, url: str) -> bs4.BeautifulSoup:
        """Get a soup from a url.

        Args:
            url: The url.

        Returns:
            The soup object.
        """
        return utils.get_soup(url, session=self.session)

    @abc.abstractmethod
    def get_chapters(self) -> Generator[Tuple[str, Dict[str, str]], None, None]:
        """Get all chapters in the manga.
        You must override this.

        Yields:
            A two-tuple of (chapter, chapter_info)
            where chapter is the chapter number and chapter_info is a dict:
            {
                "title": "chapter title",
                "url": "chapter url",
                "volume": "volume, i.e '0'",
            }
        """

    @abc.abstractmethod
    def get_pages(self, chapter_url: str) -> List[str]:
        """Get all pages for a chapter, given its url.
        You must override this.

        Args:
            chapter_url: The url of the chapter.
        Returns:
            A list of urls of the pages.
        """

    def get_title(self) -> str:
        """Get the title of the manga.
        Overriding this is optional.

        Returns:
            The manga title.
        """
        return (
            self.soup.title.text
            or self.soup.find("meta", property="og:title")["content"]
        )

    def get_covers(self) -> Dict[str, str]:
        """Get all covers for the manga volumes.
        Overriding this is optional, the cover won't be downloaded if it does not exist.

        Returns:
            A dictionary where volume numbers are mapped to the url of the cover:
            {
                "0": "...",
                ...
            }
        """
        return {}

    def _build_volumes(self) -> Dict[str, List[str]]:
        volumes = collections.defaultdict(list)
        for chapter, chapter_info in self.database["chapters"].items():
            volume = chapter_info.get("volume") or "0"
            volumes[volume].append(chapter)
        return volumes

    def parse(self, chapters: Optional[List[str]] = None) -> List[str]:
        """Parse chapters, adding their pages to the database.

        Args:
            chapters: The chapters to parse. If None, all chapters are parsed.
                Defaults to None.

        Returns:
            The chapters that were parsed.
        """
        if chapters is None:
            chapters = self.database["chapters"].keys()

        with concurrent.futures.ThreadPoolExecutor() as pool:
            results = {
                pool.submit(
                    self.get_pages, self.database["chapters"][chapter]["url"]
                ): chapter
                for chapter in chapters
                if not self.database["chapters"][chapter].get("pages")
            }

            for future in concurrent.futures.as_completed(results):
                chapter = results[future]
                pages = future.result()
                if not chapter or not pages:
                    continue
                self.database["chapters"][chapter]["pages"] = pages
                _log.info(f"[parse] parsed {chapter}")

        return chapters

    def _download_page(
        self,
        chapter_path: pathlib.Path,
        page_number: int,
        cooldown: int,
        *args,
        **kwargs,
    ):
        time.sleep(cooldown)
        with self.session.get(*args, **kwargs) as response:
            page_path = chapter_path / f"{page_number}"
            try:
                # return path to page
                return utils.save_response(page_path, response)
            except KeyError:
                # there is no content type (text/html, problably)
                raise TankobonError(f"page '{response.url}' is not an image")

    def download_chapters(
        self,
        path: Union[str, pathlib.Path],
        chapters: Optional[List[str]] = None,
        force: bool = False,
        cooldown: int = 2,
    ) -> None:
        """Download chapters, caching its pages on disk.

        Args:
            path: Where to download the chapters to.
            chapters: The chapters to download. Defaults to all chapters.
            force: Whether or not to re-download chapters, regardless if they are
                already downloaded. Defaults to False.
            cooldown: How long to wait before downloading each page.
                Defaults to 2.
        """

        path = pathlib.Path(path)

        chapters = self.parse(chapters=chapters)

        _log.info(f"[download] {len(chapters)} chapters to download, starting")

        for chapter in chapters:

            chapter_path = path / chapter
            if chapter_path.exists() and not force:
                _log.info(f"[download] skipping chapter {chapter}")
                continue
            _log.info(f"[download] downloading chapter {chapter}")

            try:
                chapter_path.mkdir(exist_ok=True)
                urls = self.database["chapters"][chapter]["pages"]

                with concurrent.futures.ThreadPoolExecutor() as pool:
                    responses = [
                        pool.submit(
                            self._download_page, chapter_path, page, cooldown, url
                        )
                        for page, url in enumerate(urls)
                    ]

                    for future in concurrent.futures.as_completed(responses):
                        # just run the function, no need for the return result
                        __ = future.result()

            except:  # noqa: E722
                _log.critical(
                    "[download] could not download all pages for chapter %s, removing chapter dir",
                    chapter,
                )
                shutil.rmtree(str(chapter_path))
                raise

    def download_volumes(
        self,
        path: Union[str, pathlib.Path],
        volumes: Optional[List[str]] = None,
        add_cover: bool = False,
        **kwargs,
    ) -> None:
        """Download volumes, by downloading the chapters first and adding their pages to a PDF.

        Args:
            path: Where to download the volumes (as {volume_number}.pdf).
            volumes: The volumes to download.
                If not specified, all volumes are downloaded.
            add_cover: Whether or not to add a cover to each volume (if it exists).
                Defaults to False.
            **kwargs: Passed to download_chapters.
        """
        path = pathlib.Path(path)

        all_volumes = self._build_volumes()
        if volumes is None:
            volumes = list(all_volumes.keys())

        for volume in volumes:
            chapters = all_volumes[volume]

            # download required chapters first
            self.download_chapters(path, chapters=chapters, **kwargs)

            _log.info("[pdf] creating pdf for volume %s", volume)
            pdf = fpdf.FPDF()

            cover_url = self.database["covers"].get(volume)
            if cover_url is not None and add_cover:
                _log.debug("[pdf] adding cover from %s", cover_url)
                cover_path = str(
                    utils.save_response(
                        path / f"cover_{volume}",
                        self.session.get(cover_url),
                    )
                )
                pdf.add_page()
                pdf.image(cover_path)

            for chapter in natsort.natsorted(chapters):
                _log.info("[pdf] adding chapter %s", chapter)
                chapter_path = path / chapter
                for page in natsort.natsorted(
                    (str(p) for p in chapter_path.glob("*.*"))
                ):
                    _log.debug("[pdf] adding page %s", page)
                    pdf.add_page()

                    width, height = imagesize.get(page)
                    page_width = 210
                    page_height = 297
                    ratio = min(page_width / width, page_height / height)

                    # use ratio to scale correctly
                    try:
                        pdf.image(page, 0, 0, w=width * ratio, h=height * ratio)
                    except RuntimeError as e:
                        raise RuntimeError(page, e)

            _log.info("[pdf] saving %s.pdf", volume)
            pdf.output(str(path / f"{volume}.pdf"), "F")
