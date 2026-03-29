# R2 File Upload Example

Upload, download, and list files using [Cloudflare R2](https://developers.cloudflare.com/r2/) object storage from a Python Worker.

## How to Run

First ensure that `uv` is installed:
https://docs.astral.sh/uv/getting-started/installation/#standalone-installer

Now, if you run `uv run pywrangler dev` within this directory, it should use the config
in `wrangler.jsonc` to run the example.

You can also run `uv run pywrangler deploy` to deploy the example.

## Routes

- `GET /` — Instructions
- `PUT /file/<key>` — Upload a file with the given key (set `Content-Type` header)
- `GET /file/<key>` — Download a file by key
- `GET /list` — List all files in the bucket

## Try it

```sh
# Upload a text file
curl -X PUT -H "Content-Type: text/plain" -d "Hello R2" http://localhost:8787/file/hello.txt

# Download it
curl http://localhost:8787/file/hello.txt

# List files
curl http://localhost:8787/list
```
