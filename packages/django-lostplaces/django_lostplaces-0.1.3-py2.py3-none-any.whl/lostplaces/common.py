def get_all_subclasses(cls):
    '''
    Gets all subclasses recursively, does not contain
    abstract classes
    '''
    subclass_list = []
    for subclass in cls.__subclasses__():
        if not subclass._meta.abstract:
            subclass_list.append(subclass)
        subclass_list += get_all_subclasses(subclass)
    return subclass_list