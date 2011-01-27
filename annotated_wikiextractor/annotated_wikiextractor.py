# -*- coding: utf-8 -*-
# =============================================================================
#  Version: 0.1 (Jan 26, 2010)
#  Author: Joachim Daiber (jo.daiber@fu-berlin.de)
# =============================================================================

# =============================================================================
#
# Copyright (C) 2011 Joachim Daiber
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# =============================================================================

import re
import json
import urllib

import wikiextractor

prefix = 'http://en.wikipedia.org/wiki/'

"""
An extention of a WikiDocument, which also contains the annotations
of DBPedia entities referenced in the text.

The serialization has been changed from XML to JSON. 
"""
class DBPediaWikiDocument (dict):
    
    __slots__ = ['default', 'id', 'url', 'text', 'annotations']
    
    def __init__(self, default=None):
        dict.__init__(self)
        self.default = default
    
    def fromWikiDocument(self, wiki_document):
        self["id"] = wiki_document.id,
        self["url"] = wiki_document.url
        self["text"] = wiki_document.text 

    def setAnnotations(self, annotations):
        self["annotations"] = annotations
        
    def __str__(self):
        return json.dumps(self) + "\n"

"""

"""
class DBPediaWikiExtractor (wikiextractor.WikiExtractor):

    def __init__(self):
        wikiextractor.WikiExtractor.__init__(self)

    def extract(self, wiki_document):
        annotations = []
        
        wiki_document = wikiextractor.WikiExtractor.extract(self, wiki_document)
        if not wiki_document: return None
        
        while (True):
            m = re.search('<a href="([^"]+)">([^>]+)</a>', wiki_document.text)
            if m is None:
                break
            
            if urllib.quote("#") not in m.group(1):
                annotations.append({
                    "id"    :   m.group(1), 
                    "label" :   m.group(2), 
                    "from"  :   m.start(), 
                    "to"    :   m.start() + len(m.group(2))
                })
            
            wiki_document.text = wiki_document.text[:m.start(0)] + m.group(2) + wiki_document.text[m.start(0)+len(m.group(0)):]
        
        dbpedia_wiki_document = DBPediaWikiDocument()
        dbpedia_wiki_document.fromWikiDocument(wiki_document)
        dbpedia_wiki_document.setAnnotations(annotations)

        return dbpedia_wiki_document

def main():
    wikiextractor.WikiExtractor = DBPediaWikiExtractor
    wikiextractor.main()
     
if __name__ == '__main__':
    main()