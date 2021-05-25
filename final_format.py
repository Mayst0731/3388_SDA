from detail.format_strings import get_duration_type, get_duration_num, calculate_end_date, calculate_duration_info


def filter_out_final_categories(details):
    category_list = []
    for detail in details:
        category_zip = zip(detail["category"],detail["category_url"])
        for category in category_zip:
            if "executive-open-programs" in category[1]:
                parent_url = "https://www.sdabocconi.it/en/executive-open-programs"
                category_info = {"category":category[0],
                                 "url":category[1],
                                 "parent_url":parent_url}
                category_list.append(category_info)
            elif "online-programs" in category[1]:
                parent_url = "https://www.sdabocconi.it/en/online-programs"
                category_info = {"category": category[0],
                                 "url": category[1],
                                 "parent_url": parent_url}
                category_list.append(category_info)
            else:
                continue
    final_categories = delete_repeat_categories(category_list)
    return final_categories


def add_masters_mbas_categories(details):
    category_list = []
    category_set = set()
    for detail in details:
        for cate in detail["category"]:
            if cate not in category_set:
                category_set.add(cate)
                category_info = {"category": cate,
                                 "url": detail["category_url"][0],
                                 "parent_url": detail["parent_url"]}
                category_list.append(category_info)
    return category_list


def delete_repeat_categories(category_list):
    final_category_list = []
    category_set = set()

    for category in category_list:
        if category["category"] not in category_set:
            category_set.add(category["category"])
            final_category_list.append(category)
    return final_category_list



def filter_out_final_courses(details):
    course_list = []
    for detail in details:
        course = {"name":detail["name"],
                  "url": detail["url"],
                  "category_name":detail["category"],
                  "category_url":detail["category_url"]
                  }
        course_list.append(course)
    return course_list


def add_masters_mbas_courses(details):
    course_list = []
    course_set = set()
    for detail in details:
        if detail["url"] not in course_set:
            course_set.add(detail["url"])
            course_info = {"name": detail["name"],
                      "url": detail["url"],
                      "category_name": detail["category"],
                      "category_url": detail["category_url"]
                      }
            course_list.append(course_info)
    return  course_list


def filter_out_final_faculties(details):
    faculty_list = []
    for detail in details:
        try:
            faculty_list += detail["course_faculty"]
            faculty_list = delete_repeat_faculties(faculty_list)
        except:
            pass
    faculty_list = delete_repeat_faculties(faculty_list)
    return faculty_list


def delete_repeat_faculties(faculty_list):
    final_faculty_list = []
    faculty_set = set()
    for faculty in faculty_list:
        if faculty["name"] not in faculty_set:
            faculty_set.add(faculty["name"])
            final_faculty_list.append(faculty)
        else:
            continue
    return final_faculty_list


def filter_out_final_details(details):
    final_details = []
    for detail in details:
        course_faculties = []
        locations = deal_with_location(detail["location"])
        course_type = deal_with_course_type(detail["course_type"])
        if len(detail["course_faculty"]) > 0:
            for faculty in detail["course_faculty"]:
                course_faculty = faculty['name']
                course_faculty = course_faculty.strip()
                course_faculties.append(course_faculty)
        final_detail = {"name":detail["name"],
                        "url":detail["url"],
                        "university_school":"3388_EUR",
                        "category":detail["category"],
                        "priority":0,
                        "publish": 100,
                        "version":1,
                        "location":locations,
                        "currency":detail["currency"],
                        "tuition_number":detail["tuition"],
                        "tuition_note":"",
                        "Repeatable":"Y",
                        "exec_ed_inquiry_cc_emails":detail["exec_ed_inquiry_cc_emails"],
                        "effective_date_start":detail["effective_date_start"],
                        "effective_date_end":detail["effective_date_end"],
                        "languages":detail["language"],
                        "course_takeaways":detail["course_takeaways"],
                        "course_faculties": course_faculties,
                        "who_attend_desc":detail["who_attend_desc"],
                        "video_title":detail["video_title"],
                        "video_url":detail["video_url"],
                        "desc":detail["overview"],
                        "type":course_type,
                        "testimonials": detail["testimonials"]}
        overview = {"desc": final_detail["desc"],
                    "video_title": final_detail["video_title"],
                    "video_url": final_detail["video_url"]}
        final_detail["overview"] = overview
        del final_detail["desc"]
        del final_detail["video_title"]
        del final_detail["video_url"]
        final_detail["audience_title_level"] = ''
        final_detail["is_advanced_management_program"] = False
        final_detail["who_attend_params"] = '{\"working experience":\"\",\"background knowledge\": \"\"}'
        final_detail["duration_desc"] = ''
        final_detail["category_tags"] = []
        final_detail["active"] = True
        final_detail["duration_consecutive"] = detail.get("duration_consecutive","Yes")
        final_detail["credential"] = detail.get("credential","")
        if not detail["effective_date_start"] and not detail["effective_date_end"] and not detail["duration"]:
            final_detail["schedule"] = [[detail["effective_date_start"],
                                        detail["effective_date_end"],
                                        "",
                                        "formal"]]
        else:
            duration = calculate_duration_info(detail["effective_date_start"],detail["effective_date_end"])
            duration_type = duration["duration_type"]
            duration_num = duration["duration_num"]
            duration_type = 'duration_' + duration_type
            final_detail["schedule"] = [[detail["effective_date_start"],
                                        detail["effective_date_end"],
                                        str(duration_num),
                                        "formal"]]
            final_detail[duration_type] = duration_num
        if "duration_" in final_detail:
            final_detail["duration_days"] = 1
            del final_detail["duration_"]
        final_details.append(final_detail)
    return final_details


