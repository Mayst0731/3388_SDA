import bs4


async def download_site(url, session):
    content = await session.get(url)
    source = await content.text(errors="ignore")
    page = parse(source)
    return page


def parse(source):
    page = bs4.BeautifulSoup(source,'lxml')
    return page