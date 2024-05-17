import openpyxl as op

def get_metadata_from_sheet(file_name, sheet_name):

    file_path = file_name

    columns_to_read = ['source_tables', 'target_table', 'transformation_id']
    try:
        workbook = op.load_workbook(file_path, data_only=True)
        worksheet = workbook[sheet_name]
        metadata = []
        header_row = worksheet[1]
        header_values = [cell.value for cell in header_row]

        column_indices = [header_values.index(header) for header in columns_to_read]
        for row in worksheet.iter_rows(min_row=2, values_only=True):
            row_data = tuple((str(row[i]).lower().strip() if row[i] is not None else None) \
                             for i in column_indices)
            metadata.append(row_data)
        return metadata
    except FileNotFoundError:
        return f"File '{file_path}' not found"
    except Exception as e:
        return f"An error occured: {e}"