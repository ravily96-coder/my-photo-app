from PIL import Image
import os
from io import BytesIO

class AIModels:

    def __init__(self):
        self.provider = "demo"

    def set_provider(self, provider):
        self.provider = provider

    def enhance(self, image):
        if self.provider == "demo":
            return image

        elif self.provider == "replicate":
            return self.replicate_enhance(image)

    def rejuvenate(self, image):
        if self.provider == "demo":
            return image

        elif self.provider == "replicate":
            return self.replicate_rejuvenate(image)

    def restore(self, image):
        if self.provider == "demo":
            return image

        elif self.provider == "replicate":
            return self.replicate_restore(image)

    def colors(self, image):
        return image

    def sharpen(self, image):
        return image

    def denoise(self, image):
        return image

    # ---------------------------------------
    # REPLICATE
    # ---------------------------------------

    def replicate_enhance(self, image):
        raise NotImplementedError("Replicate еще не подключен")

    def replicate_rejuvenate(self, image):
        raise NotImplementedError("Replicate еще не подключен")

    def replicate_restore(self, image):
        raise NotImplementedError("Replicate еще не подключен")


ai = AIModels()
