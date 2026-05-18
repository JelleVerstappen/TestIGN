def getDevices():
    """
    Get all PLCs (Programmable Logic Controllers) that are configured in the Ignition gateway.

    Returns:
        Dataset: A dataset containing the names of all PLCs.
    """
    # Get a dataset with every device
    Devices = system.device.listDevices()

    # Create an empty dataset to store the information
    headers = ["PLCName"]
    data = system.dataset.toDataSet(headers, [])

    # Loop through all the devices and add them to the dataset
    for row in range(Devices.rowCount):
        PLCName = Devices.getValueAt(row, "Name")
        # Add them to the dataset
        NewRow = [PLCName]
        data = system.dataset.addRow(data, NewRow)

    # Return the dataset
    return data


def getDatabaseConnections():
    """
    Get all database connections configured in the Ignition gateway.

    Returns:
        Dataset: A dataset containing the names of all database connections.
    """
    # Get a dataset with every database connection
    Connections = system.db.getConnections()

    # Create an empty dataset to store the information
    headers = ["DatabaseName"]
    data = system.dataset.toDataSet(headers, [])

    # Loop through all the database connections and add them to the dataset
    for row in range(Connections.rowCount):
        DatabaseName = Connections.getValueAt(row, "Name")
        # Add them to the dataset
        NewRow = [DatabaseName]
        data = system.dataset.addRow(data, NewRow)

    # Return the dataset
    return data


def clientPerformance(request=None):
    """
    Get performance information about the Ignition server or client.

    Args:
        request (str, optional): Specifies the type of information to retrieve ("cpu", "totalmem", "freemem", "memutil").

    Returns:
        float or list: The requested performance information.
    """
    # import library
    import java.lang.management.ManagementFactory as MF

    # Get all the system information
    mbs = MF.getOperatingSystemMXBean()
    cpu = mbs.getSystemCpuLoad() * 100
    totalmem = mbs.getTotalPhysicalMemorySize()
    freemem = mbs.getFreePhysicalMemorySize()
    usedmem = (totalmem - freemem)
    memutil = float(usedmem) / float(totalmem) * 100

    # Return value based on the parameter of this function
    if request == "cpu":
        return round(cpu, 2)
    elif request == "totalmem":
        return ((totalmem / 1024) / 1024)
    elif request == "freemem":
        return ((freemem / 1024) / 1024)
    elif request == "memutil":
        return round(memutil, 2)
    else:
        return [cpu, totalmem, freemem, memutil]


def getClients():
    """
    Update the list of online devices (clients) in the Ignition gateway.

    Returns:
        None
    """
    # Get session information
    sessions = system.perspective.getSessionInfo()
    tagProvider = ata.config.defaultTagProvider
    devices = []

    # Loop through all sessions and gather device information
    for device in sessions:
        client = {}
        if 'Android' in device['userAgent']:
            client['OS'] = 'Android'
        elif 'Windows' in device['userAgent']:
            client['OS'] = 'Windows'
        elif 'iPhone' in device['userAgent']:
            client['OS'] = 'iPhone'
        elif 'Mac' in device['userAgent']:
            client['OS'] = 'Mac'
        else:
            client['OS'] = 'Designer'

        client['username'] = device['username']
        client['IP'] = device['clientAddress']
        seconds = device['uptime'] / 1000
        uptime = ata.date.secondsToTime(seconds, True)   
        client['uptime'] = uptime
        devices.append(client)
	
    # Write the gathered device information to a tag
    system.tag.writeBlocking(['['+str(tagProvider)+']System/Server/Devices'], [system.util.jsonEncode(devices)])


def getSystemPerformance():
    """
    Get performance information about the system and update related tags in the Ignition gateway.

    Returns:
        None
    """
    from java.lang.management import ManagementFactory
    
    tagProvider = ata.config.defaultTagProvider

    # Get operating system bean
    bean = ManagementFactory.getOperatingSystemMXBean()
    gigs = 2 ** 20
    totalMem = bean.getTotalPhysicalMemorySize()
    freeMem = bean.getFreePhysicalMemorySize()

    TotalMemory = totalMem / gigs
    FreeMemory = freeMem / gigs
    UsedMemory = (totalMem - freeMem) / gigs
    TotalCPULoad = bean.getSystemCpuLoad() * 100

    # Callback function for asynchronous tag write
    def callback(a):
        pass
        return

    # Write performance information to tags asynchronously
    system.tag.writeAsync(['['+str(tagProvider)+"]System/Server/Max Memory",
                           '['+str(tagProvider)+"]System/Server/Free Memory",
                           '['+str(tagProvider)+"]System/Server/Used Memory",
                           '['+str(tagProvider)+"]System/Server/CPU Usage"],
                          [TotalMemory,
                           FreeMemory,
                           UsedMemory,
                           TotalCPULoad], callback)

