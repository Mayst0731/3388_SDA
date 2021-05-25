from urllib import parse
from detail.format_strings import get_tuition, get_currency
from download_parse import download_site


def get_course_price_info(course_page):
    tuition = ''
    currency = ''
    try:
        price_related_session = course_page.find('span',attrs={"class":"label"},text="Price (+ VAT)")
        if not price_related_session:
            price_related_session = course_page.find('span',attrs={"class":"label"},text="Prive (+ VAT)")
        if not price_related_session:
            price_related_session = course_page.find('span',attrs={"class":"label"},text="Fee")
        price_session = price_related_session.find_previous("h5")
        price = price_session.text
        tuition = get_tuition(price)
        currency = get_currency(price)
    except:
        pass
    price_info = {"tuition":tuition,
                  "currency":currency}
    return price_info


def get_course_language_info(course_page):
    lan = ''
    try:
        lan_related_session = course_page.find('span',attrs={"class":"label"},text="Language")
        lan_session = lan_related_session.find_previous("h5")
        lan = lan_session.text
    except:
        pass
    return lan


def get_course_loc_info(course_page):
    loc = ''
    try:
        loc_related_session = course_page.find('span',attrs={"class":"label"},text="Location")
        loc_session = loc_related_session.find_previous("h5")
        loc = loc_session.text
    except:
        pass
    return loc


def get_course_type(course_page):
    type = ''
    try:
        type_related_session = course_page.find('span', attrs={"class": "label"}, text="Format")
        type_session = type_related_session.find_previous("h5")
        type = type_session.text
    except:
        pass
    if not type:
        on_demand = course_page.find('span',text='On Demand')
        if on_demand:
            type = 'Online - Self-paced'
    return type


def get_overview(course_page):
    overview = ''
    try:
        overview_sessions = course_page.find('div',attrs={"class":"text-paragraph-prm"}).find_all('p')
        for overview_session in overview_sessions:
            if overview_session.get('style'):
                break
            else:
                overview += overview_session.text + '\n'
    except:
        pass
    overview = overview.strip()

    return overview


def get_takeaways(course_page):
    takeaways = ''
    try:
        takeaways_sessions = course_page.find('div', attrs={"class": "textWrapper tinyHtml "
                                                                     "text-paragraph-prm"}).find_all('li')
        for takeaways_session in takeaways_sessions:
            takeaways += takeaways_session.text + '\n'
        takeaways = takeaways.strip()
    except:
        pass
    return takeaways


def get_who_should_attend(course_page):
    who_attend = ''
    try:
        txt = 'Who is it for'
        who_attend_related_sessions = course_page.find_all('p')
        for who_attend_related_session in who_attend_related_sessions:
            p_text = who_attend_related_session.text
            if txt in p_text:
                if who_attend_related_session.find_next('p'):
                    who_attend += who_attend_related_session.find_next('p').text
                if who_attend_related_session.find_next('ul'):
                    who_attend_sessions = who_attend_related_session.find_next('ul').find_all('li')
                    for who_attend_session in who_attend_sessions:
                        who_attend += who_attend_session.text
    except Exception as e:
        print(e)
    return who_attend


def get_video_info(course_page):
    video_url = ''
    video_title = ''
    try:
        video_url = course_page.find_all('iframe')[-1].get('src')
        if video_url:
            video_url = parse.urljoin('https://www.youtube.com/',video_url)
    except:
        pass
    try:
        video_title = course_page.find_all('iframe')[-1].parent.parent.find_previous('p',attrs={"class":"title"}).text
    except:
        pass
    return {"video_title":video_title,
            "video_url":video_url}


async def get_faculties(course_page,session):
    faculties = []
    try:
        faculty_related_sessions = course_page.find_all('a',text="Go to CV")
        for faculty_related_session in faculty_related_sessions:
            faculty_link = faculty_related_session.get('href')
            if faculty_link:
                faculty = dict()
                faculty_url = parse.urljoin("https://www.sdabocconi.it/",faculty_link)
                title = faculty_related_session.parent.parent.parent.find_next('div',attrs={"class":"dida2"}).text
                faculty['title'] = title
                faculty_page = await download_site(faculty_url, session)
                faculty_other_info = get_one_fac_info(faculty_page)
                faculty.update(faculty_other_info)
                if faculty["name"] and faculty["name"] != "Ops, page not found!":
                    faculties.append(faculty)
    except:
        pass
    return faculties


def get_one_fac_info(fac_page):
    name = ''
    pic_url = ''
    intro_desc = ''
    pdf_url = ''
    try:
        name = fac_page.find('h1',attrs={"class":"title-h1 title-main"}).text.strip()
        if name and name != 'Ops, page not found!' and '-' in name:
            name_list = name.split('-')
            name = name_list[0].strip()
    except:
        pass

    try:
        pic_url = fac_page.find('div',attrs={"class":"teacherHeaderContainer"}).img.get('src')
    except:
        pass

    try:
        intro_desc_sessions = fac_page.find('div',attrs={"class":"plainTextContainer text-paragraph-prm"}).find_all('p')
        for intro_desc_session in intro_desc_sessions:
            intro_desc += intro_desc_session.text
        if intro_desc:
            intro_desc = intro_desc.strip()
    except:
        pass

    try:
        pdf_link = fac_page.find_all('a',attrs={"class":"link link-download"})[-1].get('href')
        if pdf_link:
            pdf_url = parse.urljoin("https://www.sdabocconi.it",pdf_link)
    except:
        pass
    faculty_other_info = {"name": name,
                          "title":"",
                          "pic_url": pic_url,
                          "intro_desc": intro_desc,
                          "pdf_url": pdf_url,
                          "university_school": "3388_EUR"}
    return faculty_other_info

