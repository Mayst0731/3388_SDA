
from urllib import parse
import re

from detail.category_page_detail import get_cate_duration, get_cate_start_date, get_cate_end_date, \
    get_cate_language_info
from detail.course_page_detail import get_one_fac_info
from detail.format_strings import get_tuition, get_currency, get_duration_type, get_duration_num, arrange_date_format, \
    calculate_end_date
from download_parse import download_site
from final_format import deal_with_location, add_schedule


async def get_comprehensive_master_mba_detail(session):
    details = []
    mba_emba_gemba_cate_url = 'https://www.sdabocconi.it/en/mba-executive-mba'
    masters_cate_url = 'https://www.sdabocconi.it/en/specialized-master-full-time-executive'
    parent_url = 'https://www.sdabocconi.it/'
    mba_emba_gemba_cate_page = await download_site(mba_emba_gemba_cate_url,session)
    masters_cate_page = await download_site(masters_cate_url,session)
    masters_detail = await get_masters_cate_course_detail(masters_cate_page,masters_cate_url,parent_url,session)
    details += masters_detail
    mba_emba_gemba_detail = await get_mbas_cate_course_detail(mba_emba_gemba_cate_page,mba_emba_gemba_cate_url,parent_url,session)
    details += mba_emba_gemba_detail
    for detail in details:
        detail["schedule"] = [add_schedule(detail)]
    return details


async def get_mbas_cate_course_detail(cate_page,cate_url,parent_url,session):
    course_list = []
    course_sessions = cate_page.find_all('div',attrs={"class":"textWrapper"})
    for course_session in course_sessions:
        course_name = course_session.find('h2').text
        cate_name = 'All MBAs'
        duration_info = course_session.find('div',attrs={"class":"partTitle"},text="Duration").find_next('p').text
        duration_type = get_duration_type(duration_info)
        duration_type = 'duration_'+duration_type
        duration_num = get_duration_num(duration_info)
        language = course_session.find('div',attrs={"class":"partTitle"},text="Language").find_next('p').text
        course_link = course_session.find('a').get('href')
        course_url = parse.urljoin("https://www.sdabocconi.it/",course_link)
        if course_url.endswith("program"):
            course_url = course_url[:-8]
        cate_page_info = {"name": course_name,
                          "category": [cate_name],
                          "category_url": [cate_url],
                          "parent_url": parent_url,
                          duration_type: duration_num,
                          "language": language,
                          "url": course_url,
                          "version":1}
        if "EMBA" in course_name:
            cate_page_info['credential'] = "EMBA"
        else:
            cate_page_info['credential'] = "MBA"
        print(cate_page_info["url"])
        course_page = await download_site(course_url,session)
        mbas_course_info = await get_mbas_course_detail(course_url,course_page,session)
        info = {**cate_page_info, **mbas_course_info}
        info["effective_date_end"] = calculate_end_date(info["effective_date_start"],duration_type,duration_num)
        course_list.append(info)
    return course_list


async def get_mbas_course_detail(course_url,page,session):
    locations = get_masters_locations(page)
    takeaways = get_masters_takeaways(page)
    who_attend_desc = get_masters_who_attend(page)
    exec_ed_inquiry_cc_emails = get_contact_email(page)
    desc = get_masters_desc(page)
    video_info = get_masters_video_info(page)
    video_title = video_info["video_title"]
    video_url = video_info["video_url"]

    price_url = course_url + '/admissions'
    price_page = await download_site(price_url, session)
    price_info = get_masters_price_info(price_page)
    tuition = price_info['tuition']
    currency = price_info['currency']
    tuition_note = price_info['tuition_note']

    course_type = get_mbas_masters_course_type(page)
    print(course_type)
    duration_consecutive = ''
    if "Weekend" in course_type:
        duration_consecutive = 'No'
    else:
        duration_consecutive = 'Yes'
    course_type = course_type_map(course_type)
    testi_url = course_url+'experience/testimonials'
    testi_page = await download_site(testi_url, session)
    testimonials = get_masters_testimonial(testi_page)

    faculty_url = course_url+'/faculty'
    faculty_page = await download_site(faculty_url, session)
    faculty_list = await get_masters_faculty(faculty_page, session)

    start_date = get_mbas_start_date(page)
    if start_date:
        start_date = arrange_date_format(start_date)
    end_date = ''
    return {"location": locations,
            "exec_ed_inquiry_cc_emails":exec_ed_inquiry_cc_emails,
            "course_takeaways": takeaways,
            "who_attend_desc": who_attend_desc,
            "desc": desc,
            "video_title": video_title,
            "video_url": video_url,
            "tuition_number": tuition,
            "currency": currency,
            "tuition_note": tuition_note,
            "course_type": course_type,
            "testimonials": testimonials,
            "course_faculty": faculty_list,
            "effective_date_start":start_date,
            "effective_date_end":end_date,
            "duration_consecutive":duration_consecutive}


