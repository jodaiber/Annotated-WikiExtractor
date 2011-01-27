import unittest
from annotated_wikiextractor.annotated_wikiextractor import DBPediaWikiExtractor
import annotated_wikiextractor.wikiextractor
import sys
import json

class TestAnnotatedWikiExtractor(unittest.TestCase):
    def setUp(self):
        annotated_wikiextractor.wikiextractor.prefix = 'http://en.wikipedia.org/wiki/'
        self.wikiextractor = DBPediaWikiExtractor()
        
    """
    Test the extraction process by comparing the result with a pre-processed result
    serialized in the file singlepage_annotated.json
    """
    def test_extract(self):
        page = map(lambda x: x.rstrip("\n"), open("singlepage_wikien.txt", "r").readlines())
        wiki_document = annotated_wikiextractor.wikiextractor.extract_document(page)
        annotated_wiki_document = self.wikiextractor.extract(wiki_document)
        #json.dump(json.loads(str(annotated_wiki_document)), open("singlepage_annotated.json", "w"))
        self.assertEquals(open("singlepage_annotated.json").read(), json.dumps(annotated_wiki_document))   

if __name__ == '__main__':
    unittest.main()