from workers import WorkerEntrypoint, Response


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        url = request.url
        path = url.split("//", 1)[1].split("/", 1)[1] if "//" in url else "/"

        if request.method == "GET" and (path == "" or path == "/"):
            return Response(
                "PUT /file/<key> — upload a file (body = file content)\n"
                "GET /file/<key> — download a file by key\n"
                "GET /list — list all files in the bucket\n",
            )

        if request.method == "GET" and path == "list":
            listed = await self.env.MY_BUCKET.list()
            keys = [obj.key for obj in listed.objects]
            return Response.json({"files": keys})

        if request.method == "GET" and path.startswith("file/"):
            key = path[len("file/"):]
            obj = await self.env.MY_BUCKET.get(key)
            if obj is None:
                return Response("Not found", status=404)
            headers = obj.writeHttpMetadata({})
            return Response(await obj.arrayBuffer(), headers=headers)

        if request.method == "PUT" and path.startswith("file/"):
            key = path[len("file/"):]
            content_type = request.headers.get("Content-Type") or "application/octet-stream"
            body = await request.arrayBuffer()
            await self.env.MY_BUCKET.put(key, body, {
                "httpMetadata": {"contentType": content_type},
            })
            return Response.json({"key": key, "status": "uploaded"})

        return Response("Not found", status=404)
