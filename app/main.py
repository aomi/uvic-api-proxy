from litestar import Litestar, get
from .banner import Banner
from .kuali import Kuali

# setup clients for banner and kuali

banner = Banner()
kuali = Kuali()


@get(
    "/kuali/catalogs",
    tags=["Kuali"],
    description="Returns a list of catalogs. Returns the original data as-is.",
)
async def get_catalogs_raw() -> dict[str, str]:
    """
    Returns a list of catalogs.
    """
    catalogs = await kuali.get_catalogs_raw()
    return catalogs


@get("/catalogs", tags=["Kuali"], description="Returns a list of catalogs.")
async def get_catalogs() -> dict[str, str]:
    """
    Returns a list of catalogs.
    """
    catalogs = await kuali.get_catalogs()
    return catalogs


@get(
    "/catalogs/{catalogId:str}",
    tags=["Kuali"],
    description="Returns a catalog for a given id.",
)
async def get_catalog_by_id(catalogId: str) -> dict[str, str]:
    """
    Returns a list of courses for a catalog.
    """
    print(catalogId)
    catalog = await kuali.get_catalog(catalogId)
    return catalog


@get("/catalogs/{catalogId:str}/courses", tags=["Kuali"])
async def get_catalog_courses(catalogId: str) -> dict[str, str]:
    """
    Returns a list of courses for a catalog.
    """

    courses = await kuali.get_courses(catalogId)
    return courses


@get("/catalogs/{catalogId:str}/courses/{pid:str}", tags=["Kuali"])
async def get_catalog_course(catalogId: str, pid: str) -> dict[str, str]:
    """
    Returns a list of courses for a catalog.
    """

    course = await kuali.get_course(catalogId, pid)
    return course


@get("/terms", cache=True, tags=["Banner"])
async def get_terms() -> dict[str, str]:
    """
    Returns a list of terms.
    """
    terms = await banner.get_terms()
    return terms


@get("/terms/{term:str}/subjects")
async def get_subjects_by_term(term: str) -> dict[str, str]:
    """
    Returns a list of subjects for a term.
    """
    await banner._set_term(term)
    subjects = await banner.get_subjects(term)
    return subjects


@get("/terms/{term:str}/courses")
async def get_term_courses(term: str) -> dict[str, str]:
    await banner._set_term(term)
    courses = await banner.get_search_results(
        {
            "term": term,
        }
    )
    return courses


@get("/terms/{term:str}/courses/{subject:str}")
async def get_term_subject_courses(term: str, subject: str) -> dict[str, str]:
    courses = await banner.get_search_results(
        {
            "term": term,
            "subject": subject,
        }
    )
    return courses


@get("/terms/{term:str}/courses/{subject:str}/{course_number:str}")
async def get_term_subject_course(
    term: str, subject: str, course_number: str
) -> dict[str, str]:
    """
    Fetches a single course for a term, subject, and course number.
    The course number is the course number as it appears in the catalog.
    ie. CSC 101 where 101 is the course number.
    """
    courses = await banner.get_search_results(
        {
            "term": term,
            "subject": subject,
            "courseNumber": course_number,
        }
    )
    return courses


@get("/terms/{term:str}/courses/{subject:str}/{course_number:str}/sections")
async def get_term_subject_course_sections(
    term: str, subject: str, course_number: str
) -> dict[str, str]:
    courses = await banner.get_search_results(
        {
            "term": term,
            "subject": subject,
            "courseNumber": course_number,
        }
    )
    return courses


@get("/terms/{term:str}/courses/{subject:str}/{course_number:str}/textbooks")
async def get_term_subject_course_textbooks(
    term: str, subject: str, course_number: str
) -> dict[str, str]:
    raise NotImplementedError()


app = Litestar(
    route_handlers=[
        get_catalogs,
        get_catalog_by_id,
        get_catalog_courses,
        get_catalog_course,
        get_terms,
        get_subjects_by_term,
        get_term_courses,
        get_term_subject_courses,
        get_term_subject_course,
        get_term_subject_course_sections,
        get_term_subject_course_textbooks,
    ],
)
