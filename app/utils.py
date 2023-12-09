import os

import aiofiles
import aiocsv


async def read_csv_file(file: os.path) -> list[dict[str, str]]:
    async with aiofiles.open(file, mode='r', encoding='utf-8') as afp:
        headers: str = await afp.readline()
        headers: list[str] = headers.replace('\n', '').split(';')

        csv_reader: aiocsv.readers.AsyncDictReader = aiocsv.AsyncDictReader(
            afp,
            fieldnames=headers,
            delimiter=';',
            restval=None
        )
        read_file: list[dict[str, str]] = [row async for row in csv_reader]

        return read_file

