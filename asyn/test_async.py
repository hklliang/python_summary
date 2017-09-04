import types
import asyncio
# async def coro1():
#     print("C1: Start")
#     print("C1: Stop")

async def coro1():
    print("C1: Start")
    await switch()
    print("C1: Stop")


async def coro2():
    print("C2: Start")
    print("C2: a")
    print("C2: b")
    print("C2: c")
    print("C2: Stop")


def run(coros):
    coros = list(coros)

    while coros:
        # Duplicate list for iteration so we can remove from original list.
        for coro in list(coros):
            try:
                coro.send(None)
            except StopIteration:
                coros.remove(coro)

# async def main():
#     await c1


@types.coroutine
def switch():
    yield
c1 = coro1()

c2 = coro2()
run([c1, c2])
# print(c1, c2)



# try:
#     c1.send(None)
# except StopIteration:
#     pass
# try:
#     c2.send(None)
# except StopIteration:
#     pass
# try:
#     c1.send(None)
# except StopIteration:
#     pass