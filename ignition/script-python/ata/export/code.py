def exportTableToExcel(table, filename):
    """
    Exports table data to an Excel file.

    Args:
        table (com.inductiveautomation.perspective.table.TableComponent): The table component.
        filename (str): The name of the Excel file.
    """
    columns = table.props.columns
    headerNames = {}
    header = []

    # Extract visible column information
    for col in columns:
        if col.visible:
            field = col.field
            headerNames[field] = col.header.title
            header.append(field)

	try:
		filteredData = table.props.filter.results.data[0]
		data = table.props.filter.results.data
		data = ata.format.json.toDataset(data)
	except:
		data = table.props.data
		if not ata.validation.isDataset(data):
			data = ata.format.json.toDataset(data)

    # Filter columns
    data = system.dataset.filterColumns(data, header)

    # Convert dataset to Excel format
    excelData = system.dataset.toExcel(True, [data])

    # Download the Excel file
    system.perspective.download(filename, excelData)
