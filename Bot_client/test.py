import asyncio
async def task2(i):
    print(i)
    await asyncio.sleep(3)
    print('fun2 завершена')


async def task(i):
     await task2(i)
async def main():

    for i in range(5):
        task1 = asyncio.create_task(task(i))
    await task1
asyncio.run(main())
