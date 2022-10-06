from typing import List, Optional

from pydantic import BaseModel


class UrlItem(BaseModel):
    URL: str
    row_index: int = 0  # zero it is for testing on local
    scraped_time: str = None
    message: str = None


class UrlsData(BaseModel):
    data: List[UrlItem]
    sheet_name: str = None


class SheetResponse(BaseModel):
    status: str
    sheet_name: str
    data: List[UrlItem] = None
