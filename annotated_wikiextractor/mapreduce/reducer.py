# -*- coding: utf-8 -*-

import sys
import os
import marshal

#Add the folder containing annotated_wikiextractor to the PYTHON_PATH, so
#it can be executed in hadoop 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"../..")))

#Import annotated_wikiextractor from the path added in the last step
import annotated_wikiextractor
from annotated_wikiextractor.annotated_wikiextractor import AnnotatedWikiExtractor

#Use the standard AnnotatedWikiExtractor
wiki_extractor = AnnotatedWikiExtractor()

for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    page = marshal.loads(line)
    wiki_document = annotated_wikiextractor.wikiextractor.extract_document(page)
    annotated_wiki_document = wiki_extractor.extract(wiki_document)
    print "%s\t%s" % (annotated_wiki_document["url"].replace(annotated_wikiextractor.wikiextractor.prefix, ""), annotated_wiki_document)