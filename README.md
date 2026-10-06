# michaeljwilliams.me

This is the git repo for my personal website.
It has gone through a few iterations but the current version is based on the [Academic Pages template](https://github.com/academicpages/academicpages.github.io).

## Rebuilding publications

After editing `page_generators/references.bib`, run `pixi run publications`.
Pixi installs the dependencies and runs the Makefile's `publications` target,
which fetches abstracts from arXiv and writes the pages to `_publications/`.
To force a rebuild without changing the bibliography, run `pixi run make -B publications`.

## Building the site

Run `pixi run build` to install the Ruby dependencies and build the Jekyll site
into `_site/`. Ruby and the build tools are managed by Pixi; gems are installed
inside `.pixi/`.

Run `pixi run serve` to preview the site at http://127.0.0.1:4000/.
Jekyll rebuilds when site files change. Stop the server with Ctrl+C.

Publication entries can set `category` in `page_generators/references.bib`;
entries without it default to `manuscripts`.

## Rebuilding the talk map

Run `pixi run talkmap` after updating talks in `_talks/`.
To force a rebuild, run `pixi run make -B talkmap`.
New locations are geocoded online; previously resolved locations use the cache.
