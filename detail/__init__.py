
from detail.course_page_detail import get_course_price_info, get_course_language_info, get_course_loc_info, \
    get_course_type, get_overview, get_takeaways, get_who_should_attend, get_video_info, get_faculties
from detail.executive_detail import get_executive_cate_detail
from detail.format_strings import arrange_date_format
from detail.masters_detail import get_contact_email
from detail.online_detail import get_online_detail, single_cate_for_online
from download_parse import download_site


async def extract_details(origin_category_list,session):
    course_list = []
    for cate_info in origin_category_list:
        cate_url = cate_info['url']
        if not cate_info['name'].startswith("Online") and not cate_info['name'].startswith("Management"):
            executive_cate_detail = []
            try:
                cate_page = await download_site(cate_url,session)
                executive_cate_detail = get_executive_cate_detail(cate_page,cate_url)
            except:
                pass
            course_list += executive_cate_detail
        else:
            continue
    management_cate_url = 'https://www.sdabocconi.it/en/executive-education/executive-open-programs/managment#category-generalmanagement%7Clanguage-english'
    cate_page = await download_site(management_cate_url, session)
    management_executive_cate_detail = get_executive_cate_detail(cate_page,management_cate_url)
    course_list += management_executive_cate_detail

    online_url = 'https://www.sdabocconi.it/en/online-programs'
    online_page = await download_site(online_url, session)
    online_detail = single_cate_for_online(online_page,online_url)
    course_list += online_detail
    course_list = arrange_categories(course_list)
    return course_list


def arrange_categories(course_list):
    course_dict = dict()
    for course in course_list:
        if course['url'] not in course_dict:
            new_course = {"name": course['name'],
                          "category": [course["category"]],
                          "category_url":[course["category_url"]],
                          "duration": course["duration"],
                          "effective_date_start": arrange_date_format(course["effective_date_start"]),
                          "effective_date_end": arrange_date_format(course["effective_date_end"]),
                          "language": course["language"],
                          "url": course["url"],
                          "testimonials":[]}
            course_dict[course["url"]] = new_course
        else:
            course_dict[course["url"]]["category"].append(course["category"])
            course_dict[course["url"]]["category_url"].append(course["category_url"])
    collected_courses = []
    for course in course_dict.values():
        collected_courses.append(course)
    for course in collected_courses:
        if len(course["category"]) == 2 and course["category"][0] == course["category"][1]:
            course["category"] = course["category"][:1]
            course["category_url"] = course["category_url"][:1]
    return collected_courses


async def integrate_details(courses,session):
    details = []
    course_page = None
    for course in courses:
        print(f'{course["name"]}: {course["url"]}')
        course_url = course['url']
        try:
            course_page = await download_site(course_url, session)
        except:
            pass
        one_detail = await integrate_one_course_detail(course_page,course,session)
        if one_detail["name"]!="" and one_detail["course_type"]!="":
            details.append(one_detail)
    return details


async def integrate_one_course_detail(course_page,course,session):
    new_info = dict()
    tuition = ''
    currency = ''
    location = ''
    course_type = ''
    overview = ''
    takeaways = ''
    who_attend_desc = ''
    video_title = ''
    video_url = ''
    faculties = []
    exec_ed_inquiry_cc_emails = get_contact_email(course_page)
    try:
        price_info = get_course_price_info(course_page)
        tuition = price_info["tuition"]
        currency = price_info["currency"]
    except:
        pass
    try:
        location = get_course_loc_info(course_page)
    except:
        pass
    try:
        course_type = get_course_type(course_page)
    except:
        pass
    try:
        overview = get_overview(course_page)
    except:
        pass
    try:
        takeaways = get_takeaways(course_page)
    except:
        pass
    try:
        who_attend_desc = get_who_should_attend(course_page)
    except:
        pass
    try:
        video_info = get_video_info(course_page)
        video_url = video_info["video_url"]
        video_title = video_info["video_title"]
    except:
        pass
    try:
        faculties = await get_faculties(course_page, session)
    except:
        pass
    new_info["exec_ed_inquiry_cc_emails"] = get_contact_email(course_page)
    new_info["tuition"] = tuition
    new_info["currency"] = currency
    new_info["location"] = location
    new_info["course_type"] = course_type
    new_info["overview"] = overview
    new_info["course_takeaways"] = takeaways
    new_info["who_attend_desc"] = who_attend_desc
    new_info["video_title"] = video_title
    new_info["video_url"] = video_url
    new_info["course_faculty"] = faculties
    new_info["exec_ed_inquiry_cc_emails"] = exec_ed_inquiry_cc_emails
    comprehensive_detail = {**course,**new_info}
    return comprehensive_detail









