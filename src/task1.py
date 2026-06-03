class AttributeRouter:
    __slots__ = ("_components", )

    def __init__(self, *components: object) -> None:
        object.__setattr__(self, "_components", components)


    def has_route(self, item: str) -> bool:
        if item == "_components":
            return True
        if item.startswith("_"):
            return False
        try:
            object.__getattribute__(self, item)
            return True
        except AttributeError:
            pass

        components = object.__getattribute__(self, "_components")

        for comp in components:
            try:
                getattr(comp, item)
                return True
            except AttributeError:
                continue
        return False

    def __getattribute__(self, item) -> object:
        if item.startswith("_"):
            return object.__getattribute__(self, item)
        try:
            return object.__getattribute__(self, item)
        except AttributeError:
            pass
        components = object.__getattribute__(self, "_components")
        for comp in components:
            try:
                return getattr(comp, item)
            except AttributeError:
                continue
        raise AttributeError(f"Аттрибута {item} нет")
