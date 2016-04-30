import aiohttp
import asyncio
import json
url = 'http://localhost:9999/'
payload = {'pk': 'four',
		   'op':'insert_ts',
			'ts':[[0.0, 1.0, 4.0], [0.0, 0.0, 4.0]]}
#headers = {'content-type': 'application/json'}


async def hello():
	with aiohttp.ClientSession() as session:
		#session.post('http://localhost:9999/', data=b'data')
	    async with session.get('http://localhost:9999/') as resp:
	        print(resp.status)
	        print(await resp.text())

async def run():
	with aiohttp.ClientSession() as session:
		#async with session.post(url, data=payload) as resp:
		async with session.post(url, data=json.dumps(payload)) as resp:
		    print(await resp.text())




loop = asyncio.get_event_loop()  
loop.run_until_complete(run())  
loop.close()  