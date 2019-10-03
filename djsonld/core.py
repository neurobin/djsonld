
from urllib.parse import urlparse
import re
import json


class Base(object):
    def __init__(self, type, **kwargs):
        self.jsonld = {
            "@type": type,
        }
        self.jsonld.update(kwargs)


class Author(object):
    def __init__(self, name, **kwargs):
        self.jsonld = {
            "@type": "Person",
            "name": name,
        }
        self.jsonld.update(kwargs)


class Organization(object):
    def __init__(self, name, description, foundingDate, founder, **kwargs):
        self.jsonld = {
            "@type": "Organization",
            "name": name,
            "description": description,
            "foundingDate": foundingDate,
            "founder": founder,
        }
        self.jsonld.update(kwargs)



def urljoin(*args):
    """
    Joins given arguments into an url.
    """

    return "/".join(map(lambda x: str(x).strip('/'), args))

def get_jsonld(request, page_conf):
    """Calculate jsonld from request and page conf (context)
    
    Args:
        request (HttpRequest): request object
        page_conf (dict): Context
    
    Returns:
        dict: jsonld object
    """
    url = request.build_absolute_uri()
    urlo = urlparse(url)
    host = urlo.netloc
    protocol = urlo.scheme
    path = urlo.path
    domain_name = page_conf.get('site_name', host)
    domain_url = protocol + '://' + host

    #Constructing breadcrumb
    ps = path.split('/')
    urp = '';
    bread_crumb_items = []
    bread_crumb_items.append({
        "@type": "ListItem",
        "position": 1,
        "item": {
            "@type": "WebSite",
            "@id": domain_url,
            "url": domain_url,
            "name": domain_name,
        }
    })

    i = 0
    bc_name = ''
    for psc in ps:
        psc = psc.strip()
        if not psc:
            continue
        i = i + 1
        bc_name = re.sub(r'[-]', ' ', psc).capitalize()
        urp = urljoin(urp, psc)
        u = urljoin(domain_url, urp)
        bread_crumb_items.append({
            "@type": "ListItem",
            "position": i+1,
            "item": {
                "@type": "WebPage",
                '@id': u,
                "url": u,
                "name": bc_name,
            }
        })
    
    if bread_crumb_items:
        breadcrumb = {
            "@type": "BreadcrumbList",
            "itemListElement": bread_crumb_items,
        }
    else:
        breadcrumb = {}

    if 'thumb0' in page_conf:
        thumb = urljoin(domain_url, page_conf['thumb0'])
        # {
        #     "@type": "ImageObject",
        #     "url": urljoin(domain_url, page_conf['thumb0']),
        #     "width": "600",
        #     "height": "600",
        # }
    else:
        thumb = {}

    webpage = {
        "@type":"WebPage",
        "@id": url,
    }
    if breadcrumb:
        webpage['breadcrumb'] = breadcrumb

    webpage_full = {
        "@type":"WebPage",
        "headline": page_conf.get('title', bc_name),
        "description": page_conf.get('description', bc_name),
    }
    
    if 'startdate' in page_conf:
        startdate = page_conf['startdate']
    else:
        startdate = ''
    
    if 'timestamp' in page_conf:
        moddate = page_conf['timestamp']
    else:
        moddate = ''
    
    if 'jsonld_author' in page_conf:
        jsonld_author = page_conf['jsonld_author']
    else:
        jsonld_author = {}

    if 'jsonld_organization' in page_conf:
        jsonld_organization = page_conf['jsonld_organization']
    else:
        jsonld_organization = {}

    if 'jsonld_home' in page_conf:
        jsonld_home = page_conf['jsonld_home']
    else:
        jsonld_home = {}

    if thumb:
        webpage_full['image'] = thumb
    
    if startdate:
        webpage_full['datePublished'] = startdate

    if moddate:
        webpage_full['dateModified'] = moddate
    
    if jsonld_author:
        webpage_full['author'] = jsonld_author
    if jsonld_organization:
        webpage_full['publisher'] = jsonld_organization

    webpage_full["license"] = "https://neurobin.org/about/tos/"
    
    if breadcrumb:
        webpage_full['breadcrumb'] = breadcrumb
    
    page_json_ld = {"@context": "http://schema.org",}
    page_json_ld.update(webpage_full)

        
    code = {
        "@type": "Code",
    }

    itms = ('name', 'description', 'dateCreated', 'license', )
    for k in itms:
        if k in page_conf:
            code[k] = page_conf[k]
    if startdate:
        code['dateCreated'] = startdate

    if jsonld_author:
        code['author'] = jsonld_author
    if jsonld_organization:
        code['provider'] = jsonld_organization
    
    if 'name' not in code:
        code['name'] = bc_name
    if 'description' not in code:
        code['description'] = bc_name
    
    soft = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        'url': url,
    }

    itms = ('name', 'operatingSystem', 'applicationCategory', 'keywords', 'description' )
    for k in itms:
        if k in page_conf:
            soft[k] = page_conf[k]
    if 'os' in page_conf:
        soft['operatingSystem'] = page_conf['os']
    if 'OS' in page_conf:
        soft['operatingSystem'] = page_conf['OS']
    
    if jsonld_author:
        soft['author'] = jsonld_author
        soft['copyrightHolder'] = jsonld_author
    
    if startdate:
        soft['datePublished'] = startdate
    if moddate:
        soft['dateModified'] = moddate
    if jsonld_organization:
        soft['provider'] = jsonld_organization
    if webpage:
        soft['mainEntityOfPage'] = webpage
    if thumb:
        soft['thumbnailUrl'] = thumb

    article = {
        "@type": "Article",
        "headline": page_conf.get('title', bc_name),
        "description": page_conf.get('description', bc_name),
    }
    if thumb:
        article['image'] = thumb
    
    if webpage:
        article['mainEntityOfPage'] = webpage

    if startdate:
        article['datePublished'] = startdate
    if moddate:
        article['dateModified'] = moddate
    if jsonld_author:
        article['author'] = jsonld_author
    if jsonld_organization:
        article['publisher'] = jsonld_organization

    if 'type' in page_conf:
        ptype = page_conf['type']
    else:
        ptype = ''

    if ptype == 'project':
        article['about'] = code

    article_json_ld = {
        "@context": "http://schema.org",
    }
    article_json_ld.update(article)


    json_ld_f = {};
    if ptype == 'home':
        json_ld_f = jsonld_home
    elif ptype == 'project' or ptype == 'article':
        json_ld_f = article_json_ld
    elif ptype == 'product':
        json_ld_f = soft
    else:
        json_ld_f = page_json_ld

    return json_ld_f


def get_jsonld_script_from_jsonld(jsonld):
    """Get jsonld script from jsonld object
    
    Args:
        jsonld (dict): json
    
    Returns:
        str: jsonld script with <script> tag
    """
    return '<script type="application/ld+json">' + json.dumps(jsonld) + '</script>'

def get_jsonld_script(request, context):
    """Get jsonld script
    
    Args:
        request (HttpRequest): request object
        context (dict): page context
    
    Returns:
        str: jsonld script with <script> tag
    """
    return get_jsonld_script_from_jsonld(get_jsonld(request, context))