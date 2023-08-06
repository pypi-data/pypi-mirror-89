# python standard imports
import xml.etree.ElementTree as etree

# markdown imports
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor

# internal imports
from . import schemas, load_schemas

class CitationInlineProcessor(InlineProcessor):
    ANCESTOR_EXCLUDES = ('a',)
    def __init__(self, schema, md):
        super().__init__(schema.regex.pattern, md)
        self.schema = schema

    def handleMatch(self, m, data):
        try:
            url = self.schema._url_from_match(m)
        except KeyError: # return text unchanged if URL generation failed
            return m.group(0), m.start(0), m.end(0)
        el = etree.Element('a')
        el.attrib={'href': url}
        el.text = m.group(0)
        return el, m.start(0), m.end(0)
        
class CiteURLExtension(Extension):
    """Detects legal citations and inserts relevant hyperlinks."""
    def __init__(self, **kwargs):
        self.config = {'supplemental_yamls': [
            [],
            'List of paths to YAML files containing additional citation'
            + 'schemas to load. - Default: []'
        ]}
        super(CiteURLExtension, self).__init__(**kwargs)
    
    def extendMarkdown(self, md):
        for path in self.config['supplemental_yamls'][0]:
            load_schemas(path)
        pattern = 1
        for schema in schemas:
            md.inlinePatterns.register(
                CitationInlineProcessor(schema, md),
                'citeurl-pattern-' + str(pattern),
                pattern + 1037,
            )
            pattern += 1

def makeExtension(**kwargs):
    return CiteURLExtension(**kwargs)
