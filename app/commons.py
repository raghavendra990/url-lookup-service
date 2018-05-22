



def isGeneratorObjectEmpty(items):
    
    if items is None:
        return False
    if not items:
        return False
    try:
        iterator = iter(items)
        next_item = next(items)
    except Exception as ex:
        return False
    else:
        return next_item