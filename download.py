#!/usr/bin/env python
# coding: utf-8
import click
import re
import requests
from PIL import Image
from PyPDF2 import PdfFileMerger
from StringIO import StringIO

@click.command()
@click.option('--first-image-url',
              prompt='URL to the first page image.')
@click.option('--output-name',
              prompt='The file name where to save the PDF.',
              default='output.pdf')
def saada_to_pdf(first_image_url, output_name):
  print 'Analyzing: {}'.format(repr(first_image_url))

  match = re.match(r'(?P<base>.*)-001\.(?P<extension>.*)$', first_image_url)
  if not match:
    raise Exception('Invalid URL structure: {}'.format(repr(first_image_url)))

  #url_template = 'http://s3.amazonaws.com/saada-online/objects/2012-08/item-ih-1921-05-{page}.jpg'
  match_dict = match.groupdict()
  url_template = '%s-{page}.%s' % (match_dict['base'], match_dict['extension'])
  pdfs = []
  page = 0
  while True:
    page += 1
    page_str = str(page).zfill(3) # Changes 1 to '001', 18 to '018'.
    page_request = requests.get(url_template.format(page=page_str), stream=True)
    if page_request.status_code != 200:
      print 'Reached the last page of content.'
      break

    # Save the page contents as an in-memory image.
    fd_in = StringIO()
    for chunk in page_request.iter_content(1024):
      fd_in.write(chunk)

    # Load the content image into PIL for transformation to PDF.
    fd_in.seek(0)
    image = Image.open(fd_in)

    # Save the image to an in-memory PDF file.
    fd_out = StringIO()
    image.save(fd_out, format='PDF')
    fd_out.seek(0) # Return to the 0th byte so that it can be read.

    # Add this pdf of content to the list of pdfs to be merged.
    pdfs.append(fd_out)

  # Merge the in-memory PDFs to a single output PDF on disk.
  merger = PdfFileMerger()
  map(merger.append, pdfs)
  with open(output_name, 'wb') as output_fd:
    merger.write(output_fd)

  print 'Wrote {} pages of content to PDF: {}'.format(page - 1, output_name)

if __name__ == '__main__':
  saada_to_pdf()
