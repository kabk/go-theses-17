#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script searches information about this year’s theses and updates
the index with this information.
"""

from __future__ import unicode_literals

# These are the modules that we import, which we use for this script

# These modules are part of python:
from urllib2 import urlopen, HTTPError
from codecs import open
import json
import re
import sys

# And these we added ourselves (they are the folder opengraph and the file
# link_header.py respectively)
import opengraph
from link_header import parse_link_value

def get_slugs():
    url = "https://api.github.com/orgs/kabk/repos"
    repos = []

    """
    First we are going to connect with Github, and find out the names of all
    the theses of this year. ie, all the repositories in the `kabk` organisation
    that start with `govt-theses-16-`

    We use the ‘API’ of Github, a special version of the site that returns not
    web pages but data structures that can be easily re-used by scripts.
    """
    while url:
        print "fetching %s" % url
        res = urlopen(url)
        # The data is encoded in an exchange format called JSON
        # We can load this data into a variable so we can afterwards use it in python
        # In this case we know the JSON encodes a list so we can add it to the already
        # encoded lists.
        repos += json.load(res)

        print "fetched %s records in total" % len(repos)

        # http headers are metadata send along with each http response
        headers = dict(res.info())
        if 'link' in headers:
            # Github returns a maximum of 30 results at the time.
            # We need to request the next ‘page’ of results until we’ve read all.
            # Github uses a special header, `link`, to tell us where to find
            # the next page.
            # For this it uses the Link header, a format specified here:
            # http://tools.ietf.org/html/rfc5988
            # we use a bit of existing code to read in (‘parse’) these values (from `link_header.py`)
            links = parse_link_value(headers['link'])
            # this gives us a response like
            # {'https://api.github.com/organizations/8778805/repos?page=2' : {'rel' : 'next'}}
            for key, value in links.iteritems():
                # if there is a next page this is the url we need
                if value['rel'] == 'next':
                    url = key
                    break
                # if we are at the before-last set of results, there is no `next` page, but a `last` page:
                if value['rel'] == 'last':
                    url = key
                    break
            else:
                url = None
        else:
            url = None

    # Sort the repositories (for now, alphabetically by repository name)
    repos.sort(key=lambda x: x['name'])

    # filter the repositories so we only have those starting with `go-theses-17-`
    slugs = [r['name'] for r in repos if r['name'].startswith('go-theses-17-')]
    return slugs

def scrape_info(slugs):
    # Now we are going to do the actual scraping, i.e. finding out information about
    # the websites from the websites themselves

    theses = []
    default_values = {
        'image' : '',
        'title' : 'Specify title with &lt;title&gt; tag',
        'creator' : 'Specify creator with &lt;meta property="dc:creator"&gt; tag',
        'description' : 'Specify description with &lt;meta name="description"&gt; tag',
    }
    for slug in slugs:
        url = 'http://kabk.github.io/%s/' % slug
        print "parsing %s:" % url
        try:
            g = opengraph.OpenGraph(url=url, scrape=True)
        except HTTPError as e:
            print "%s gives error %s" % (url, e)
        d = json.loads(g.to_json())
        d['slug'] = slug
        d['url'] = url
        for key in ['image', 'title', 'creator', 'description']:
            if key not in d:
                d[key] = default_values[key]
        theses.append(d)

    return theses

def write_html(theses):
    thesis_template = """
<div class="preview">
    <figure>
        <a href="{url}"><img src="{image}"/></a>
    </figure>
    <h2><a href="{url}">{url} {title}</a></h2>
    <h3>{creator}</h3>
    <p>{description} <a href="{url}">Continue reading…</a></p>
</div>
"""
    
    # For each of the thesis, render the template with the information we found
    thesis_html = ""
    for thesis in theses:
        thesis_html += thesis_template.format(**thesis)

    # Open the current index page and read in the current contents
    current_file = open('index.html', 'r', 'utf-8')
    current_html = current_file.read()
    current_file.close()

    # Replace the part of the page that has the list of theses
    # with the newly generated HTML
    # (Note: we use search and replace with regular expressions—
    # this is bad form; one is supposed to use a ‘parser’).
    modified_html = re.sub(r'<section id="theses">.*</section>',
                    '<section id="theses">%s</section>' % thesis_html,
                    current_html, flags=re.M | re.S)

    # Write the modified HTML file back onto disk
    modified_file = open('index.html', 'w', 'utf-8')
    modified_file.write(modified_html)
    modified_file.close()

if __name__ == "__main__":
    write_html(scrape_info(get_slugs()))
    # print scrape_info(["govt-theses-16-caroline-langendoen"])
