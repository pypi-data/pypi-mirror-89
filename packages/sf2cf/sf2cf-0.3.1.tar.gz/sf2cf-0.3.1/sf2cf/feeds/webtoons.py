# Copyright (c) 2020, Cyril Roelandt
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
import base64
import datetime
import html
import io
import logging
from lxml import html as lxml_html

from PIL import Image
import requests

from sf2cf import sf2cf


LOG = logging.getLogger('sf2cf')


class Webtoons(sf2cf.FeedFixer):
    name = 'webtoons'
    version = '0.1'
    description = ('This feed provider creates an ATOM feed for comics from '
                   'https://www.webtoons.com/')
    sample_conf = ('''[feed:webtoons]
plugin=webtoons
url=https://www.webtoons.com/fr/comedy/monsieur-le-prof/list?title_no=2382
output=/path/to/output.xml''')

    def __init__(self, conf_section):
        try:
            self.output = self._expand_path(conf_section['output'])
            self.url = conf_section['url']
        except KeyError:
            LOG.error('You MUST specify an output file and a URL.')
            raise

    @staticmethod
    def _get_image(url):
        # Webtoons does not like the Web, so they prevent their images from
        # being viewable without the "Referer" header.
        headers = {
            "Referer": "https://www.webtoons.com/",
        }
        r = requests.get(url, headers=headers)
        return Image.open(io.BytesIO(r.content))

    @staticmethod
    def _concat_images(images):
        result = Image.new('RGB', (images[0].width,
                                   sum([img.height for img in images])))
        total_height = 0
        for image in images:
            result.paste(image, (0, total_height))
            total_height += image.height
        return result

    @staticmethod
    def _get_base64_for_image(image):
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode('ascii')

    def _get_comic_image_as_base64(self, comic_url):
        r = requests.get(comic_url)
        comic_tree = lxml_html.fromstring(r.content)
        img_urls = comic_tree.xpath('//div[@id="_imageList"]/img/@data-url')
        images = [self._get_image(url) for url in img_urls]
        image = self._concat_images(images)
        return self._get_base64_for_image(image)

    def run(self):
        r = requests.get(self.url)
        tree = lxml_html.fromstring(r.content)
        feed_title = tree.xpath('//h1[@class="subj"]/text()')[0]
        now = datetime.datetime.now()
        now = datetime.datetime.isoformat(now, timespec='seconds')

        with open(self.output, 'w+') as f:
            f.write(f'''<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="en">
  <title>{feed_title}</title>
  <link href="{self.url}" rel="alternate"/>
  <id>{self.url}</id>
  <updated>{now}</updated>''')
            for li in tree.xpath('//ul[@id="_listUl"]/li'):
                comic_link = li.xpath('./a/@href')[0]
                f.write('  <entry>')
                thumbnail_img = li.xpath('.//span[@class="thmb"]/img')[0]
                date_str = thumbnail_img.attrib['src'].split('/')[3][:8]
                pub_date = datetime.datetime(int(date_str[0:4]),
                                             int(date_str[4:6]),
                                             int(date_str[6:8]))

                pub_date = datetime.datetime.isoformat(pub_date, timespec='seconds')  # noqa
                title = thumbnail_img.attrib['alt']
                f.write(f'    <title>{html.escape(title, quote=False)}</title>')  # noqa
                f.write(f'    <link href="{html.escape(comic_link, quote=False)}" rel="alternate"/>')  # noqa
                f.write(f'    <updated>{pub_date}</updated>')
                f.write(f'    <id>{html.escape(comic_link, quote=False)}</id>')

                b64 = self._get_comic_image_as_base64(comic_link)
                summary = f'<img src="data:image/jpeg;base64,{b64}"/>'
                summary = html.escape(summary, quote=False)
                f.write(f'    <summary type="html">{summary}</summary>')
                f.write('  </entry>')
            f.write('</feed>')
