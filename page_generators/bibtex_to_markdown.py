import arxiv
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import homogenize_latex_encoding
import sys
import re
from pathlib import Path
import mdtex2html


def slugify(title):
    # Create a URL-friendly slug
    title = title.lower()
    title = re.sub(r"[^\w\s-]", "", title)
    title = re.sub(r"\s+", "-", title)
    return title


def make_citation(entry):
    authors = entry.get("author", "").replace("{", "").replace("}", "")
    year = entry.get("year", "")
    title = entry.get("title", "").replace("{", "").replace("}", "")
    journal = entry.get("journal", entry.get("venue", ""))
    volume = entry.get("volume", "")
    number = entry.get("number", "")
    pages = entry.get("pages", "")

    citation = f"{authors} ({year}). &quot;{title}.&quot; <i>{journal}</i>"
    if volume:
        citation += f". {volume}"
        if number:
            citation += f"({number})"
    if pages:
        citation += f": {pages}"
    citation += "."
    return citation


def main(bib_file):
    # Load your .bib file
    output_dir = Path("../_publications")
    output_dir.mkdir(exist_ok=True)

    # Read bibtex
    with open(bib_file, encoding="utf-8") as bibtex_file:
        parser = BibTexParser()
        parser.customization = homogenize_latex_encoding
        bib_database = bibtexparser.load(bibtex_file, parser=parser)

    client = arxiv.Client()

    for entry in bib_database.entries:
        title = entry.get("title", "Untitled").replace("{", "").replace("}", "")
        year = entry.get("year", "2025")
        month = entry.get("month", "01").zfill(2)
        slug = slugify(title)
        arxiv_id = entry.get("eprint", "")
        arxiv_url = f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else ""

        # Fetch abstract from arXiv if available

        if arxiv_id:
            search = arxiv.Search(id_list=[arxiv_id])
            paper = next(client.results(search), None)
            if paper:
                abstract = paper.summary.replace("\n", " ")
            else:
                abstract = ""
        else:
            abstract = entry.get("abstract", "").replace("\n", " ")

        abstract = mdtex2html.convert(abstract)

        paper_md = f"""---
title: "{title}"
collection: publications
category: manuscripts
permalink: /publication/{arxiv_id if arxiv_id else f'{year}-{slug}'}/
date: {year}-{month}-01
excerpt: ''
venue: '{entry.get("journal", "")}'
arxivurl: '{arxiv_url}'
---
{abstract}
"""
        # Save the markdown
        md_file = output_dir / f"{year}-{slug}.md"
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(paper_md)

    print(f"Markdown files generated in {output_dir}/")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "references.bib" )
