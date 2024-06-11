from django.shortcuts import render

import asyncio
import random

from django.http import StreamingHttpResponse
from django.shortcuts import render


async def sse_stream(request):
    """
    Sends server-sent events to the client.
    """
    async def event_stream():
        emojis = ["🚀", "🐎", "🌅", "🦾", "🍇"]
        i = 0
        while True:
            yield f'data: {random.choice(emojis)} {i}\n\n'
            i += 1
            await asyncio.sleep(1)

    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')
