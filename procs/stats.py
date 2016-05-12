import asyncio

def proc_main(pk, row, arg):
    damean = row['ts'].mean()
    dastd = row['ts'].std()
    return [damean, dastd]

async def main(pk, row, arg):
    # Calculate Stats on the passed in TimeSeries,
    # namely mean and std
    return proc_main(pk, row, arg)
    
