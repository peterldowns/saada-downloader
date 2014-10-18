#!/usr/bin/env python
# coding: utf-8
import requests
import json
from StringIO import StringIO
from PIL import Image
from PyPDF2 import PdfFileMerger, parse_filename_page_ranges


def main():
  url_template = 'http://s3.amazonaws.com/saada-online/objects/2012-08/item-ih-1921-05-{page}.jpg'
  page = 1
  image_files = []
  while True:
    page_str = str(page).zfill(3)
    page_request = requests.get(url_template.format(page=page_str), stream=True)

    if page_request.status_code != 200:
      print 'exiting due to status code', page_request.status_code
      break

    filename = 'page_{}.jpg'.format(page_str)
    fd_in = StringIO()
    fd_out = StringIO()
    for chunk in page_request.iter_content(1024):
      fd_in.write(chunk)
    print 'saved file: {}'.format(filename)
    fd_in.seek(0)
    image = Image.open(fd_in)
    image.save(fd_out, format='PDF')
    fd_out.seek(0) # Return to the 0th byte so that it can be read.
    image_files.append(fd_out)
    page += 1

  merger = PdfFileMerger()
  for i, pdf_fd in enumerate(image_files):
    merger.append(pdf_fd) # TODO(peter): pages=page_range?
  out_pdf = open('output.pdf', 'wb')
  merger.write(out_pdf)


if __name__ == '__main__':
  main()
