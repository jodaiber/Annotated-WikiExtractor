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
    
    script_name = os.path.basename(sys.argv[0])
    try:
        long_opts = ['help', 'usage', 'compress', 'bytes=', 'output=']
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'cb:o:', long_opts)
    except getopt.GetoptError:
        show_usage(sys.stderr, script_name)
        show_suggestion(sys.stderr, script_name)
        sys.exit(1)

    compress = False
    file_size = 500 * 1024
    output_dir = '.'

    for opt, arg in opts:
        if opt == '--help':
            show_help()
            sys.exit()
        elif opt == '--usage':
            show_usage(sys.stdout, script_name)
            sys.exit()
        elif opt in ('-c', '--compress'):
            compress = True
        elif opt in ('-b', '--bytes'):
            try:
                if arg[-1] in 'kK':
                    file_size = int(arg[:-1]) * 1024
                elif arg[-1] in 'mM':
                    file_size = int(arg[:-1]) * 1024 * 1024
                else:
                    file_size = int(arg)
                if file_size < 200 * 1024: raise ValueError()
            except ValueError:
                show_size_error(script_name, arg)
                sys.exit(2)
        elif opt in ('-o', '--output'):
            if os.path.isdir(arg):
                output_dir = arg
            else:
                show_file_error(script_name, arg)
                sys.exit(3)

    wiki_extractor = DBPediaWikiExtractor()
    output_splitter = OutputSplitter(compress, file_size, output_dir)
    process_data(sys.stdin, wiki_extractor, output_splitter)

    output_splitter.close()

if __name__ == '__main__':
    main()