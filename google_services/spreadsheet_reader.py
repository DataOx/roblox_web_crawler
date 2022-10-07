from typing import List, Any, Dict

from google_services.connections import get_spreadsheets_service
from google_services.decorators import retry_with_backoff


def dimension_unspecified_dict(values: List[List[Any]]) -> List[Dict[str, Any]]:
    keys = values[0]
    result_list = []

    for row in values[1:]:
        row_data = dict()

        for key in keys:
            try:
                value = row[keys.index(key)]
            except IndexError:
                value = ''
            row_data[key] = value

        result_list.append(row_data)

    return result_list


def columns_dict(values: List[List[Any]]) -> List[Dict[str, Any]]:
    result = []

    for row_id in range(len(values)):
        if row_id == 0:
            continue
        row_data = dict()

        for inner_iter_row in values:
            key = inner_iter_row[0]
            row_data[key] = inner_iter_row[row_id]

        result.append(row_data)

    return result


@retry_with_backoff
def get_sheet_data(spreadsheet_id: str, sheet_name: str, col_ranges: str = 'A:Z',
                   major_dimension: str = 'DIMENSION_UNSPECIFIED') -> List[Dict[str, Any]]:
    """
    service, spreadsheet_id: str, sheet_name: str, column_name: str, col_ranges: str = 'A:Z',
    all_columns: bool = False, ignore_columns: list = None
    """
    assert ':' in col_ranges
    assert major_dimension in ('DIMENSION_UNSPECIFIED', 'ROWS', 'COLUMNS')

    values = get_spreadsheets_service().spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                                                    range=f'{sheet_name}!{col_ranges.upper()}',
                                                                    majorDimension=major_dimension).execute()
    values = values.get('values')

    if not values:
        return []

    if major_dimension == 'COLUMNS':
        return columns_dict(values)

    return dimension_unspecified_dict(values)
