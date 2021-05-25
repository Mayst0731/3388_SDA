import urllib
from download_parse import download_site


async def extract_categories(url,online_url,session):
    cates = []
    cates += await extract_online_categories(online_url,session)
    cates += await extract_executive_categories(url,session)
    return cates


async def extract_executive_categories(url,session):
    cate_list = []
    page = await download_site(url, session)
    div = page.find('div',attrs={"class":"modal-body"})
    uls = div.find_all('ul')
    for ul in uls:
        lis = ul.find_all('li')
        outer_cate_name = lis[0].text.strip().title()
        inner_cates = lis[1:]
        for cate in inner_cates:
            cate_link = cate.find('a').get('href')
            inner_cate_name = cate.find('a').text.strip()
            cate_name = outer_cate_name + ' - ' + inner_cate_name
            cate_url = urllib.parse.urljoin(url, cate_link)
            cate = {'parent_url':url,
                    'name':cate_name,
                    'url':cate_url}
            cate_list.append(cate)
    return cate_list


async def extract_online_categories(online_url,session):
    cate_list = []
    page = await download_site(online_url, session)
    outer_name = 'Online'
    links = page.find_all('a',attrs={"class":"link swiperlink"})
    for link in links:
        inner_cate_name = link.text.strip().title()
        cate_link = link.get('href')
        cate_name = outer_name + ' - ' + inner_cate_name
        cate_url = urllib.parse.urljoin(online_url, cate_link)
        cate = {'parent_url':online_url,
                'name':cate_name,
                'url':cate_url}
        cate_list.append(cate)
    return cate_list






