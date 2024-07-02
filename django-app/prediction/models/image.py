class Image:
    def __init__(self, image_id=None, input_image_path=None, output_image_path=None, uploader_id=None, created_at=None):
        self._image_id = image_id
        self._input_image_path = input_image_path
        self._output_image_path = output_image_path
        self._uploader_id = uploader_id
        self._created_at = created_at

    @property
    def image_id(self):
        return self._image_id

    @property
    def input_image_path(self):
        return self._input_image_path

    @property
    def output_image_path(self):
        return self._output_image_path

    @property
    def uploader_id(self):
        return self._uploader_id

    @property
    def created_at(self):
        return self._created_at
