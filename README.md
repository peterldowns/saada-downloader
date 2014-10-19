# SAADA Downloader

The [South African Digital Archive](http://www.saadigitalarchive.org/) hosts
great content, but only allows reading via an in-browser tool. This repository
contains a CLI tool (`download.py`) for downloading content from SAADA in the
form of a PDF.

# Requirements
Python requirements are documented in `requirements.txt`. For image
manipulation there are a few dependencies that can be installed via `apt-get`:

```bash
$ sudo apt-get install python-dev libjpeg-dev
```
# Usage

Running is very simple. Once the `python-dev` and `libjpeg-dev` packages
are installed, you run:

```bash
$ make
```

A new virtual environment will be created and all of the Python requirements
will be installed. Then, the download script is run.

The download script asks for two pieces of information:

### URL to the first page's image

This should be the URL to the image file containing the first page of content.
You can get this URL like so:

1. Visit the SAADA overview page for your content (for example:
   http://www.saadigitalarchive.org/item/20110901-312).
2. Right-click on the small image on the left side of the page and select "Copy
   Link." You should have a link that looks like
   `http://s3.amazonaws.com/saada-online/objects/2012-00/item-freehindusthan-v1-n1-001.jpg`
3. Paste that link in to the command line and press enter.

### The output file's name

This should be a filename ending in `.pdf`, the name of a new PDF file to be
created. The default is `output.pdf`.

You can run the script again the same way as the first time:
```bash
$ make
```
