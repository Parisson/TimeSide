import timeside

def list_processors(interface, prefix=""):
    print prefix + interface.__name__
    subinterfaces = interface.__subclasses__()
    for i in subinterfaces:
        list_processors(i, prefix + "  ")
    processors = timeside.processors(interface, False)
    for p in processors:
        print prefix + "  %s [%s]" % (p.__name__, p.id())

list_processors(timeside.api.IProcessor)        
