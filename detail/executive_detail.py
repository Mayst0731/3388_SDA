
from urllib import parse

from detail.category_page_detail import get_cate_category, get_cate_duration, get_cate_start_date, \
    get_cate_end_date, get_cate_language_info


def get_executive_cate_detail(page,cate_url):
    course_list = []
    link_sessions = page.find_all('a', attrs={"class": "courseBox shown"})
    for link_session in link_sessions:
        cate_name = get_cate_category(link_session)
        course_name = link_session.h6.text.title()
        duration_info = get_cate_duration(link_session)
        start_date = get_cate_start_date(link_session)
        end_date = get_cate_end_date(link_session)
        language = get_cate_language_info(link_session)
        course_link = link_session.get('href')
        course_url = parse.urljoin("https://www.sdabocconi.it", course_link)
        info = {"name": course_name,
                "category": cate_name,
                "category_url":cate_url,
                "duration": duration_info,
                "effective_date_start": start_date,
                "effective_date_end": end_date,
                "language": language,
                "url": course_url}
        course_list.append(info)
    course_list = filter_exe_courses(course_list)

    return course_list


def filter_exe_courses(course_list):
    new_course_list = []
    for course in course_list:
        if course['name'] == course['category']:
            continue
        else:
            new_course_list.append(course)
    return new_course_list




