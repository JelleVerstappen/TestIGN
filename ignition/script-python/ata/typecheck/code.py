def dataset(dataset):
    """
    Checks if the given object is an Ignition dataset.

    Args:
        dataset: The object to be checked.

    Returns:
        bool: True if the object is a dataset, False otherwise.
    """
    return str(type(dataset)) in ["<type 'com.inductiveautomation.ignition.common.BasicDataset'>",
                                  "<type 'com.inductiveautomation.ignition.common.JsonDataset'>",
                                  "<type 'com.inductiveautomation.ignition.gateway.datasource.BasicStreamingDataset'>"]


def string(value, field, errors):
    """
    Validates and cleans a string value for a specified field.

    Args:
        value: The input value to be validated and cleaned.
        field (str): The field name associated with the value.
        errors (List): A list to store error messages.

    Returns:
        tuple: A tuple containing the cleaned value and the list of errors.
    """
    try:
        field = system.util.translate(field)
        value = str(value).strip()
        if len(value) == 0:
            errors.add(system.util.translate("Value may not be empty for field") + ": {}.".format(field))
        else:
            return value, errors
    except Exception:
        errors.add(system.util.translate("Value can't be cast to string for field") + ": {}.".format(field))
    
    return value, errors


def bool(value, field, errors):
    """
    Converts a value to a boolean and handles errors.

    Args:
        value: The input value to be converted to a boolean.
        field (str): The field name associated with the value.
        errors (List): A list to store error messages.

    Returns:
        tuple: A tuple containing the converted boolean value and the list of errors.
    """
    try:
        field = system.util.translate(field)
        value = bool(value)
    except Exception:
        errors.add(system.util.translate("Value can't be cast to boolean for field") + ": {}.".format(field))
    
    return value, errors


def date(value, field, errors):
    """
    Converts a value to a date and handles errors.

    Args:
        value: The input value to be converted to a date.
        field (str): The field name associated with the value.
        errors (List): A list to store error messages.

    Returns:
        tuple: A tuple containing the converted date value and the list of errors.
    """
    try:
        field = system.util.translate(field)
        type = str(type(value))
        if type == str("<type 'long'>"):
            value = system.date.fromMillis(value)
        elif type == str("<type 'java.util.Date'>"):
            value = system.date.addDays(value, 0)
        else:
            raise Exception('')
    except Exception:
        errors.add(system.util.translate("Value can't be cast to date for field") + ": {}.".format(field))
    
    return value, errors


def integer(value, field, errors):
    """
    Converts a value to an integer and handles errors.

    Args:
        value: The input value to be converted to an integer.
        field (str): The field name associated with the value.
        errors (List): A list to store error messages.

    Returns:
        tuple: A tuple containing the converted integer value and the list of errors.
    """
    try:
        field = system.util.translate(field)
        value = int(value)
    except Exception:
        errors.add(system.util.translate("Value can't be cast to integer for field") + ": {}.".format(field))
        
    return value, errors