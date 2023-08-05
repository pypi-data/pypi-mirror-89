from rest_framework import serializers


class ImageValidator:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class MaxImageDimensionsValidator(ImageValidator):
    def __call__(self, value) -> None:
        img = value.image
        if img.width > self.x or img.height > self.y:
            message = f"Image exceeds maximum dimensions of {self.x}x{self.y}."
            raise serializers.ValidationError(message)


class MinImageDimensionsValidator(ImageValidator):
    def __call__(self, value) -> None:
        img = value.image
        if img.width < self.x or img.height < self.y:
            message = f"Image subceeds maximum dimensions of {self.x}x{self.y}."
            raise serializers.ValidationError(message)


class ExactImageDimensionsValidator(ImageValidator):
    def __call__(self, value) -> None:
        img = value.image
        if not img.width == self.x or not img.height == self.y:
            message = f"Image does not match required dimensions of {self.x}x{self.y}."
            raise serializers.ValidationError(message)


__all__ = [
    "MaxImageDimensionsValidator",
    "MinImageDimensionsValidator",
    "ExactImageDimensionsValidator"
]
