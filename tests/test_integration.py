from poem_for_the_day import get_poem_today, create_app


async def test_get_poem(aiohttp_client):
    app = await create_app()
    client = await aiohttp_client(app)
    poem = await get_poem_today()
    response = await client.get('/')

    assert response.status == 200

    assert poem == await response.text()
