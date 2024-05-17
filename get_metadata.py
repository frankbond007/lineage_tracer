import openpyxl as op
import logging


def get_metadata_from_sheet(file_name, sheet_name):
    """
    Extracts metadata from an Excel sheet.

    Parameters:
    file_name (str): The path to the Excel file.
    sheet_name (str): The name of the sheet to read from.

    Returns:
    list: A list of tuples containing the metadata.
    """
    file_path = file_name
    columns_to_read = ['source_tables', 'target_table', 'transformation_id']

    try:
        workbook = op.load_workbook(file_path, data_only=True)
        worksheet = workbook[sheet_name]
        metadata = []

        header_row = worksheet[1]
        header_values = [cell.value for cell in header_row]

        for col in columns_to_read:
            if col not in header_values:
                raise ValueError(f"Column '{col}' not found in sheet '{sheet_name}'")

        column_indices = [header_values.index(header) for header in columns_to_read]
        for row in worksheet.iter_rows(min_row=2, values_only=True):
            row_data = tuple((str(row[i]).lower().strip() if row[i] is not None else None) for i in column_indices)
            metadata.append(row_data)

        return metadata

    except FileNotFoundError:
        logging.error(f"File '{file_path}' not found")
        return []
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return []
