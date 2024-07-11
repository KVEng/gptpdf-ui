from markdown.inlinepatterns import InlineProcessor
from markdown.extensions import Extension
import xml.etree.ElementTree as ElementTree

class ImagePrefixExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            'prefix': ['', 'Prefix for image paths']
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        IMAGE_LINK_RE = r'!\[(.*?)\]\((.*?)\)'
        md.inlinePatterns.register(ImagePrefixInlineProcessor(IMAGE_LINK_RE, self.getConfigs()), 'image_prefix', 175)

class ImagePrefixInlineProcessor(InlineProcessor):
    def __init__(self, pattern, config):
        super().__init__(pattern)
        self.config = config

    def handleMatch(self, m, data):
        if m:
            alt = m.group(1)
            src = m.group(2)
            src = self.config['prefix'] + "/" + src
            el = ElementTree.Element("img")
            el.set('style', 'max-width: 100%')
            el.set('src', src)
            el.set('alt', alt)
            return el, m.start(0), m.end(0)
        return None, None, None

