class DataProcess:
    async def data_filter(self, data):
        filtered_data = {}
        for date, exchange_data in data.items():
            exchange_rates = exchange_data.get('exchangeRate', [])
            keys = ['USD', 'EUR']
            filtered_rates = [x for x in exchange_rates if x.get('currency') in keys]
            data_dict = {x['currency']: {'sale': x.get('saleRate'), 'purchase': x.get('purchaseRateNB')} for x in filtered_rates}
            filtered_data[date] = data_dict
        return filtered_data
