# python standard imports
import re
from pathlib import Path

# external imports
from yaml import safe_load

###################################################
# define classes
###################################################

class Schema:
    """
    The information needed to turn a citation into a URL.

    Each schema represents a body of law. At minimum it needs a
    regex to recognize, and a set of URLParts to construct a URL
    out of capture groups from the regex. A schema may also have
    default values, mutations, and substitutions, which will be
    applied, in that order, to the specified capture groups before
    constructing the URL.

    For how to write a schema, see citation-schemas.yml."""

    link_class = "statutory-link"

    def __init__(self, ydict: dict):
        self.__dict__ = ydict
        self.regex = re.compile("".join(self.regexParts), flags=re.I)
        if hasattr(self, "broadRegexParts"):
            self.broadRegex = re.compile(
                "".join(self.broadRegexParts), flags=re.I
            )
        if hasattr(self, "mutations"):
            mutation_objs = []
            for mut in self.mutations:
                mutation_objs.append(_Mutation(mut))
            self.mutations = mutation_objs
        else:
            self.mutations = []
        if hasattr(self, "substitutions"):
            sub_objs = []
            for sub in self.substitutions:
                sub_objs.append(_Substitution(sub))
            self.substitutions = sub_objs
        else:
            self.substitutions = []

    def url_from_query(self, query):
        """Apply schema to the given query to generate a URL.
        
        Returns the URL, or None if the query does not match
        the schema.""" 
        if hasattr(self, "broadRegexParts"):
            regex_source = self.broadRegexParts
        else:
            regex_source = self.regexParts
        regex_str = "".join(regex_source)
        match = re.search(re.compile(regex_str, flags=re.I), query)
        if match:
            return self._url_from_match(match)
        else:
            return None
    
    def insert_links(self, text):
        """Add <a> elements wherever the schema recognizes a citation.

        Tries to avoid modifying citations that are already inside
        <a> elements, but may not always be successful. If multiple
        schemas have overlapping regexes, it may be a problem."""
        regex_str = r'(?<!class="%s"\>)%s(?!\</a\>)' % (
            self.link_class,
            "".join(self.regexParts),
        )
        regex = re.compile(regex_str)
        return re.sub(regex, self._get_link_element, text)

    def _url_from_match(self, match):
        keys = match.groupdict()
        if hasattr(self, "defaults"):
            for default in self.defaults:
                keys[default] = self.defaults[default]
        for mut in self.mutations:
            for key in keys:
                if key != mut.key or keys[key] is None:
                    continue
                keys[mut.key] = mut._mutate(keys[key])
        for sub in self.substitutions:
            keys = sub._substitute(keys)
        url = """"""
        for part in self.URLParts:
            for key in keys:
                if not keys[key]:
                    continue
                part = part.replace("{%s}" % key, keys[key])
            missing_value = re.search("\{.+\}", part)
            if not missing_value:
                url += part
        return url

    def _get_link_element(self, match):
        text = '<a href="%s" class="%s">%s</a>' % (
            self._url_from_match(match),
            self.link_class,
            match.group(0),
        )
        return text


class _Mutation:
    """
    Text filters to apply to an individual regex capture group.

    A mutation can be used to process the text from a capture group.
    Mutations are applied before substutions, so they can normalize
    input for substitutions as well as for URL construction.

    For more information, see citation-schemas.yml"""

    def __init__(self, ydict: dict):
        self.__dict__ = ydict

    def _mutate(self, key: str):
        if hasattr(self, "omit"):
            key = re.sub(re.compile(self.omit), "", key)
        if hasattr(self, "splitter") and hasattr(self, "joiner"):
            parts = re.split(re.compile(self.splitter), key)
            parts = list(filter(None, parts))
            key = self.joiner.join(parts)
        if hasattr(self, "case"):
            if self.case == "upper":
                key = key.upper()
            elif self.case == "lower":
                key = key.lower()
        return key


class _Substitution:
    def __init__(self, ydict: dict):
        self.__dict__ = ydict

    def _substitute(self, keys: dict):
        key = keys[self.inputKey]
        if not key:
            return
        key = self.index.get(key)
        if key:
            if hasattr(self, "outputKey"):
                keys[self.outputKey] = key
            else:
                keys[self.inputKey] = key
        elif (
            not hasattr(self, allowUnmatched) or self.allowUnmatched is not True
        ):
            raise KeyError(
                "%s %s is out of index" % (self.inputKey, keys[self.inputKey])
            )
        return keys

###################################################
# setup
###################################################

# load citation schemas
schemas = []
# with open("citation-schemas.yml", "r") as f:
#     yaml_nodes = safe_load(f)
yaml_path = Path(__file__).parent.absolute() / 'citation-schemas.yml'
yaml_nodes = safe_load(yaml_path.read_text())
for node in yaml_nodes:
    schemas.append(Schema(node))

###################################################
# module functions
###################################################

def insert_links(text):
    """
    Returns a version of input text where all citations are hyperlinks.

    Uses case-sensitive regex matching based on each schema's default
    regex. Replaces each match with an <a> element with an href to the
    proper URL, and the class "statutory-link".

    Does not handle overlapping regexes well."""
    for schema in schemas:
        text = schema.insert_links(text)
    return text


def lookup_query(query):
    """
    Look up the the appropriate URL for a single citation query.

    Uses case-insensitive regex matching, and uses each schema's
    more permissive ("broad") regex, if one is defined."""
    for schema in schemas:
        url = schema.url_from_query(query)
        if url:
            return url
    raise KeyError("'%s' doesn't match a known regex." % query)
