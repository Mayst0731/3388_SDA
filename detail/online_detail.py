import urllib


from detail import *
from detail.category_page_detail import get_cate_language_info, get_cate_start_date, get_cate_end_date, \
    get_cate_duration, get_cate_category



def single_cate_for_online(online_page,cate_url):
    details = []
    cate_sessions = online_page.find('div',attrs={"id":"yxp_block_017e4c80ab0c7adb78d5a076daf619c0"}).find_all('div',
                                                                                                               attrs={"class":"yxpRow"},recursive=False)[8:16]
    for cate_session in cate_sessions:
        cate_title = cate_session.find('h3',attrs={"class":"title-h3 title-main"}).text.strip()
        course_sessions = cate_session.find_all('a',attrs={"class":"courseBox shown"})
        for course_session in course_sessions:
            detail = get_online_detail(course_session,cate_url)
            details.append(detail)
    return details


def get_online_detail(course_session,cate_url):
    course_name = course_session.find('h6').text.title()
    course_link = course_session.get('href')
    course_url = urllib.parse.urljoin("https://www.sdabocconi.it/en/online-programs", course_link)
    language = get_cate_language_info(course_session)
    start_date = get_cate_start_date(course_session)
    end_date = get_cate_end_date(course_session)
    duration_info = get_cate_duration(course_session)
    cate = get_cate_category(course_session)
    course = {
              'category':cate,
              "category_url":cate_url,
              'name': course_name,
              'url': course_url,
              'language': language,
              'effective_date_start': start_date,
              'effective_date_end': end_date,
              "duration": duration_info}
    return course


