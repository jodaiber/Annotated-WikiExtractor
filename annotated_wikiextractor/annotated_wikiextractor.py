# -*- coding: utf-8 -*-
# =============================================================================
#  Version: 0.1 (Jan 26, 2010)
#  Author: Joachim Daiber (jo.daiber@fu-berlin.de)
# =============================================================================
from multiprocessing import Pool

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

"""Annotated Wikipedia Extractor:
Extracts and cleans text from Wikipedia database dump and stores output in a
number of files of similar size in a given directory. Each file contains
several documents in JSON format (one document per line) with additional
annotations for the links in the article.

Usage:
  annotated_wikiextractor.py [options]

Options:
  -k, --keep-anchors    : do not drop annotations for anchor links (e.g. Anarchism#gender)
  -c, --compress        : compress output files using bzip2 algorithm
  -b ..., --bytes=...   : put specified bytes per output file (500K by default)
  -o ..., --output=...  : place output files in specified directory (current
                          directory by default)
  --help                : display this help and exit
  --usage               : display script usage
"""



import re
import json
import urllib
import getopt
import sys
import os

import wikiextractor

prefix = 'http://en.wikipedia.org/wiki/'
number_of_workers = 2
keep_anchors = False

"""
An extention of a WikiDocument, which also contains the annotations
of DBPedia entities referenced in the text.

The serialization has been changed from XML to JSON. 
"""
class AnnotatedWikiDocument (dict):
    
    __slots__ = ['default', 'id', 'url', 'text', 'annotations']
    
    def __init__(self, wiki_document, default=None):
        self.fromWikiDocument(wiki_document)
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
An extended version of the WikiExtrator. Output is in JSON format and annotations
are added for links in the article. See README.md for more information about the
JSON format.
"""
class AnnotatedWikiExtractor (wikiextractor.WikiExtractor):

    def __init__(self):
        wikiextractor.prefix = 'http://en.wikipedia.org/wiki/'
        wikiextractor.WikiExtractor.__init__(self)

    def extract(self, wiki_document):
        annotations = []
        
        #Extract the article using the general WikiExtractor:
        wiki_document = wikiextractor.WikiExtractor.extract(self, wiki_document)
        if not wiki_document: return None
        
        #This int is used to keep track of the difference between the original article with <a href="..">
        #links and the new article that only contains the label of the link.
        deltaStringLength = 0
        
        #As a first step, find all links in the article, save their positions into the annotations object
        ms = re.finditer('<a href="([^"]+)">([^>]+)</a>', wiki_document.text)
        
        for m in ms:              
            if urllib.quote("#") not in m.group(1) or keep_anchors:
                annotations.append({
                    "uri"    :   m.group(1), 
                    "surface_form" :   m.group(2), 
                    "offset"  :   m.start() - deltaStringLength
                })
            
            deltaStringLength += len(m.group(0)) - len(m.group(2))
                
        #As a second step, replace all links in the article by their label
        wiki_document.text = re.sub('<a href="([^"]+)">([^>]+)</a>', lambda m: m.group(2), wiki_document.text)
        
        #Create a new AnnotatedWikiDocument
        annotated_wiki_document = AnnotatedWikiDocument(wiki_document)
        annotated_wiki_document.setAnnotations(annotations)

        #Return the AnnotatedWikiDocument
        return annotated_wiki_document

def process_page(page, wiki_extractor):
    wiki_document = wikiextractor.extract_document(page)
    if not wiki_document: return

    wiki_document = wiki_extractor.extract(wiki_document)
    if not wiki_document: return

    return wiki_document.__str__().encode('utf-8')

def process_data(input_file, wiki_extractor, output_splitter):
    
    # Set up pool of worker processes
    pool = Pool(processes=number_of_workers)
    
    page = []
    for line in input_file:
        line = line.decode('utf-8').strip()
        if line == '<page>':
            page = []
        elif line == '</page>':
            pool.apply_async(process_page, [page, wiki_extractor], callback=(lambda x: output_splitter.write(x) if x is not None else None))
        else:
            page.append(line)

    # Close the process pool
    pool.close()
    
    # Wait for the worker processes to finish
    pool.join()


def main():
    script_name = os.path.basename(sys.argv[0])

    try:
        long_opts = ['help', 'usage', 'compress', 'bytes=', 'output=', 'keep-anchors']
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'kcb:o:', long_opts)
    except getopt.GetoptError:
        wikiextractor.show_usage(sys.stderr, script_name)
        wikiextractor.show_suggestion(sys.stderr, script_name)
        sys.exit(1)

    compress = False
    file_size = 500 * 1024
    output_dir = '.'

    for opt, arg in opts:
        if opt == '--help':
            show_help()
            sys.exit()
        elif opt == '--usage':
            wikiextractor.show_usage(sys.stdout, script_name)
            sys.exit()
        elif opt in ('-k', '--keep-anchors'):
            keep_anchors = True
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
                wikiextractor.show_size_error(script_name, arg)
                sys.exit(2)
        elif opt in ('-o', '--output'):
            if os.path.isdir(arg):
                output_dir = arg
            else:
                wikiextractor.show_file_error(script_name, arg)
                sys.exit(3)

    if len(args) > 0:
        wikiextractor.show_usage(sys.stderr, script_name)
        wikiextractor.show_suggestion(sys.stderr, script_name)
        sys.exit(4)

    wiki_extractor = AnnotatedWikiExtractor()
    output_splitter = wikiextractor.OutputSplitter(compress, file_size, output_dir)
    process_data(sys.stdin, wiki_extractor, output_splitter)

    output_splitter.close()

def show_help():
    print >> sys.stdout, __doc__,
    
if __name__ == '__main__':
    main()