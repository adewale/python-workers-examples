# Vectorize Semantic Search Example

Index and search documents using [Cloudflare Vectorize](https://developers.cloudflare.com/vectorize/) and [Workers AI](https://developers.cloudflare.com/workers-ai/) embeddings from a Python Worker.

## Setup

Create a Vectorize index before deploying:

```sh
npx wrangler vectorize create python-semantic-search --dimensions=768 --metric=cosine
```

## How to Run

First ensure that `uv` is installed:
https://docs.astral.sh/uv/getting-started/installation/#standalone-installer

Now, if you run `uv run pywrangler dev` within this directory, it should use the config
in `wrangler.jsonc` to run the example.

You can also run `uv run pywrangler deploy` to deploy the example.

## Routes

- `GET /` — Instructions
- `POST /index` — Index a document: `{"id": "1", "text": "Your document text"}`
- `GET /search?q=your+query` — Semantic search for similar documents
