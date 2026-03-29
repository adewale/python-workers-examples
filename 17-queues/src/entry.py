import json
from workers import WorkerEntrypoint, Response


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        url = request.url
        path = url.split("//", 1)[1].split("/", 1)[1] if "//" in url else "/"

        if request.method == "POST" and path == "enqueue":
            body = await request.json()
            await self.env.MY_QUEUE.send(body)
            return Response.json({"status": "enqueued", "message": body})

        return Response(
            "POST a JSON body to /enqueue to send a message to the queue.\n"
            "Messages are processed in batches — check your Worker logs.",
        )

    async def queue(self, batch):
        messages = []
        for msg in batch.messages:
            messages.append(msg.body)
            msg.ack()
        print(f"Processed batch of {len(messages)} messages: {json.dumps(messages)}")
