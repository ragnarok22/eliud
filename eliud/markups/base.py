class BaseMarkup:
    """
    Base class for Markups
    """

    def __init__(self, **kwargs):
        """
        :keyword text: Text to send
        :keyword kwargs: Optional. kwargs to format the text
        """
        try:
            if not self.text:
                self.text = kwargs.pop("text")
        except KeyError:
            pass

        if not self.kwargs:
            if self.text:
                self._check_kwargs(kwargs)
            self.kwargs = kwargs

    def _check_kwargs(self, kwargs):
        if not kwargs:
            return
        try:
            self.text.format(**kwargs)
        except KeyError:
            raise KeyError(f"Wrong attributes for the given text. Attributes: {kwargs}")

    def get_text(self):
        raise NotImplementedError


class MarkupMixin(BaseMarkup):
    """A mixin that can be used to render a Markup"""

    text = None
    kwargs = None

    def get_text(self):
        if self.kwargs:
            self._check_kwargs(self.kwargs)
            return self.text.format(**self.kwargs)
        else:
            return self.text

    def __str__(self):
        return self.text

    def __repr__(self):
        return f"Markup(text={self.text})"


class TextMarkup(MarkupMixin):
    """
    Class only for text markup
    """

    def __init__(self, **kwargs):
        super(TextMarkup, self).__init__(**kwargs)


class KeyboardMarkup(TextMarkup):
    keyboard = None

    def __init__(self, **kwargs):
        """
        :keyword text: Text to send
        :keyword keyboard: Array of buttons
        :keyword kwargs: Optional. kwargs to format the text
        """
        super(KeyboardMarkup, self).__init__(**kwargs)
        try:
            self.keyboard = kwargs.pop("keyboard")
        except KeyError:  # keyboard is not required
            raise AttributeError("You must specify a keyboard")
