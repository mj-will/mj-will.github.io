TALKS := $(wildcard _talks/*.md)
PYTHON ?= python3
PUBLICATION_SOURCES := page_generators/references.bib page_generators/bibtex_to_markdown.py
PUBLICATION_STAMP := .publications.stamp

.PHONY: all talkmap publications serve

all: talkmap publications

talkmap: talkmap/map.html

talkmap/map.html talkmap/talks.js: $(TALKS) page_generators/talkmap.py
	$(PYTHON) page_generators/talkmap.py _talks

publications: $(PUBLICATION_STAMP)

$(PUBLICATION_STAMP): $(PUBLICATION_SOURCES)
	$(PYTHON) page_generators/bibtex_to_markdown.py page_generators/references.bib
	touch $(PUBLICATION_STAMP)

serve:
	bundle exec jekyll serve
