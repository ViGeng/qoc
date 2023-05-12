import asyncio


class MyClass:
    async def func1(self):
        while True:
            # do something here
            await asyncio.sleep(1)
            print("world")

    async def func2(self):
        while True:
            # do something here
            await asyncio.sleep(2)
            print("hello")

    def get_task(self) -> list:
        return [asyncio.create_task(self.func1())
            , asyncio.create_task(self.func2())]

    def tasks(self):
        asyncio.gather(
            asyncio.create_task(self.func1()),
            asyncio.create_task(self.func2()),
        )


async def main():
    my_obj = MyClass()
    await asyncio.gather(*my_obj.get_task())


if __name__ == '__main__':
    my_obj = MyClass()
    asyncio.run(main())
