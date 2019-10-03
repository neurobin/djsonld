import requests
import unittest
from django.http.response import HttpResponseBase
from django.test.client import RequestFactory
from urllib.parse import urlparse
import re
import json
from .core import *


jsonld_author0 = {
    "@type": "Person",
    "name": "Md. Jahidul Hamid",
    "sameAs" : [ "https://github.com/neurobin",
    "https://bitbucket.org/neurobin",
    "https://www.facebook.com/jahidul.hamid",
    "https://twitter.com/jahidulhamid",
    "https://www.linkedin.com/in/jahidulhamid"
    			],
    "address": {
      "@type": "PostalAddress",
      "addressCountry": "Bangladesh"
     },
    "email": "jahidulhamid@yahoo.com",
    "birthDate": "1992-11-25"
}
    
jsonld_organization0 = {
  	"@type": "Organization","name": "Neurobin",
  	"url": "https://neurobin.org",
   "description": "Neurobin is a technology organization specializing in software development for multiple platforms, contributing to the open source world, providing technical assistance and endorsing innovative technological endeavor.",
  	"logo": {
    "@type": "ImageObject",
    "url": "https://neurobin.org/img/nblogo_scsh.jpg",
    "width": "386",
    "height": "60"
  	 },
    "image": "https://neurobin.org/img/bin_h1.jpg",
  	"sameAs" : [ "https://www.facebook.com/neurobin.org/"],
  "address": {
    "@type": "PostalAddress",
    "addressCountry": "Bangladesh"
  },
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "technical support",
    "url": "https://neurobin.org/about/contact/"
  },
    "foundingDate": "2015",
    "founder": jsonld_author0,
}


jsonld_home0 = {
    "@context": "http://schema.org",
    "@type": "WebSite",
    "url":"https://neurobin.org",
    "name":"Neurobin",
    "alternateName":"Neurobin",
    "dateCreated":"07/11/2015 GMT",
    "thumbnailUrl": 'https://neurobin.org/img/nblogo_scsh.jpg',
    "genre":"Technology",
    "about": jsonld_organization0,
    "author": jsonld_author0,
}


def test_get_bread_crumb():
    rf = RequestFactory()
    request = rf.get('https://127.0.0.1/docs/android/time-picker-example?q=9')
    print(dir(request))

    page_conf = {
        'site_name': 'Neurobin',
        'jsonld_author': jsonld_author0,
        'jsonld_organization': jsonld_organization0,
        'jsonld_home': jsonld_home0,
    }
    jsonld = get_jsonld(request, page_conf)
    print(json.dumps(jsonld, indent=4, sort_keys=True))
    print(get_jsonld_script_from_jsonld(jsonld))



