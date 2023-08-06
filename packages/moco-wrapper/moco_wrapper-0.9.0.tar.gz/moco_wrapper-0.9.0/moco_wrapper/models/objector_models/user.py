from moco_wrapper.models import objector_models as obj


class User(object):
    def __init__(
        self, 
        **kwargs
        ):
        
        nk = kwargs
        if "unit" in kwargs.keys():
            u = obj.Unit(**kwargs["unit"])
            
            del nk["unit"]
            nk["unit"] = u

        if "bday" in nk.keys():
            nk["birthday"] = nk["bday"]
            del nk["bday"]

        self.__dict__.update(nk)
        