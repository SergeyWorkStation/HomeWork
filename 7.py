import aiohttp
import asyncio
import re
import aiofiles

semaphore = asyncio.Semaphore(2)
async def load_page(url: str, filename: str, retries:int = 3, timeout:int = 5) -> None:
    """
    Асинхронная функция для загрузки веб-страницы в файл.

    :param filename: Имя файла для загрузки страницы
    :param url: URL для загрузки.
    :param retries: Количество попыток в случае неудачи.
    :param timeout: Таймаут для запросов в секундах.
    :return: None
    """
    for attempt in range(retries):
        try:
            async with semaphore:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, timeout=timeout) as response:
                        response.raise_for_status()
                        html_content = await response.text()
                        h_pattern = r'<h\d>([\s\S]*?)<\/h\d>'
                        p_pattern = r'<p>([\s\S]*?)<\/p>'
                        link_pattern = r'<a href="(.*?)">(.*?)<\/a>'
                        h_matches = [''.join(line) for line in re.findall(h_pattern, html_content)]
                        p_matches = [''.join(line) for line in re.findall(p_pattern, html_content)]
                        link_matches = [''.join(line) for line in re.findall(link_pattern, html_content)]
                        lines = h_matches+p_matches+link_matches
                        async with aiofiles.open(filename, 'w') as f:
                            for line in lines:
                                await f.write(line+'\n')
                        await asyncio.sleep(10)
                        print(f"Страница:{url} загружена в файл {filename}.")
                        return
        except aiohttp.ClientError as e:
            print(f"Ошибка при загрузке {url}: {e}")
        except asyncio.TimeoutError:
            print(f"Таймаут при загрузке {url}. Попытка {attempt + 1} из {retries}.")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")
        await asyncio.sleep(1)

    print(f"Не удалось загрузить {url} после {retries} попыток.")
    return

async def main():
    await asyncio.gather(
        load_page("https://example.org/", '1.txt'),
        load_page("https://example.com/", '2.txt'),
        load_page("https://example.net/", '3.txt')
    )

asyncio.run(main())
