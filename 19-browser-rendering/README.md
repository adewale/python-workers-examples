# Browser Rendering Example

Take screenshots, extract HTML content, and generate PDFs of web pages using
[Cloudflare Browser Rendering](https://developers.cloudflare.com/browser-rendering/)
from a Python Worker.

## How to Run

First ensure that `uv` is installed:
https://docs.astral.sh/uv/getting-started/installation/#standalone-installer

Now, if you run `uv run pywrangler dev` within this directory, it should use the config
in `wrangler.jsonc` to run the example.

You can also run `uv run pywrangler deploy` to deploy the example.

## Routes

- `GET /` — Instructions
- `GET /screenshot` — PNG screenshot of example.com
- `GET /pdf` — PDF of example.com
- `GET /content` — HTML content of example.com
