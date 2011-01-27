import json
import unittest

from annotated_wikiextractor.annotated_wikiextractor import \
    AnnotatedWikiExtractor
from annotated_wikiextractor.wikiextractor import WikiExtractor
import annotated_wikiextractor.wikiextractor

class TestAnnotatedWikiExtractor(unittest.TestCase):
    def setUp(self):
        
        annotated_wikiextractor.wikiextractor.prefix = 'http://en.wikipedia.org/wiki/'
        self.annotated_wikiextractor = AnnotatedWikiExtractor()
        self.wikiextractor = WikiExtractor()
    
    """
    Test the extraction process by comparing the result with a pre-processed result
    serialized in the file singlepage_original.xml
    
    This test targets the script in wikiextractor.py
    """
    def test_extract_original(self):
        page = map(lambda x: x.rstrip("\n"), open("singlepage_wikien.txt", "r").readlines())
        wiki_document = annotated_wikiextractor.wikiextractor.extract_document(page)
        wiki_document = self.wikiextractor.extract(wiki_document)
        
        #open("singlepage_original.xml", "w").write(wiki_document.__str__())
        self.assertEquals(open("singlepage_original.xml").read(), wiki_document.__str__())   

    
    """
    Test the extraction process by comparing the result with a pre-processed result
    serialized in the file singlepage_annotated.json
    
    This test targets the script in annotated_wikiextractor.py
    """
    def test_extract_annotated(self):
        page = map(lambda x: x.rstrip("\n"), open("singlepage_wikien.txt", "r").readlines())
        wiki_document = annotated_wikiextractor.wikiextractor.extract_document(page)
        annotated_wiki_document = self.annotated_wikiextractor.extract(wiki_document)
        #json.dump(json.loads(str(annotated_wiki_document)), open("singlepage_annotated.json", "w"))
        self.assertEquals(open("singlepage_annotated.json").read(), json.dumps(annotated_wiki_document))   

if __name__ == '__main__':
    unittest.main()