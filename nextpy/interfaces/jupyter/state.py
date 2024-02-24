import nextpy.interfaces.jupyter as xtj 

class State:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        # Automatically convert class attributes to state variables
        for attr_name, initial_value in cls.__dict__.items():
            if not callable(initial_value):
                setattr(cls, attr_name, xtj.reactive(initial_value))
