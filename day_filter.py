from data_proc import DataProcess

class DayCount:
    async def day_count(self, data):
        data_process = DataProcess()
        filtered_data = await data_process.data_filter(data)
        return filtered_data


