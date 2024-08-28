from .s3 import BucketCompliant


# Create the custom namespace structure in a compact way
class Compliant:
    class s3:
        Bucket = BucketCompliant


# Define the public API of your module
__all__ = ["Compliant"]
