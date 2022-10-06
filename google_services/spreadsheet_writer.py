from typing import List, Any, Dict

from google_services.connections import get_spreadsheets_service, logger
from google_services.decorators import retry_with_backoff


@retry_with_backoff
def clear_sheet(spreadsheet_id: str, sheet_name: str, col_ranges: str = 'B3:Z') -> None:
    assert ':' in col_ranges
    clear_range = f'{sheet_name}!{col_ranges.upper()}'
    logger.warning("Be careful, you've run a table range cleanup: " + clear_range)
    get_spreadsheets_service().spreadsheets().values().batchClear(spreadsheetId=spreadsheet_id,
                                                                  body={'ranges': [clear_range]}).execute()


@retry_with_backoff
def write_data_on_sheet(spreadsheet_id: str, sheet_name: str, data: List[List[str]],
                        col_ranges: str = 'A:Z') -> Dict[str, Any]:
    assert ':' in col_ranges
    return get_spreadsheets_service().spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={"valueInputOption": "USER_ENTERED",
              "data": [{'range': f'{sheet_name}!{col_ranges.upper()}', 'majorDimension': 'ROWS', 'values': data}]}
    ).execute()
