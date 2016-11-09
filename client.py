# -*- coding: utf-8 -*-
import json
import urllib


class Client(object):
    def __init__(self, api_version=1):
        self.base_url = 'http://www.splashbase.co/api/v{version}'.format(version=api_version)

    def by_id(self, image_id):
        image_url = self.base_url + '/images/%s' % image_id
        return self._fetch(image_url)

    @property
    def random(self):
        random_url = self.base_url + '/images/random'
        return self._fetch(random_url)

    @property
    def latest(self):
        random_url = self.base_url + '/images/latest'
        return self._fetch(random_url)

    def search(self, search_string):
        search_url = self.base_url + '/images/search' + self._dump_query_string(dict(query=search_string))
        return self._fetch(search_url)

    def source(self, source_id):
        sources_url = self.base_url + '/sources/%s' % source_id
        return self._fetch(sources_url)

    def _fetch(self, url):
        response = urllib.urlopen(url)
        return json.loads(response.read())

    def _dump_query_string(self, qs_dict):
        """Returns query string dumped from dict"""
        return '?' + '&'.join(['='.join(x) for x in qs_dict.items()])

