

def get_cate_language_info(link_session):
    language = ''
    try:
        info_div = link_session.find('div',attrs={"class":"box-info"})
        language_session = info_div.find('div',attrs={"class":"row-info"}).find('span',attrs={"class":"bold "
                                                                                                      "value"})
        language = language_session.text.title()
    except:
        pass
    return language


def get_cate_start_date(link_session):
    start_date = ''
    try:
        info_div = link_session.find('div', attrs={"class": "box-info"})
        start_related_session = info_div.find('span',text="Start date")
        start_date_session = start_related_session.find_next('span')
        start_date = start_date_session.text
    except:
        pass
    return start_date


def get_cate_end_date(link_session):
    end_date = ''
    try:
        info_div = link_session.find('div', attrs={"class": "box-info"})
        end_related_session = info_div.find('span',text="End date")
        end_date_session = end_related_session.find_next('span')
        end_date = end_date_session.text
    except:
        pass
    return end_date


def get_cate_duration(link_session):
    duration = ''
    try:
        info_div = link_session.find('div', attrs={"class": "box-info"})
        duration_session = info_div.find('div', attrs={"class": "row-info duration-field"}).find('span',
                                                                                                 attrs={"class":
                                                                                                             "bold "
                                                                                                          "value"})
        if not duration_session:
            duration_session = info_div.find('span', attrs={"class": "lable"},text="Total duration").find_next("span")
        duration = duration_session.text
    except:
        pass
    return duration


def get_cate_category(link_session):
    cate_name = link_session.find("div",attrs={"class":"box-ribbon"}).span.text
    return cate_name


