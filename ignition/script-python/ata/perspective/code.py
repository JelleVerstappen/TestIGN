def getNavigationStructure(navigationDataset, userRoles = [], parentNavigationItemId = None, isMobile = False, showAll = False):
	"""
	Constructs a navigation structure from a specified data tag path. 
	This function processes navigation data and filters items based on user roles, mobile compatibility, parent-child relationship, and optionally shows all items.
	
	Args:
	    navigationDataset (Dataset): The Navigation Dataset.
	    userRoles (list, optional): A list of user roles for filtering navigation items. Defaults to an empty list.
	    parentNavigationItemId (str/None, optional): The ID of the parent navigation item for building a hierarchical structure. Defaults to None.
	    isMobile (bool, optional): Indicates if the navigation is being accessed on a mobile device. Defaults to False.
	    showAll (bool, optional): Determines whether to show all items regardless of other filtering conditions. Defaults to False.
	
	Returns:
	    list: A list of dictionaries representing the structured navigation items, each with potential child items.
	"""
	navData = system.dataset.toPyDataSet(navigationDataset)
	navHeaders = navData.getColumnNames()
	
	navItems = []
	for row in range(len(navData)):
		navItem = {column: navData[row][column] for column in navHeaders}

		# turn string of required roles into a list if not None
		navItem['required_roles'] = [role.strip() for role in navItem['required_roles'].split(',')] if navItem['required_roles'] is not None and navItem['required_roles'] != '' else None
		
		# check if this is a child of the give parent
		isChild = navItem['parent_navigation_item_id'] == parentNavigationItemId
		
		# determine if the function should include/return this item
		if showAll:
			showItem = isChild
		else:
			# retrieve the users roles
			userRoles = [] if userRoles is None else userRoles #if self.session.props.auth.user.roles == None else self.session.props.auth.user.roles
			
			# check if the user is authorized to see this item
			isAuthorized = navItem['required_roles'] is None or (True in [True if role in navItem['required_roles'] else False for role in userRoles]) 

			# check if it should be included on mobile
			includeOnMobile = True if navItem['exclude_on_mobile'] is None or not navItem['exclude_on_mobile'] else False
			
			# determine if the function should include the item
			showItem = navItem['label'] != '' and isAuthorized and isChild and (not isMobile or includeOnMobile)
		
		if showItem:
			# add children to the item (this makes this function recursive)
			children = getNavigationStructure(navigationDataset, parentNavigationItemId = navItem['id'], userRoles = userRoles, isMobile = isMobile, showAll = showAll)
			navItem.update({'children': children})
			
			# add navItem to navItems
			navItems.append(navItem)
		
	return navItems


def generateHorizontalMenuItems(navigationStructure = [],depth=0):
	"""
	Creates a tree-like menu structure for a horizontal menu component. This function processes navigation items in a recursive manner to build a detailed menu tree.
	
	Args:
	    navigationStructure (list, optional): A list of navigation items for constructing the menu tree. Defaults to an empty list.
	
	Returns:
	    list: A list of dictionaries, each dictionary representing a tree menu item, including properties like target path, child items, icon, label, visibility, and style options.
	"""
	items = []
	newDepth = depth + 1
	for navItem in navigationStructure:
		children = generateHorizontalMenuItems(navItem['children'],newDepth)
		if (depth == 0 and len(children) != 0) or depth > 0 or navItem['navigation_path'] == "/":
			items.append({
			  "enabled": True,
			  "target": navItem['navigation_path'],
			  "items": children,
			  "icon": {
			    "path": navItem['material_icon']
			  },
			  "label": navItem['label'],
			  "style": {
			    "classes": ""
			  }	
			})
	
	return items


def generateMenuTreeItems(navigationStructure = []):
	"""
	Creates a tree-like menu structure for the menu tree componenet. This function processes navigation items in a recursive manner to build a detailed menu tree.
	
	Args:
	    navigationStructure (list, optional): A list of navigation items for constructing the menu tree. Defaults to an empty list.
	
	Returns:
	    list: A list of dictionaries, each dictionary representing a tree menu item, including properties like target path, child items, icon, label, visibility, and style options.
	"""
	items = []
	for navItem in navigationStructure:
		children = generateMenuTreeItems(navItem['children'])
		items.append({
		  "target": navItem['navigation_path'],
		  "items": children,
		  "navIcon": {
		    "path": navItem['material_icon'],
		    "color": ""
		  },
		  "label": {
		    "text": navItem['label'],
		    "icon": {
		      "path": ""
		    }
		  },
		  "visible": True,
		  "enabled": True,
		  "showHeader": True,
		  "resetOnClick": False,
		  # "backActionText": "",
		  "style": {
		    "classes": ""
		  }
		})
	return items

