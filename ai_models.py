from PIL import Image
import requests
import os
from io import BytesIO

HF_TOKEN = os.getenv("HF_TOKEN")


class AIProvider:

    def __init__(self):
        self.token = HF_TOKEN

    def enhance(self, image: Image.Image):
        raise NotImplementedError

    def restore(self, image: Image.Image):
        raise NotImplementedError

    def rejuvenate(self, image: Image.Image):
        raise NotImplementedError


class DemoProvider(AIProvider):

    def enhance(self, image):
        return image

    def restore(self, image):
        return image

    def rejuvenate(self, image):
        return image
