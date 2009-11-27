import timeside

def list_processors(interface, prefix=""):
    print prefix + interface.__name__
    subinterfaces = interface.__subclasses__()
    for i in subinterfaces:
        list_processors(i, prefix + "  ")
    processors = timeside.processors(interface, False)
    for p in processors:
        print prefix + "  " + p.__name__

list_processors(timeside.api.IProcessor)        
