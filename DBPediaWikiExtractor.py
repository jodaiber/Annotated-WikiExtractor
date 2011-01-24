# -*- coding: utf-8 -*-
import re
import json

from wikiextractor import *

"""
An extention of a WikiDocument, which also contains the annotations
of DBPedia ids referenced in the text.

The serialization has been changed from XML to JSON. 
"""

class DBPediaWikiDocument (dict):
    
    __slots__ = ['default', 'id', 'url', 'text', 'annotations']
    
    def __init__(self, default=None):
        dict.__init__(self)
        self.default = default
    
    def fromWikiDocument(self, wiki_document):
        self["id"] = wiki_document.id
        self["url"] = wiki_document.url
        self["text"] = wiki_document.text

    def setAnnotations(self, annotations):
        self["annotations"] = annotations
        
    def __str__(self):
        return json.dumps(self) + "\n"  #'<doc id="%d" url="%s">\n%s\n</doc>\n' % (self.id, self.url, self.text)


class DBPediaWikiExtractor (WikiExtractor):

    def __init__(self):
        WikiExtractor.__init__(self)

    def extract(self, wiki_document):
        annotations = []
        
        wiki_document = WikiExtractor.extract(self, wiki_document)
        
        m = re.search('<a href="([^"]+)">([^>]+)</a>', wiki_document.text)
        while (m != None):
            annotations.append({"id" : m.group(1), "label" : m.group(2), "offset" : m.start(), "length" : len(m.group(2))})
            wiki_document.text = wiki_document.text[:m.start(0)] + m.group(2) + wiki_document.text[m.start(0)+len(m.group(0)):]
            m = re.search('<a href="([^"]+)">([^>]+)</a>', wiki_document.text)
        
        dbpedia_wiki_document = DBPediaWikiDocument()
        dbpedia_wiki_document.fromWikiDocument(wiki_document)
        dbpedia_wiki_document.setAnnotations(annotations)
        
        print dbpedia_wiki_document
        
        return dbpedia_wiki_document

def main():
    wiki_extractor = DBPediaWikiExtractor()
    
    compress = False
    file_size = 500 * 1024
    output_dir = '.'
    output_splitter = OutputSplitter(compress, file_size, output_dir)
    process_data(sys.stdin, wiki_extractor, output_splitter)

    output_splitter.close()

if __name__ == '__main__':
    main()