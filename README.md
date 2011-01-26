# A Wikipedia Plain Text Extractor with Link Annotations

This project is a simple wrapper around the Wikipedia Extractor by [Medialab](http://medialab.di.unipi.it/wiki/Wikipedia_Extractor). It generates a JSON object for each article. The JSON object contains the id, title and plain text of the article, as well as annotations of article links in the text.

## Annotations

Annotations are sequentially stored in a list. A single annotation has the following form:

	{"to": 1165, "from": 1156, "id": "Socialist", "label": "socialist"}
	
* `from`: start positon of the string
* `to`: end position of the string
* `id`: Wikipedia/DBPedia article name
* `label`: the label of the link in the text (what part of the text was linked)

