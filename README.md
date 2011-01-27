# A Wikipedia Plain Text Extractor with Link Annotations

This project is a simple wrapper around the Wikipedia Extractor by [Medialab](http://medialab.di.unipi.it/wiki/Wikipedia_Extractor). It generates a JSON object for each article. The JSON object contains the id, title and plain text of the article, as well as annotations of article links in the text.

## Annotations

Annotations are sequentially stored in a list. A single annotation has the following form:

	{"to": 1165, "from": 1156, "id": "Socialist", "label": "socialist"}
	
* `from`: start positon of the string
* `to`: end position of the string
* `id`: Wikipedia/DBPedia article name
* `label`: the label of the link in the text (what part of the text was linked)

## Usage

As this is only an extention of the orgininal WikiExtractor, the usage is more or less the same.

	$ python annotated_wikiextractor.py --help
	Annotated Wikipedia Extractor:
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