def get_mbas_masters_course_type(page):
    type = ''
    try:
        type_related_session = page.find('span', attrs={"class": "low"}, text="Format")
        type_session = type_related_session.find_previous("span")
        type = type_session.text
    except:
        pass
    return type


def get_mbas_start_date(page):
    start_date = ''
    try:
        start_date_related_session = page.find('span', attrs={"class": "low"}, text="Next Start")
        start_date_session = start_date_related_session.find_previous("span")
        start_date = start_date_session.text
    except:
        pass
    return start_date


async def get_masters_cate_course_detail(cate_page,cate_url,parent_url,session):
    course_list = []
    link_sessions = cate_page.find_all('div', attrs={"class": "box"})
    for link_session in link_sessions:
        cate_name = "Specialized Executive Masters"
        course_name = link_session.h6.text.title()
        duration_info = get_cate_duration(link_session)
        start_date = get_cate_start_date(link_session)
        end_date = get_cate_end_date(link_session)
        language = get_cate_language_info(link_session)
        course_link = link_session.get('onclick')
        _,href,course_partial_link = course_link.partition("href='")
        course_partial_link = course_partial_link.replace("'",'').replace(';','').strip()
        course_url = parse.urljoin("https://www.sdabocconi.it", course_partial_link)
        if start_date:
            start_date = arrange_date_format(start_date)
        if end_date:
            end_date = arrange_date_format(end_date)
        cate_page_info = {"name": course_name,
                "category": [cate_name],
                "category_url":[cate_url],
                "parent_url":parent_url,
                "effective_date_start": start_date,
                "effective_date_end": end_date,
                "language": language,
                "url": course_url,
                "credential":"Masters",
                "version":1}
        print(cate_page_info["url"])
        if cate_page_info["url"] == "https://www.sdabocconi.it/placeholder.url":
            continue
        if duration_info:
            duration_type = get_duration_type(duration_info)
            duration_type = 'duration_' + duration_type
            duration_num = get_duration_num(duration_info)
            cate_page_info[duration_type] = duration_num
        if course_url.endswith("program"):
            course_url = course_url[:-8]
        course_page = await download_site(course_url,session)
        course_page_info = await get_masters_course_detail(course_url,course_page,session)
        info = {**cate_page_info,**course_page_info}
        info = deal_with_schedule_related(info)
        course_list.append(info)
    course_list.pop()
    return course_list


