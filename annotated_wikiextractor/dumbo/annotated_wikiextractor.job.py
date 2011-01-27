import annotated_wikiextractor.wikiextractor
from annotated_wikiextractor.annotated_wikiextractor import \
    AnnotatedWikiExtractor
    
wiki_extractor = AnnotatedWikiExtractor()

def mapper(key, value):
    wiki_document = annotated_wikiextractor.wikiextractor.extract_document(value)
    annotated_wiki_document = wiki_extractor.extract(wiki_document)
    yield key, json.dumps(annotated_wiki_document)

def reducer(key, values):
    yield key, values[0]

if __name__ == "__main__":
    import dumbo
    dumbo.run(mapper, reducer)