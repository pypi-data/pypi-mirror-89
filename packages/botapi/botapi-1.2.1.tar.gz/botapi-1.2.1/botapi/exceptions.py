class TypeCastException(TypeError):
    def __init__(self, var_name, value, var_type):
        super().__init__(
            f"Can't cast {var_name} new value from {type(value)} to {var_type}"
        )
