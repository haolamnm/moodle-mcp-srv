"""Course tool implementations."""

from __future__ import annotations

from moodle_mcp.api._helpers import get_enrolled_courses
from moodle_mcp.api.coercion import (
    as_int,
    as_optional_float,
    as_optional_int,
    as_optional_str,
    as_str,
    object_list,
)
from moodle_mcp.models import Course, CourseSection, Module, SiteInfo
from moodle_mcp.moodle import APIFunction, get_moodle_api_data, resolve_current_user_id


async def get_site_info() -> SiteInfo:
    """Return authenticated Moodle site and user metadata."""
    data = await get_moodle_api_data(APIFunction.core_webservice_get_site_info)
    data_object = data if isinstance(data, dict) else {}

    return SiteInfo(
        sitename=as_str(data_object.get("sitename")),
        siteurl=as_optional_str(data_object.get("siteurl")),
        userid=as_int(data_object.get("userid")),
        username=as_optional_str(data_object.get("username")),
        firstname=as_optional_str(data_object.get("firstname")),
        lastname=as_optional_str(data_object.get("lastname")),
        fullname=as_optional_str(data_object.get("fullname")),
        release=as_optional_str(data_object.get("release")),
        version=as_optional_str(data_object.get("version")),
    )


async def get_my_courses() -> list[Course]:
    """Return all courses the current user is enrolled in."""
    userid = await resolve_current_user_id()
    courses_raw = await get_enrolled_courses(userid)
    courses: list[Course] = []

    for course in courses_raw:
        courses.append(
            Course(
                id=as_int(course.get("id")),
                fullname=as_str(course.get("fullname")),
                shortname=as_str(course.get("shortname")),
                category=as_int(course.get("category")),
                summary=as_str(course.get("summary")),
                startdate=as_optional_int(course.get("startdate")),
                enddate=as_optional_int(course.get("enddate")),
                progress=as_optional_float(course.get("progress")),
            )
        )
    return courses


async def get_course_content(courseid: int) -> list[CourseSection]:
    """Return sections and modules for a given course."""
    data = await get_moodle_api_data(
        APIFunction.core_course_get_contents,
        {"courseid": str(courseid)},
    )
    if not isinstance(data, list):
        return []

    sections: list[CourseSection] = []
    for section in object_list(data):
        modules: list[Module] = []
        for module in object_list(section.get("modules")):
            modules.append(
                Module(
                    id=as_int(module.get("id")),
                    name=as_str(module.get("name")),
                    modname=as_str(module.get("modname")),
                    url=as_optional_str(module.get("url")),
                    description=as_optional_str(module.get("description")),
                )
            )
        sections.append(
            CourseSection(
                id=as_int(section.get("id")),
                name=as_str(section.get("name")),
                summary=as_optional_str(section.get("summary")),
                modules=modules,
            )
        )
    return sections
