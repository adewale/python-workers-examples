from workers import WorkerEntrypoint, Response

UPLOAD_HTML = """<!DOCTYPE html>
<html>
<head><title>R2 File Upload</title></head>
<body>
  <h1>Upload a file to R2</h1>
  <form action="/upload" method="POST" enctype="multipart/form-data">
    <input type="file" name="file" required>
    <button type="submit">Upload</button>
  </form>
  <h2>Files</h2>
  <p>Visit <code>/file/&lt;key&gt;</code> to download a file.</p>
  <p>Visit <code>/list</code> to list all files.</p>
</body>
</html>"""


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        url = request.url
        path = url.split("//", 1)[1].split("/", 1)[1] if "//" in url else "/"

        if request.method == "GET" and (path == "" or path == "/"):
            return Response(UPLOAD_HTML, headers={"Content-Type": "text/html"})

        if request.method == "GET" and path == "list":
            listed = await self.env.MY_BUCKET.list()
            keys = [obj.key for obj in listed.objects]
            return Response.json({"files": keys})

        if request.method == "GET" and path.startswith("file/"):
            key = path[len("file/"):]
            obj = await self.env.MY_BUCKET.get(key)
            if obj is None:
                return Response("Not found", status=404)
            body = await obj.text()
            return Response(body, headers={
                "Content-Type": obj.httpMetadata.contentType or "application/octet-stream",
            })

        if request.method == "PUT" and path.startswith("file/"):
            key = path[len("file/"):]
            body = await request.text()
            await self.env.MY_BUCKET.put(key, body)
            return Response.json({"key": key, "status": "uploaded"})

        return Response("Not found", status=404)
