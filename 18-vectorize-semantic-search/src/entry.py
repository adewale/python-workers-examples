import json
from workers import WorkerEntrypoint, Response

EMBEDDING_MODEL = "@cf/baai/bge-base-en-v1.5"


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        url = request.url
        path = url.split("//", 1)[1].split("/", 1)[1] if "//" in url else "/"

        if request.method == "POST" and path == "index":
            return await self._index(request)

        if request.method == "GET" and path.startswith("search"):
            return await self._search(request)

        return Response(
            "POST /index with {\"id\": \"1\", \"text\": \"...\"} to index a document.\n"
            "GET /search?q=your+query to find similar documents.",
        )

    async def _index(self, request):
        body = await request.json()
        doc_id = body["id"]
        text = body["text"]

        embedding_resp = await self.env.AI.run(EMBEDDING_MODEL, {"text": [text]})
        vector = list(embedding_resp.data[0])

        await self.env.VECTORIZE_INDEX.insert([{
            "id": doc_id,
            "values": vector,
            "metadata": {"text": text},
        }])

        return Response.json({"status": "indexed", "id": doc_id})

    async def _search(self, request):
        url = request.url
        query = ""
        if "?" in url:
            params = url.split("?", 1)[1]
            for param in params.split("&"):
                if param.startswith("q="):
                    query = param[2:].replace("+", " ")

        if not query:
            return Response("Missing ?q= query parameter", status=400)

        embedding_resp = await self.env.AI.run(EMBEDDING_MODEL, {"text": [query]})
        query_vector = list(embedding_resp.data[0])

        results = await self.env.VECTORIZE_INDEX.query(query_vector, {"topK": 5, "returnMetadata": "all"})

        matches = []
        for match in results.matches:
            matches.append({
                "id": match.id,
                "score": match.score,
                "text": match.metadata.text if match.metadata else None,
            })

        return Response.json({"query": query, "matches": matches})
