TALKS := $(wildcard _talks/*.md)
PUBLICATION_SOURCES := page_generators/references.bib page_generators/bibtex_to_markdown.py
PUBLICATION_STAMP := .publications.stamp

.PHONY: all talkmap publications serve

all: talkmap publications

talkmap: talkmap/map.html

talkmap/map.html talkmap/talks.js: $(TALKS) page_generators/talkmap.py
	python page_generators/talkmap.py _talks

publications: $(PUBLICATION_STAMP)

$(PUBLICATION_STAMP): $(PUBLICATION_SOURCES)
	python page_generators/bibtex_to_markdown.py page_generators/references.bib
	touch $(PUBLICATION_STAMP)

serve:
	bundle exec jekyll serve
