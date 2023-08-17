import aiohttp
import urllib.parse
from typing import Dict, Optional

ROOT_URL = 'https://banner.uvic.ca'
BANNER_SSB_URL = f'{ROOT_URL}/StudentRegistrationSsb/ssb'
BANNER_SSB_SEARCH_URL = f'{BANNER_SSB_URL}/classSearch/'
BANNER_SSB_SEARCH_GET_SUBJECTS = f'{BANNER_SSB_SEARCH_URL}/get_subject'
BANNER_SSD_SEARCH_RESULTS_URL = f'{BANNER_SSB_URL}/searchResults/searchResults'
BANNER_SSB_GET_TERMS = f'{BANNER_SSB_URL}/classSearch/getTerms'


class Banner():
    """
    Banner API client.
    """
    def __init__(self):
        self.terms = {}
        

    async def get_terms(self, offset: int = 1, max_items: int = 99) -> list[dict]:
        """
        Returns a list of terms from the Banner API.
        """
        url_params = {
            "searchTerm": "",
            "offset": offset,
            "max": max_items
        }
        # convert to url params
        params = urllib.parse.urlencode(url_params)

        url = f"{BANNER_SSB_GET_TERMS}?{params}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                html = await resp.text()
                print(html)
                print(resp.status)
                if resp.status == 200:
                    data = await resp.json()
                    print(data)
                    # store terms
                    for term in data:
                        self.terms[term['code']] = term
                    return data
                else:
                    raise Exception(f"Error getting terms: {resp.status}")
            
    async def get_subjects(self, term: str) -> list[dict]:
        jar = await self._get_cookie_jar(term)

        url_params = {
            "searchTerm": "",
            "term": term,
            "offset": 1,
            "max": 300,
        }
        # convert to url params
        params = urllib.parse.urlencode(url_params)

        url = f"{BANNER_SSB_SEARCH_GET_SUBJECTS}?{params}"

        async with aiohttp.ClientSession(cookie_jar=jar) as session:
            async with session.get(url) as resp:
                html = await resp.text()
                print(html)
                print(resp.status)
                if resp.status == 200:
                    data = await resp.json()
                    print(data)
                    return data
                else:
                    raise Exception(f"Error getting subjects: {resp.status}")

    @staticmethod
    def get_search_results_params(params: Dict[str, Optional[str]]) -> str:
        url_params = {
            "txt_subject": params.get("subject", ""),
            "txt_term": params.get("term", ""),
            "txt_courseNumber": params.get("courseNumber", ""),
            "startDatepicker": "",
            "endDatepicker": "",
            "pageOffset": str(params.get("offset", 0)),
            "pageMaxSize": str(params.get("max", 1000)),
            "sortColumn": "subjectDescription",
            "sortDirection": "asc",
        }

        return urllib.parse.urlencode(url_params)


    async def get_search_results(self, params: Dict[str, Optional[str]]):
        """
        Performs a search for courses.
        """
        jar = await self._get_cookie_jar(params["term"])
        print("params",params)
        url_params = Banner.get_search_results_params(params)
        print('url_params',url_params)
        url = f"{BANNER_SSD_SEARCH_RESULTS_URL}?{url_params}"

        async with aiohttp.ClientSession(cookie_jar=jar) as session:
            async with session.get(url) as resp:
                response = await resp.text()
                print(response)
                print(resp.status)

                return response



    # private method 
    async def _get_cookie_jar(self, term: str) -> aiohttp.CookieJar:
        """
        Returns a cookie jar for a given term.
        """
        jar = self.terms.get(term, aiohttp.CookieJar(unsafe=True))
        print("got jar",jar)
        return jar

    async def _set_term(self, term: str) -> aiohttp.CookieJar:
        """
        Sets the term cookie for a given term.
        """
        jar = await self._get_cookie_jar(term)

        url = f"{BANNER_SSB_URL}/term/search?mode=search"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        params = aiohttp.FormData()
        params.add_field("term", term)
        async with aiohttp.ClientSession(cookie_jar=jar) as session:
            async with session.post(url, data=params, headers=headers) as resp:
                if resp.status == 200:
                    self.terms[term] = jar
                    return True
                else:
                    raise Exception(f"Error getting subjects: {resp.status}")

