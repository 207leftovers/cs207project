import asyncio
async def main(pk, row, arg):
    # Calculate Stats on the passed in TimeSeries,
    # namely mean and std
    damean = row['ts'].mean()
    dastd = row['ts'].std()
    return [damean, dastd]
