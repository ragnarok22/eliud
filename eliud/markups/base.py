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
            self._text = kwargs.pop("text")
        except KeyError:
            raise AttributeError("You must to provide a 'text'")

        self.__check_kwargs(kwargs)
        self._kwargs = kwargs

    @property
    def text(self) -> str:
        if self._kwargs:
            return self._text.format(**self._kwargs)
        else:
            return self._text

    @text.setter
    def text(self, value):
        self._text = value

    def __check_kwargs(self, kwargs):
        if not kwargs:
            return
        try:
            self._text.format(**kwargs)
        except KeyError:
            raise KeyError("Wrong attributes for the given text")

    def __str__(self):
        return self.text

    def __repr__(self):
        return f"Markup(text={self.text})"


class TextMarkup(BaseMarkup):
    """
    Class only for text markup
    """

    def __init__(self, text, **kwargs):
        kwargs["text"] = text
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
