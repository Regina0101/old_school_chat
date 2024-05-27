class ApiPrivatBank:
    BASE_API = "https://api.privatbank.ua/p24api/exchange_rates?json&date="

    async def fetch(self, date, session):
        # async with aiohttp.ClientSession() as session:
        url = self.BASE_API + date
        async with session.get(url) as response:
            try:
                print(url)
                print("Status:", response.status)
                print("Content-type:", response.headers['content-type'])
                if response.status == 200:
                    result = await response.json()
                    return result
                else:
                    print(f"Error status: {response.status} for {url}")
                    return None
            except Exception as e:
                return f"Error: {e}"
