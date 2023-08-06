# -*- coding: utf-8 -*-

# Copyright 2019-2020 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://www.wikiart.org/"""

from .common import Extractor, Message
from .. import text

BASE_PATTERN = r"(?:https?://)?(?:www\.)?wikiart\.org/([a-z]+)"


class WikiartExtractor(Extractor):
    """Base class for wikiart extractors"""
    category = "wikiart"
    filename_fmt = "{id}_{title}.{extension}"
    archive_fmt = "{id}"
    root = "https://www.wikiart.org"

    def __init__(self, match):
        Extractor.__init__(self, match)
        self.lang = match.group(1)

    def items(self):
        data = self.metadata()
        yield Message.Version, 1
        yield Message.Directory, data
        for painting in self.paintings():
            url = painting["image"]
            painting.update(data)
            yield Message.Url, url, text.nameext_from_url(url, painting)

    def metadata(self):
        """Return a dict with general metadata"""

    def paintings(self):
        """Return an iterable containing all relevant 'painting' objects"""

    def _pagination(self, url, extra_params=None, key="Paintings"):
        headers = {
            "X-Requested-With": "XMLHttpRequest",
            "Referer": url,
        }
        params = {
            "json": "2",
            "layout": "new",
            "page": 1,
            "resultType": "masonry",
        }
        if extra_params:
            params.update(extra_params)

        while True:
            data = self.request(url, headers=headers, params=params).json()
            items = data.get(key)
            if not items:
                return
            yield from items
            params["page"] += 1


class WikiartArtistExtractor(WikiartExtractor):
    """Extractor for an artist's paintings on wikiart.org"""
    subcategory = "artist"
    directory_fmt = ("{category}", "{artist[artistName]}")
    pattern = BASE_PATTERN + r"/(?!\w+-by-)([\w-]+)"
    test = ("https://www.wikiart.org/en/thomas-cole", {
        "url": "5ba2fbe6783fcce34e65014d16e5fbc581490c98",
        "keyword": "6d92913c55675e05553f000cfee5daff0b4107cf",
    })

    def __init__(self, match):
        WikiartExtractor.__init__(self, match)
        self.artist = match.group(2)

    def metadata(self):
        url = "{}/{}/{}?json=2".format(self.root, self.lang, self.artist)
        return {"artist": self.request(url).json()}

    def paintings(self):
        url = "{}/{}/{}/mode/all-paintings".format(
            self.root, self.lang, self.artist)
        return self._pagination(url)


class WikiartArtworksExtractor(WikiartExtractor):
    """Extractor for artwork collections on wikiart.org"""
    subcategory = "artworks"
    directory_fmt = ("{category}", "Artworks by {group!c}", "{type}")
    pattern = BASE_PATTERN + r"/paintings-by-([\w-]+)/([\w-]+)"
    test = ("https://www.wikiart.org/en/paintings-by-media/grisaille", {
        "url": "36e054fcb3363b7f085c81f4778e6db3994e56a3",
    })

    def __init__(self, match):
        WikiartExtractor.__init__(self, match)
        self.group = match.group(2)
        self.type = match.group(3)

    def metadata(self):
        return {"group": self.group, "type": self.type}

    def paintings(self):
        url = "{}/{}/paintings-by-{}/{}".format(
            self.root, self.lang, self.group, self.type)
        return self._pagination(url)


class WikiartArtistsExtractor(WikiartExtractor):
    """Extractor for artist collections on wikiart.org"""
    subcategory = "artists"
    pattern = (BASE_PATTERN + r"/artists-by-([\w-]+)/([\w-]+)")
    test = ("https://www.wikiart.org/en/artists-by-century/12", {
        "pattern": WikiartArtistExtractor.pattern,
        "count": ">= 8",
    })

    def __init__(self, match):
        WikiartExtractor.__init__(self, match)
        self.group = match.group(2)
        self.type = match.group(3)

    def items(self):
        url = "{}/{}/App/Search/Artists-by-{}".format(
            self.root, self.lang, self.group)
        params = {"json": "3", "searchterm": self.type}

        for artist in self._pagination(url, params, "Artists"):
            artist["_extractor"] = WikiartArtistExtractor
            yield Message.Queue, self.root + artist["artistUrl"], artist
