# A Wikipedia Plain Text Extractor with Link Annotations

This project is a simple wrapper around the Wikipedia Extractor by [Medialab](http://medialab.di.unipi.it/wiki/Wikipedia_Extractor). It generates a JSON object for each article. The JSON object contains the id, title and plain text of the article, as well as annotations of article links in the text.

# Output

## JSON of a single article

	{"url": "http://en.wikipedia.org/wiki/Anarchism", 
	 "text": "Anarchism.\nAnarchism is a political philosophy which considers the state 
		undesirable, unnecessary and harmful, and instead promotes a stateless society, or 
		anarchy. It seeks to diminish ...", 
	 "id": 12, 
	 "annotations": [
		{"to": 46, "from": 26, "id": "Political_philosophy", "label": "political philosophy"}, 
		{"to": 72, "from": 67, "id": "State_(polity)", "label": "state"}, 
		{"to": 163, "from": 156, "id": "Anarchy", "label": "anarchy"}, 
		...
	]}


## Annotations

Annotations are stored in an ordered list. A single annotation has the following form:

	{"to": 1165, "from": 1156, "id": "Socialist", "label": "socialist"}
	
* `from`: start positon of the string
* `to`: end position of the string
* `id`: Wikipedia/DBPedia article name
* `label`: the label of the link in the text (what part of the text was linked)

# Usage

The extractor can be run from the Terminal or on a Hadoop MapReduce
cluster.

## Bash

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

To convert the whole Wikipedia Dump to plain text, use the following command:

	bzip2 -dc enwiki-20110115-pages-articles.xml.bz2 | python annotated_wikiextractor.py -o extracted/

If you want the output files to be compressed, use the -c option:

	bzip2 -dc enwiki-20110115-pages-articles.xml.bz2 | python annotated_wikiextractor.py -co extracted/

## Hadoop MapReduce

To run the extractor on a Hadoop MapReduce cluster, the Hadoop Streaming API can be used.

	mapreduce jodaiber$ hadoop jar $HADOOP_PATH/contrib/streaming/hadoop-0.20.2-streaming.jar \
	  -file ./mapper.py -mapper ./mapper.py \
	  -inputreader "StreamXmlRecordReader,begin=<page>,end=</page>" \
	  -input ../test/resources/wikien.xml \
	  -output out

In this case, the XML Dump must be available in HDFS (or locally, as is
the case above) in its uncompressed form. The output will be written to
the folder specified in the `-output` parameter and will have the following format:

	Anarchism	{...}
	Anaphora	{...}
	[...]
