def public():
    import requests
    pub_ip = requests.get('http://jsonip.com').json()['ip']
    return pub_ip

    