import tldextract

def get_domain_name(link):
    url_extract = tldextract.extract(link)
    site_name = url_extract.domain + '.' + url_extract.suffix
    return site_name
