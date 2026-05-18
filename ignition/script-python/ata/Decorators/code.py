from functools import wraps


def measure_elapsed_time(func):
    """Decorator function. Logs debug messages for the total elapsed time 
       running the given function.

    Args:
        func (function): the function to be wrapped
        
    Returns:
        result: the result of the called function
    """
    calling_module = func.__module__
    calling_function = func.__name__
    logger = system.util.getLogger("SAB.measure_elapsed_time")
    
    @wraps(func)
    def func_wrapper(*args, **kvargs):	
        start_time = system.date.toMillis(system.date.now())
        logger.debugf(
            "Function %s started. Timestamp: %d.",
            calling_function,
            start_time
        )
        result = func(*args, **kvargs)
        end_time = system.date.toMillis(system.date.now())
        elapsed_time = end_time - start_time
        logger.debugf(
            "Function %s completed. Timestamp: %d. Total elapsed time: %d ms",
            calling_function,
            end_time,
            elapsed_time
        )
        return result
    return func_wrapper


def catch_exceptions(package_name="unknown"):
    """Decorator function. Adds exception catching and logs traceback.

    Args:
        func (function): the function to be wrapped
        
    Returns:
        result: the result of the called function, or None if exceptions are raised.
    """
    import sys
    from java.lang import Exception as JavaException
    import traceback
    
    def decorator(func):
        calling_module = func.__module__
        calling_function = func.__name__
        logger = system.util.getLogger("SAB.catch_exceptions")
        
        @wraps(func)
        def func_wrapper(*args, **kvargs):
            try:
                return func(*args, **kvargs)
            except (JavaException, Exception), e:
                # get line number and exception info for the log
                tb = sys.exc_info()[2]
                if traceback:
                    logger.errorf(
                        "Exception: %s in <%s.%s.%s>. %s",
                        str(e),
                        package_name,
                        calling_module,
                        calling_function,
                        str(traceback.format_exc()),
                    )
                else:
                    logger.errorf(
                        "Exception: %s in <%s.%s.%s>. No Traceback.",
                        str(e),
                        package_name,
                        calling_module,
                        calling_function,
                    )
            return None
            
        return func_wrapper
        
    # The double wrapping is needed for the decorator to accept parameters
    return decorator