def generateAccordionItems(navigationStructure = []):
	items = []
	for navItem in navigationStructure:
		children = generateMenuTreeItems(navItem['children'])
		defaultBody = {
		  "viewPath": "Library/SharedDocked/Templates/NavItems",
		  "viewParams": {},
		  "useDefaultViewWidth": False,
		  "useDefaultViewHeight": False,
		  "height": "auto",
		  "style": {
		    "classes": "",
		    "margin": 0
		  }
		}
			    
		navigationDict = {"expanded": False, 'body':defaultBody}
		navigationDict['target'] = navItem['navigation_path']
		navigationDict['body']['viewParams'] = {"list":children}
		navigationDict['header'] = {
		  "toggle": {
		    "enabled": True,
		    "expandedIcon": {
		      "path": "material/expand_less",
		      "color": "",
		      "style": {
		        "classes": ""
		      }
		    },
		    "collapsedIcon": {
		      "path": "material/expand_more",
		      "color": "",
		      "style": {
		        "classes": ""
		      }
		    }
		  },
		  "content": {
		    "type": "text",
		    "text":  navItem['label'],
		    "useDefaultViewWidth": False,
		    "useDefaultViewHeight": False,
		    "viewPath": "",
		    "viewParams": {},
		    "style": {
		      "classes": "",
		      "textAlign": "left"
		    }
		  },
		  "height": "40px",
		  "reverse": True,
		  "style": {
		    "classes": ""
		  }
		}
		items.append(navigationDict)
	return items
	    	

def openPopup(id, view, params={},title="",position={},showCloseIcon=True,draggable=False,resizable=False,modal=True,overlayDismiss=True,sessionId=None,pageId=None):
	system.perspective.openPopup(id=id, view=view, params=params,title=title,position=position,showCloseIcon=showCloseIcon,draggable=draggable,resizable=resizable,modal=modal,overlayDismiss=overlayDismiss,sessionId=sessionId,pageId=pageId)
	
	
def getSessionInfo(targetPage="", returnProps=False, returnCustom=False):
    """
    Retrieves active session information with the option to include session properties and custom properties.
    
    Args:
        targetPage (str): Filter for results based on the target view's page ID.
        returnProps (bool): If True, session properties ('props') will be included in the return.
        returnCustom (bool): If True, custom properties ('custom') will be included in the return.
    
    Returns:
        list: A list of dictionaries, each containing details about active sessions that have the target page open.
    """
    
    # Import the IgnitionGateway module
    from com.inductiveautomation.ignition.gateway import IgnitionGateway
    
    # Get the current project name
    projectName = system.util.getProjectName()
    
    # Get the context and module manager from the Ignition Gateway
    context = IgnitionGateway.get()
    moduleManager = context.getModuleManager()
    
    # Resolve the PropertyType class and get 'props' and 'custom' enums
    propTypeClass = moduleManager.resolveClass('com.inductiveautomation.perspective.common.api.PropertyType')
    propsEnum = propTypeClass.valueOf('props')
    customEnum = propTypeClass.valueOf('custom')
    
    # Get the PerspectiveContext class and instantiate it using the gateway context
    perspectiveContextClass = moduleManager.resolveClass('com.inductiveautomation.perspective.gateway.api.PerspectiveContext')
    perspectiveContext = perspectiveContextClass.get(context)
    
    # Get the PerspectiveSessionMonitor to monitor client sessions
    sessionMonitor = perspectiveContext.getSessionMonitor()
    
    # Retrieve the internal session list for the target project
    internalSessions = sessionMonitor.getClientSessionsForProject(projectName)
    
    # List to store active sessions that match the target page
    activeSessions = []
    
    # Loop through the internal sessions
    for sess in internalSessions:
        # Loop through each page of the session
        for page in sess.getPages():
            # Get the page ID
            pageId = page.getId()
            
            # Get the views associated with the page
            views = page.getViews()
            
            # Check if any view's ID matches the targetPage
            viewId, view = next(((str(view.getId()), view) for view in views if targetPage in str(view.getId())), (None, None))
            
            # If the target view is found
            if viewId and view:
                # Get the session object associated with the view
                session = view.getSession()
                
                # Retrieve session properties and custom properties using 'getPropertyTreeOf'
                sessionProps = dict(session.getPropertyTreeOf(propsEnum))
                sessionCustom = dict(session.getPropertyTreeOf(customEnum))
                
                # Extract the session ID from session properties
                sessionId = sessionProps.get('id')
                
                # Initialize a dictionary to store the session information
                sessionInfo = {}
                sessionInfo.update({'sessionId': sessionId})  # Add session ID
                sessionInfo.update({'view': viewId})  # Add view ID
                sessionInfo.update({'userName': sessionProps['auth']['user']['userName']})  # Add username
                
                # Include session properties if returnProps is True
                if returnProps:
                    sessionInfo.update({'props': sessionProps})
                
                # Include custom properties if returnCustom is True
                if returnCustom:
                    sessionInfo.update({'custom': sessionCustom})
                
                # Append the session information to the list of active sessions
                activeSessions.append(sessionInfo)
    
    # Return the list of active sessions
    return activeSessions