# Asuntojen.hintatiedot.fi scraper

A scraper that's very much in progress. Pulls data from
[asuntojen.hintatiedot.fi](http://asuntojen.hintatiedot.fi) and
displays it in a table. Nothing fancy so far.

## To run the scraper

Clone the project, cd into the directory you cloned the project into
and run `python -m CGIHTTPServer`.

## Limitations

Currently does not take any user input but only scrapes based on the
parameters defined in `cgi-bin/scraper.py`. This is obviously not
the way things would end up being in the long run but hey, this is
just the first alpha-alpha version (more of a [PoC](http://en.wikipedia.org/wiki/Proof_of_concept).

## Why is the scraper in cgi-bin?

The reason for `scraper.py` being in <kbd>cgi-bin</kbd>     
directory is since otherwise CGIHTTPServer will not execute
the script. For production, there's no need for this limitation.
I wanted a simple testing environment and hence the implementation
