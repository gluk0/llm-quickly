import asyncio
import aiohttp
import time

async def make_request(session, i):
    start = time.time()
    async with session.post(
        'http://localhost:8000/generate',
        json={
            "prompt": f"What is {i} + {i}?",
            "max_length": 100,
            "temperature": 0.7,
            "top_p": 0.9
        }
    ) as response:
        result = await response.json()
        end = time.time()
        print(f"Request {i} took {end - start:.2f} seconds")
        return result

async def main():
    async with aiohttp.ClientSession() as session:
        # Make 5 concurrent requests
        tasks = [make_request(session, i) for i in range(5)]
        results = await asyncio.gather(*tasks)
        
        for i, result in enumerate(results):
            print(f"Response {i}:", result)

if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(f"\nTotal time for all requests: {end - start:.2f} seconds") 