async def get_masters_course_detail(url,page,session):
    locations = get_masters_locations(page)
    takeaways = get_masters_takeaways(page)
    who_attend_desc = get_masters_who_attend(page)
    exec_ed_inquiry_cc_emails = get_contact_email(page)
    desc = get_masters_desc(page)
    video_info = get_masters_video_info(page)
    video_title = video_info["video_title"]
    video_url = video_info["video_url"]

    price_url = url+'/admissions'
    price_page = await download_site(price_url,session)
    price_info = get_masters_price_info(price_page)
    tuition = price_info['tuition']
    currency = price_info['currency']
    tuition_note = price_info['tuition_note']

    course_type = get_mbas_masters_course_type(page)
    print(course_type)
    duration_consecutive = ''
    if "(" in course_type:
        duration_consecutive = 'No'
    else:
        duration_consecutive = 'Yes'
    course_type = course_type_map(course_type)
    testi_url = url+'/experience/testimonials'
    testi_page = await download_site(testi_url,session)
    testimonials = get_masters_testimonial(testi_page)

    duration = ''
    duration_info = get_masters_duration_info(page)

    faculty_url = url+'/faculty'
    faculty_page = await download_site(faculty_url,session)
    faculty_list = await get_masters_faculty(faculty_page,session)
    return {"location":locations,
            "exec_ed_inquiry_cc_emails":exec_ed_inquiry_cc_emails,
            "course_takeaways":takeaways,
            "who_attend_desc":who_attend_desc,
            "duration":duration_info,
            "desc":desc,
            "video_title":video_title,
            "video_url":video_url,
            "tuition_number":tuition,
            "currency":currency,
            "tuition_note":tuition_note,
            "course_type":course_type,
            "testimonials":testimonials,
            "course_faculty":faculty_list,
            "duration_consecutive":duration_consecutive}


def get_masters_duration_info(course_page):
    duration_info = ''
    try:
        duration_related_session = course_page.find('span', attrs={"class": "low"}, text="Duration")
        duration_session = duration_related_session.find_previous("span")
        duration_info = duration_session.text
    except:
        pass
    return duration_info


def get_masters_locations(course_page):
    locations = ''
    try:
        location_related_session = course_page.find('span', attrs={"class": "low"}, text="Where")
        location_session = location_related_session.find_previous("span").find('p')
        if not location_session:
            location_session = location_related_session.find_previous("span")
        locations = location_session.text
        locations = deal_with_location(locations)
    except:
        pass
    return locations


def get_masters_duration(course_page):
    duration = ''
    try:
        duration_related_session = course_page.find('span', attrs={"class": "low"}, text="Duration")
        duration_session = duration_related_session.find_previous("span")
        duration = duration_session.text
    except:
        pass
    return duration


def get_masters_desc(course_page):
    desc = ''
    try:
        desc_sessions = course_page.find('div',attrs={"class":"tinyHtml title-paragraph-prm"}).find_all('p')
        for desc_session in desc_sessions:
            desc += desc_session.text
        desc = desc.strip()
    except:
        pass
    return desc


def get_masters_video_info(course_page):
    video_url = ''
    video_title = ''
    try:
        video_url = course_page.find('div',attrs={"class":"videoLauncher"}).find('a').get('videourl')
    except:
        pass
    try:
        video_title = course_page.find('div',attrs={"class":"videoLauncher"}).find('div',attrs={"class":"title"}).text
    except:
        pass
    return {"video_title":video_title,
            "video_url":video_url}


def get_masters_who_attend(course_page):
    who_attend_desc = ''
    try:
        who_attend_desc = course_page.find("div",attrs={"class":"tinyHtml colsNum-1"}).text
        who_attend_desc = who_attend_desc.strip()
        who_attend_desc = re.sub("\s+", " ", who_attend_desc)
    except:
        pass
    return who_attend_desc


def get_contact_email(page):
    exec_ed_inquiry_cc_emails = ''
    try:
        contact = page.find('li',attrs={"class":"email"}).find('a')
        exec_ed_inquiry_cc_emails = contact.get('href')
        if exec_ed_inquiry_cc_emails.startswith("mailto:"):
            exec_ed_inquiry_cc_emails = exec_ed_inquiry_cc_emails[7:].strip()
        if '@' not in exec_ed_inquiry_cc_emails:
            exec_ed_inquiry_cc_emails = ''
    except:
        pass
    return exec_ed_inquiry_cc_emails