def deal_with_location(locations):
    if "(" in locations:
        left_parenthesis_idx = locations.index("(")
        locations = locations[:left_parenthesis_idx]
        locations = locations.replace("and",',')
    location_dict = {"Milano":"Milano, ----, Italy",
                     "Beijing":"Beijing, ----, China",
                     "Mumbai":"Mumbai, ----, India",
                     "New Delhi":"New Delhi, ----, India",
                     "Rome": "Rome, ----, Italy",
                     "Paris":"Paris, ----, France",
                     "London": "London, ----, United Kingdom",
                     "Dubai":"Dubai, ----, United Arab Emirates",
                     "Madrid":"Madrid, ----, Spain",
                     "Barcelona":"Barcelona, ----, Spain",
                     "Roma":"Rome, ----, Italy",
                     "Toronto": "Toronto, ON, Canada",
                     "Shanghai":"Shanghai, ----, China",
                     "San Francisco":"San Francisco, CA, United States",
                     "Copenhagen":"Copenhagen, ----, Denmark"}
    final_locations = []
    if locations == '' or locations == 'Milano':
        final_locations = ["Milano, ----, Italy"]
    elif ',' in locations:
        location_list = locations.split(',')
        for location in location_list:
            location = location.strip()
            if "Paulo" in location:
                final_locations.append("Sao Paulo, ----, Brazil")
            else:
                final_loc = location_dict[location]
                final_locations.append(final_loc)
    else:
        final_locations = ["Milano, ----, Italy"]
    return final_locations


def deal_with_course_type(course_type):
    course_type_dict = {"Class":"Onsite",
                        "Online - Self-paced":"Online - Self-paced",
                        "Blended":"Blended - Onsite & Self-paced",
                        "Online":"Online - Self-paced"}
    return course_type_dict[course_type]


def get_duration_num(detail):
    num = ''
    if "duration_days" in detail:
        num = detail["duration_days"]
    elif "duration_weeks" in detail:
        num = detail["duration_weeks"]
    elif "duration_months" in detail:
        num = detail["duration_months"]
    elif "duration_years" in detail:
        num = detail["duration_years"]
    return num


def add_schedule(detail):
    schedule = ["","","","formal"]
    schedule[0] = detail["effective_date_start"]
    schedule[1] = detail["effective_date_end"]
    schedule[2] = detail.get("duration_days",'')
    if schedule[2] == '':
        schedule[2] = detail.get("duration_weeks", '')
    if schedule[2] == '':
        schedule[2] = detail.get("duration_months", '')
    if schedule[2] == '':
        schedule[2] = detail.get("duration_years", '')
    schedule[2] = str(schedule[2])
    return schedule


def modify_mbas_masters_faculty_and_other_attr(details):
    for detail in details:
        overview = {"desc":detail["desc"],
                    "video_title":detail["video_title"],
                    "video_url":detail["video_url"]}
        detail["overview"] = overview
        del detail["desc"]
        del detail["video_title"]
        del detail["video_url"]
        detail["audience_title_level"] = ''
        detail["is_advanced_management_program"] = False
        detail["who_attend_params"] = '{\"working experience":\"\",\"background knowledge\": \"\"}'
        detail["duration_desc"] = ''
        detail["languages"] = detail["language"]
        del detail["language"]
        detail["type"] = detail["course_type"]
        del detail["course_type"]
        detail["active"] = True
        detail["category_tags"] = []
        del detail["category_url"]
        detail["publish"] = 100
        detail["priority"]= 0
        detail["Repeatable"] = 'Y'
        detail["university_school"] = detail.get("university_school",'3388_EUR')
        if "duration_years" in detail:
            detail["duration_months"] = detail["duration_years"] * 12
            del detail["duration_years"]
        if "&" in detail["languages"]:
            detail["languages"] = get_language_list(detail["languages"])
        if "course_faculty" in detail and len(detail["course_faculty"]) > 0:
            new_fac_list = []
            for fac in detail["course_faculty"]:
                new_fac = fac["name"]
                new_fac_list.append(new_fac)
            detail["course_faculties"] = new_fac_list
            del detail["course_faculty"]
        else:
            detail["course_faculties"] = []
        if "course_faculty" in detail:
            del detail["course_faculty"]
    return details


def get_language_list(languages):
    language_list = []

    language_lst = languages.split('&')
    for language in language_lst:
        if 'Eng' in language:
            language_list.append("English")
        if 'Ita' in language:
            language_list.append("Italy")
    return language_list