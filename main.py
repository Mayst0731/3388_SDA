import time
import aiohttp
import asyncio


from category import extract_categories
from detail import extract_details, integrate_details
from detail.masters_detail import get_comprehensive_master_mba_detail
from final_format import filter_out_final_categories, filter_out_final_courses, filter_out_final_faculties, \
    filter_out_final_details, add_masters_mbas_categories, add_masters_mbas_courses, \
    modify_mbas_masters_faculty_and_other_attr, delete_repeat_faculties
from write_to_json import write_to_json


async def start_crawler(url,online_url):
    session = aiohttp.ClientSession()
    category_list = await extract_categories(url,online_url,session)
    cate_page_detail = await extract_details(category_list, session)
    comprehensive_details = await integrate_details(cate_page_detail,session)

    final_categories = filter_out_final_categories(comprehensive_details)
    final_courses = filter_out_final_courses(comprehensive_details)
    final_faculties = filter_out_final_faculties(comprehensive_details)
    final_details = filter_out_final_details(comprehensive_details)

    # masters and mbas
    comprehensive_mbas_masters_details = await get_comprehensive_master_mba_detail(session)
    final_categories += add_masters_mbas_categories(comprehensive_mbas_masters_details)
    final_courses += add_masters_mbas_courses(comprehensive_mbas_masters_details)
    final_faculties += filter_out_final_faculties(comprehensive_mbas_masters_details)
    final_faculties = delete_repeat_faculties(final_faculties)
    final_details += modify_mbas_masters_faculty_and_other_attr(comprehensive_mbas_masters_details)
    write_to_json(final_categories, './final_outputfiles/category_3388_EUR_XW_0228.json')
    write_to_json(final_courses, './final_outputfiles/course_3388_EUR_XW_0228.json')
    write_to_json(final_faculties, './final_outputfiles/faculty_3388_EUR_XW_0228.json')
    write_to_json(final_details, './final_outputfiles/detail_3388_EUR_XW_0228.json')
    await session.close()
    return


if __name__ == '__main__':
    start_time = time.time()
    BASE_URL = 'https://www.sdabocconi.it/en/executive-open-programs'
    ONLINE_URL = "https://www.sdabocconi.it/en/online-programs"
    asyncio.run(start_crawler(BASE_URL,ONLINE_URL))
    duration = time.time() - start_time
    minutes = duration // 60
    print(f"Crawled {duration} seconds, {minutes} mins")
