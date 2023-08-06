# -*- coding: utf-8 -*-
#
# Copyright 2016 dpa-infocom GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import aiohttp
import bleach
import logging
import re
from urllib.parse import urlencode
from livebridge.base import BaseConverter, ConversionResult

logger = logging.getLogger(__name__)

class LiveblogScribbleliveConverter(BaseConverter):

    source = "liveblog"
    target = "scribble"

    async def _get_instagram_embed(self, insta_url):
        """Resolve embed code via Instagram API."""
        try:
            api_url = "https://api.instagram.com/oembed/?{}".format(urlencode({"url": insta_url}))
            headers = {"Content-Type": "application/json", "Accept": "application/json"}
            async with aiohttp.ClientSession(conn_timeout=10, headers=headers) as session:
                async with session.get(api_url) as response:
                    api_resp = await response.json()
                    return api_resp.get("html", None)
        except Exception as exc:
            logger.error("Fatal error when requesting instagram emebd.")
            logger.exception(exc)
        return ""

    async def _get_twitter_embed(self, twitter_url):
        """Resolve embed code via Twitter API."""
        try:
            api_url = "https://publish.twitter.com/oembed?{}".format(urlencode({"url": twitter_url, "dnt" : "1"}))
            headers = {"Content-Type": "application/json", "Accept": "application/json"}
            async with aiohttp.ClientSession(conn_timeout=10, headers=headers) as session:
                async with session.get(api_url) as response:
                    api_resp = await response.json()
                    return api_resp.get("html", None)
        except Exception as exc:
            logger.error("Fatal error when requesting twitter emebd.")
            logger.exception(exc)
        return ""

    async def _convert_image_inline(self, item):
        logger.debug("CONVERTING IMAGE INLINE")
        content = ""
        tmp_path = None
        try:
            # handle image
            image_data = item["item"]["meta"]["media"]["renditions"]["viewImage"]
            if image_data.get("href"):
                content += '<img src="{}" />'.format(image_data["href"])
            # handle text
            caption = item["item"]["meta"]["caption"]
            if caption:
                content += "<br>{} ".format(caption)
            credit = item["item"]["meta"]["credit"]
            if credit:
                content += "<i>({})</i>".format(credit)
            # wrap in div
            if content:
                content = "<div>{}</div>".format(content)
            else:
                # assure at last a whitespace!
                content += " "
        except Exception as e:
            logger.error("Fatal error when converting image.")
            logger.exception(e)
        return content, tmp_path

    async def _convert_image(self, item):
        logger.debug("CONVERTING IMAGE")
        content = ""
        tmp_path = None
        try:
            # handle image
            image_data = item["item"]["meta"]["media"]["renditions"]["baseImage"]
            if image_data:
                tmp_path = await self._download_image(image_data)

            # handle text
            caption = item["item"]["meta"]["caption"]
            if caption:
                content += "<br>{} ".format(caption)
            credit = item["item"]["meta"]["credit"]
            if credit:
                content += "<i>({})</i>".format(credit)
            if caption or credit:
                content += "<br>"
            # assure at last a whitespace!
            content += " "
        except Exception as e:
            logger.error("Fatal downloading image item.")
            logger.exception(e)
        return content, tmp_path

    async def _convert_text(self, item):
        logger.debug("CONVERTING TEXT")
        content = "<p>"
        text = item["item"]["text"].strip()
        text = text.replace("<ol>", "").replace("</ol>", "<br>")
        text = text.replace("<ul>", "").replace("</ul>", "<br>")
        text = text.replace("<li>", "<br> &bull; ").replace("</li>", "")
        text = text.replace("strike>", "s>")
        if text.startswith('<p>') and text.endswith("</p>"):
            text = text[3:-4]
        content += bleach.clean(text, tags=["b", "i", "a", "s", "br", "p", "div"], strip=True)
        content += "</p>"
        content = content.replace("<p><br></p>", "")
        content = content.replace("<p></p>", "")
        return content

    async def _convert_quote(self, item):
        logger.debug("CONVERTING QUOTE")
        meta = item["item"]["meta"]
        content = "<blockquote>{}<br>".format(meta.get("quote",""))
        if meta.get("credit"):
            content += "<br> &bull; <i>{}</i>".format(meta.get("credit", ""))
        content += "</blockquote>"
        return content

    def _prepare_facebook_embed(self, embed):
        embed = re.sub(r'<script>.*<\/script>$', '', embed)
        return embed

    def _prepare_youtube_embed(self, meta):
        template = """
        <div class="youtube-wrapper-frame"><div style="left: 0; width: 100%; height: 0; position: relative; padding-bottom: 56.25%;"><iframe class="livebridge-iframe" src="https://www.youtube-nocookie.com/embed/{original_id}" style="border: 0; top: 0; left: 0; width: 100%; height: 100%; position: absolute;" allowfullscreen="" scrolling="no" allow="encrypted-media *; accelerometer; clipboard-write; gyroscope; picture-in-picture"></iframe></div></div>
        """
        embed = template.format(**meta)
        logger.debug("Converted Youtube to "+embed)
        return embed

    def _prepare_twitter_embed(self, embed):
        embed = re.sub(r'<script[^<]*<\/script>$', '', embed, flags=re.M)
        logger.debug("Converted Tweet to "+embed)
        return embed.strip()

    def _prepare_instagram_embed(self, embed):
        embed = re.sub(r'<script[^<]*<\/script>$', '', embed, flags=re.M)
        return embed.strip()

    async def _convert_embed(self, item):
        logger.debug("Converting embed: {item}".format(item=repr(item)))

        meta = item["item"]["meta"]
        provider = meta.get("provider_name", "")
        if provider == "Twitter":
            twitter_embed = await self._get_twitter_embed(meta["original_url"])
            content = self._prepare_twitter_embed(twitter_embed)
        if provider == "YouTube":
            content = self._prepare_youtube_embed(meta)
        elif meta.get("provider_name") == "Facebook":
            content = self._prepare_facebook_embed(meta["html"])
        elif meta.get("provider_name") == "Instagram":
            insta_embed = await self._get_instagram_embed(meta["original_url"])
            content = self._prepare_instagram_embed(insta_embed)
        elif meta.get("html", "").find('class="instagram-media"') > -1:
            content = self._prepare_instagram_embed(meta["html"])
        elif meta.get("html", "").find("youtube.com") > -1 and meta.get("html", "").find("embedly-embed") > -1:
            content = self._prepare_youtube_embed(meta)
        elif meta.get("html", "").find('youtube.com/embed') > -1:
            content = self._prepare_youtube_embed(meta)
        elif meta.get("html", "").find('<iframe ') > -1:
            content = meta["html"]
        else:
            pass # positive list

        # add extra text

        if provider != "YouTube":
            if meta.get("title"):
                content += "<br><div><strong>{}</strong></div>".format(meta["title"])
            if meta.get("description"):
                content += "<p>{}</p>".format(meta["description"])
            if meta.get("credit"):
                content += "<div><i>{}</i></div>".format(meta["credit"])
        return content

    async def convert(self, post):
        """ See https://developer.scribblelive.com/accepted-and-stripped-html-tags-posted-via-api/
            for more infos by SL about supported HTML."""
        content =  ""
        images = []
        try:
            for g in post.get("groups", []):
                if g["id"] != "main":
                    continue

                for item in g["refs"]:
                    logger.debug("Converting "+item["item"]["item_type"])
                    if item["item"]["item_type"] == "text":
                        content += await self._convert_text(item)
                    elif item["item"]["item_type"] == "quote":
                        content += await self._convert_quote(item)
                    elif item["item"]["item_type"] == "image":
                        caption, img_path = await self._convert_image_inline(item)
                        if caption:
                            content += caption
                        #if img_path:
                        #    content += caption
                        #    images.append(img_path)
                    elif item["item"]["item_type"] == "embed":
                        content += await self._convert_embed(item)
                    else:
                        logger.debug("CONVERSION UNKNOWN")
                        logger.debug("Typ: {}".format(item["type"]))
                        logger.debug("Item-Type: {}".format(item["item"]["item_type"]))
                        logger.debug(item)
                        logger.debug("\n\n")
        except Exception as e:
            logger.error("Converting post failed.")
            logger.exception(e)
        return ConversionResult(content=content, images=images)
