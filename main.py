from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from config import API_KEYS
from utils.items import UrlsData, SheetResponse
from utils.validators import is_invalid_roblox_url
from tasks import run_scraping_roblox


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def api_key_auth(api_key: str = Depends(oauth2_scheme)) -> None:
    if api_key not in API_KEYS:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden")


@app.get('/')
async def root():
    return {"status": "ok"}


@app.post("/roblox/start_scrape/", dependencies=[Depends(api_key_auth)])
async def spreadsheet_urls(urls: UrlsData) -> SheetResponse:
    """
    to get scraping requests from google spreadsheet
    """
    valid_urls, invalid_urls = [], []
    added_urls = dict()

    for url_item in urls.data:
        # filtering to duplicates key=URL value=row_index
        if url_item.URL in added_urls.keys():
            url_item.message = "Duplicated with value from row " + added_urls[url_item.URL]
            invalid_urls.append(url_item)
            continue

        # checking the URL is valid.
        # If it is not, the message will be changed in the body of the is_invalid_roblox_url function.
        if is_invalid_roblox_url(url_item):
            invalid_urls.append(url_item)
        else:
            valid_urls.append(url_item)

        added_urls[url_item.URL] = str(url_item.row_index)

    response = SheetResponse(status="ok", sheet_name=urls.sheet_name, data=valid_urls + invalid_urls)
    if invalid_urls:
        response.status = "Invalid URLs found"

    if valid_urls:
        urls.data = valid_urls
        run_scraping_roblox.delay(urls)

    return response