def get_masters_takeaways(course_page):
    takeaways = ''
    try:
        takeaways_related_sessions = course_page.find_all('div',attrs={"class":"whyChooseUsTips"})
        for takeaways_related_session in takeaways_related_sessions:
            txt = takeaways_related_session.text.strip()
            txt = re.sub("\s+", " ", txt)
            takeaways += txt+'\n'
        takeaways = takeaways.strip()
    except:
        pass
    return takeaways


def get_masters_price_info(page):
    tuition = ''
    currency = ''
    tuition_note = ''
    try:
        price_session = page.find('table',attrs={"class":"fees-table"})
        price_txt = price_session.find_all('strong')[-1].text
        tuition = get_tuition(price_txt)
    except:
        pass
    try:
        price_session = page.find('table', attrs={"class": "fees-table"})
        price_txt = price_session.strong.text
        currency = get_currency(price_txt)
    except:
        pass
    try:
        price_session = page.find('table', attrs={"class": "fees-table"}).find('tbody')
        tuition_note = price_session.text
        tuition_note = re.sub("\s+", " ", tuition_note)
    except:
        pass

    return {"tuition":tuition,
            "currency":currency,
            "tuition_note":tuition_note}


async def get_masters_faculty(page,session):
    faculty_list = []
    try:
        faculty_related_sessions = page.find_all("h6",attrs={"class":"title subtitle-h5"})
        for faculty_related_session in faculty_related_sessions:
            fac_link = faculty_related_session.find('a')
            if fac_link:
                fac_link = fac_link.get('href')
                fac_url = parse.urljoin("https://www.sdabocconi.it/",fac_link)
                fac_page = await download_site(fac_url,session)
                fac_info = get_one_fac_info(fac_page)
                if fac_info["name"] and fac_info["name"] != 'Ops, page not found!':
                    faculty_list.append(fac_info)
    except Exception as e:
        print(e)
    return faculty_list


def get_masters_testimonial(page):
    testimonials = []
    testi_related_sessions = page.find_all('div',attrs={"component":"TextShortenerComponent"})
    for testi_related_session in testi_related_sessions:
        testi_info = get_one_testi_info(testi_related_session)
        testimonials.append(testi_info)
    return testimonials


def get_one_testi_info(testi_session):
    name = ''
    title = ''
    company = ''
    testimonial_statement = ''
    picture_url = ''
    visual_url = ''
    active = "True"
    publish = 100
    try:
        name = testi_session.find('div',attrs={"class":"dida1"}).text.strip()
        if name and '-' in name:
            name_list = name.split('-')
            name = name_list[0].strip()
    except:
        pass

    try:
        testimonial_statement = testi_session.find('div',attrs={"class":"tinyHtml text-paragraph-prm "
                                                                        "trimTextImageText"}).text
    except:
        pass

    try:
        picture_url = testi_session.find('img').get('src')
    except:
        pass
    return {"name":name,
            "title":title,
            "company":company,
            "testimonial_statement":testimonial_statement,
            "picture_url":picture_url,
            "visual_url": visual_url,
            "active":active,
            "publish":publish}


def deal_with_schedule_related(detail):
    if "duration" in detail and detail["duration"]!= '':
        duration_type = get_duration_type(detail["duration"])
        duration_num = get_duration_num(detail["duration"])
        if duration_type == 'years':
            duration_type = "months"
            duration_num = duration_num * 12
        if detail["effective_date_start"] and not detail["effective_date_start"]:
            detail["effective_date_end"] = calculate_end_date(detail["effective_date_start"],duration_type,duration_num)
        detail_type = 'duration_'+duration_type
        detail[detail_type] = duration_num
        del detail["duration"]
    return detail


def course_type_map(type):
    if "Executive" and "Part" in type:
        return "Blended - Onsite & Self-paced"
    course_type = {"":"Onsite",
                   "Modular":"Onsite",
                   "Weekend or Modular":"Onsite",
                   "Full-Time": "Onsite",
                   "Full-time": "Onsite"}
    return course_type.get(type,'')



