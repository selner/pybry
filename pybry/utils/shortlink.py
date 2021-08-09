


def get_shortio_link(shortdomain, url, authkey):
	import requests

	res = requests.post('https://api.short.io/links', {
		'domain':      shortdomain,
		'originalURL': url,
	}, headers={
		'authorization': authkey
	}, json=True)

	res.raise_for_status()
	data = res.json()

	print(data)

	return data['shortURL']

