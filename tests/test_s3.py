from aws_cdk import Stack, aws_s3 as s3, Duration, aws_iam as iam, App
import aws_cdk.assertions as assertions
from constructs import Construct
from compliant_cdk_lib.s3 import BucketCompliant
import pytest


def test_validate_props():
    # Test that the function raises an error if a prohibited key is in props
    props = s3.BucketProps(versioned=False)
    with pytest.raises(ValueError) as e:
        BucketCompliant.validate_props(props)
    assert (
        str(e.value)
        == "The property 'versioned' cannot be overridden in CompliantS3Bucket."
    )

    # Test that the function raises an error if bucket_name is not specified
    props = s3.BucketProps()
    with pytest.raises(ValueError) as e:
        BucketCompliant.validate_props(props)
    assert str(e.value) == "Must specify a bucket name"

    # Test that the function raises an error if the bucket_name is invalid
    props = s3.BucketProps(bucket_name="invalid_bucket_name")
    with pytest.raises(ValueError) as e:
        BucketCompliant.validate_props(props)
    assert str(e.value) == "Invalid bucket name"

    # Test that the function does not raise an error if all conditions are met
    props = s3.BucketProps(bucket_name="dino_bucket")
    BucketCompliant.validate_props(props)


def test_s3_bucket_created():
    app = App()

    class MyStack(Stack):
        def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
            super().__init__(scope, construct_id, **kwargs)
            bucket_props = s3.BucketProps(
                bucket_name="dino-my-bucket",
                lifecycle_rules=[
                    s3.LifecycleRule(id="rule1", expiration=Duration.days(30))
                ],
            )
            bucket = BucketCompliant(self, "CompliantBucket", bucket_props)
            bucket.grant_read_write(iam.AccountRootPrincipal())

    stack = MyStack(app, "cdk-py")
    template = assertions.Template.from_stack(stack)

    # bucket_resources = template.find_resources("AWS::S3::Bucket")
    # # Assuming there is only one bucket resource
    # bucket_props = list(bucket_resources.values())[0]["Properties"]
    # assert "dino" in bucket_props.get("BucketName", ""), "Invalid bucket name - must have dino"

    # Test for Bucket Versioning
    template.has_resource_properties(
        "AWS::S3::Bucket", {"VersioningConfiguration": {"Status": "Enabled"}}
    )

    # Test for Bucket Encryption
    template.has_resource_properties(
        "AWS::S3::Bucket",
        {
            "BucketEncryption": {
                "ServerSideEncryptionConfiguration": [
                    {"ServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}
                ]
            }
        },
    )

    # Test for Block Public Access
    template.has_resource_properties(
        "AWS::S3::Bucket",
        {
            "PublicAccessBlockConfiguration": {
                "BlockPublicAcls": True,
                "IgnorePublicAcls": True,
                "BlockPublicPolicy": True,
                "RestrictPublicBuckets": True,
            }
        },
    )

    # Test for Removal Policy
    template.has_resource("AWS::S3::Bucket", {"DeletionPolicy": "Delete"})
