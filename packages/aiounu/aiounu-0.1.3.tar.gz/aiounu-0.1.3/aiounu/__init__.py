import aiohttp
from mo_dots import to_data


class HTTPError(Exception):
	pass


async def shorten(url="https://example.com", output_format="dot", keyword=""):
	"""
	Shorten a given URL.
	:param url: The URL to shorten.
	:param output_format: The return format (dot, json, xml, simple)
	:param keyword: Keyword for the resulting URL (Optional)
	:return: Returns a dict-like dot.accessible.object if return-type is json,
			otherwise returns the result string (URL) from u.nu.
	"""

	if output_format not in ("dot", "simple", "xml", "json"):
		raise ValueError(f"_format must be one of: 'simple', 'xml', 'json'. Got: {output_format}")
	data = {
		"action": 'shorturl',
		"format": output_format if output_format != 'dot' else 'json',
		"url": url,
		"keyword": keyword
	}
	async with aiohttp.ClientSession() as session:
		async with session.post("https://u.nu/api.php", params=data) as resp:
			if resp.status != 200:
				await session.close()
				raise HTTPError(f"HTTP returned code {resp.status} rather than 200")
			await session.close()
			if output_format not in ('dot', 'json'):
				await session.close()
				return await resp.text()
			jo = await resp.json()
			await session.close()
			return to_data(jo) if output_format == 'dot' else jo
