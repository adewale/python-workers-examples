from workers import WorkerEntrypoint, Response


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        url = request.url
        path = url.split("//", 1)[1].split("/", 1)[1] if "//" in url else "/"

        if path == "" or path == "/":
            return Response(
                "GET /screenshot — take a PNG screenshot of example.com\n"
                "GET /content — get the HTML content of example.com\n"
                "GET /pdf — generate a PDF of example.com\n",
            )

        target = "https://example.com"

        if path == "screenshot":
            img = await self.env.BROWSER.screenshot(target, {"type": "png"})
            return Response(img, headers={"Content-Type": "image/png"})

        if path == "pdf":
            pdf = await self.env.BROWSER.pdf(target)
            return Response(pdf, headers={"Content-Type": "application/pdf"})

        if path == "content":
            page = await self.env.BROWSER.content(target)
            return Response(page, headers={"Content-Type": "text/html"})

        return Response("Not found", status=404)
