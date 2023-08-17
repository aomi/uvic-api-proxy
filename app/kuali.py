import aiohttp
from .schemas.kuali import KualiCatalogItem, KualiCourseItem


class Kuali:
    async def get_catalogs(self) -> dict[str, str]:
        """
        Fetches a list of catalogs from the Kuali API.
        """
        url = "https://uvic.kuali.co/api/v1/catalog/public/catalogs/"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()
                for item in data:
                    # pydantic doesn't like it when we have a field that's underscored.
                    item["id"] = item["_id"]
                catalogs = [KualiCatalogItem(**item) for item in data]
                return catalogs

    async def get_catalogs_raw(self) -> dict[str, str]:
        """
        Fetches a list of catalogs from the Kuali API.
        """
        url = "https://uvic.kuali.co/api/v1/catalog/public/catalogs/"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return await resp.json()

    async def get_catalog(self, catalogId: str) -> dict[str, str]:
        """
        Fetches a single catalog from the Kuali API.
        """
        url = f"https://uvic.kuali.co/api/v1/catalog/public/catalogs/{catalogId}"
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
            ) as resp:
                print(resp.status)
                return await resp.json()

    async def get_course(self, catalogId: str, pid: str) -> dict[str, str]:
        """
        Fetches a single course for a term, subject, and course number.
        The course number is the course number as it appears in the catalog.
        ie. CSC 101 where 101 is the course number.
        """

        url = f"https://uvic.kuali.co/api/v1/catalog/course/{catalogId}/{pid}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()
                return KualiCourseItem(**data)

    async def get_courses(self, catalogId: str) -> dict[str, str]:
        """
        Fetches courses for a catalog.
        """
        url = f"https://uvic.kuali.co/api/v1/catalog/courses/{catalogId}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return await resp.json()
