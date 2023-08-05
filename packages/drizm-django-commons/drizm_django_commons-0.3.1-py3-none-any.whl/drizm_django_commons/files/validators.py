from rest_framework import serializers


class MaxFileSizeValidator:
    def __init__(self, max_size_bytes: int) -> None:
        self.max_size = max_size_bytes

    def __call__(self, value) -> None:
        if value.size > self.max_size:
            message = f"Supplied file may not be larger than {self.max_size} bytes."
            raise serializers.ValidationError(message)


__all__ = ["MaxFileSizeValidator"]
