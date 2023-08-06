
# aiounu

An asyncio module for [unu](https://u.nu/) in Python3 using aiohttp. Forked from
[vcinex/unu](https://github.com/vcinex/unu).

## Install

```sh
pip install aiounu
```

## Use

```python
import aiounu as unu

test_url = "https://example.com/?test=52e838e8-0943-4ccb-bfd8-ae6bb3173bd2"
unu_resp = await unu.shorten(url=test_url, output_format="dot", keyword="")
print(unu_resp.shorturl)
```

## Example Result

If `output_format` is set to **dot** (The default), the resulting JSON object properties will be accessible (Thanks to
[mo-dots](https://pypi.org/project/mo-dots/)) by both dot.notation and dict['notation'].

```json
{
  "url": {
    "keyword": "kfuns",
    "url": "https://example.com/?test=52e838e8-0943-4ccb-bfd8-ae6bb3173bd2",
    "title": "Example Domain",
    "date": "2020-12-22 08:44:33",
    "ip": "22.42.219.59"
  },
  "status": "error",
  "message": "https://example.com/?test=52e838e8-0943-4ccb-bfd8-ae6bb[...] added to database<br/>(Could not check Google Safe Browsing: Bad Request)",
  "title": "Example Domain",
  "shorturl": "https://u.nu/kfuns",
  "statusCode": 200
}
```

Only the `url` variable is necessary. For a runnable example, see
[tests/test_shorten.py](https://github.com/TensorTom/aiounu/blob/master/tests/test_shorten.py) or clone the repo
and run [pytest](https://docs.pytest.org/en/stable/).

----------------------------------------

MIT License