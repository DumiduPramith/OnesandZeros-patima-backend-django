class Feedback:
    def __init__(self, text, rating, image_id, **kwargs):
        self._text = text
        self._rating = rating
        self._image_id = image_id
        self._kwargs = kwargs

    @property
    def text(self):
        return self._text

    @property
    def rating(self):
        return self._rating

    @property
    def image_id(self):
        return self._image_id

    @property
    def kwargs(self):
        return self._kwargs

    def is_valid(self):
        if not (len(self._text) < 400 and isinstance(self._text, str)):
            return False
        elif not (0 <= self._rating <= 5):
            return False
        elif not isinstance(self._image_id, int):
            return False
        return True
