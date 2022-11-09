class BaseMarkup:
    pass


class Markup(BaseMarkup):
    text = None
    keyboard = None
    kwargs = None

    def __init__(self, **kwargs):
        super(Markup, self).__init__(**kwargs)
        self.kwargs = kwargs
        try:
            self.keyboard = kwargs.pop("keyboard")
        except KeyError:  # keyboard is not required
            pass

        if self.text:
            self.text = self.text.__format__(**kwargs)
