"""
Aberdeen Python dojo of 26th November 2014

@author: Daniel Blasco
"""
import sys
import json
import urllib2
from xml.etree import ElementTree


def fetch_rss_file(url):
    print "Retrieving RSS feed file from {}".format(url)

    # https://docs.python.org/2/howto/urllib2.html
    return urllib2.urlopen(url).read()


def parse_xml(text):
    items = []

    # With ElementTree parse XML from text format to a tree of python elements
    # https://docs.python.org/2/library/xml.etree.elementtree.html#tutorial
    root = ElementTree.fromstring(text)

    # Use XPath expressions to find all the items in the XML tree
    # https://docs.python.org/2/library/xml.etree.elementtree.html#elementtree-xpath
    for xml_item in root.findall('.//item'):
        item = {}  # put all the data related to a item in a dictionary

        # All RSS 2.0 needs to have for sure title, description and link.
        # But it could have more properties which we don't know, like dates and images
        # We iterate over all the elements to extract all the information
        for child in xml_item:
            item[child.tag] = child.text  # FIXME: Image elements are not extracted properly here

        items.append(item)

    return items


def main(url):
    try:
        text = fetch_rss_file(url)
    except Exception, e:
        print "Error retrieving url: {}".format(e)
        sys.exit(1)  # Exit with error

    # Extract data structures from the retrieved text
    items = parse_xml(text)

    # Just using JSON here to pretty print the result
    # We could store the items in a database, generate HTML, create an API, etc...
    print json.dumps(items, indent=2)


if __name__ == "__main__":
    main("http://www.aberdeencity.gov.uk/accapps/rss/EventRSS.aspx")