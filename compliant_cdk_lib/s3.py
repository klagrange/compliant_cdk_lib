from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_s3 as s3,
    RemovalPolicy,
    Duration,
    aws_iam as iam,
    App,
)
from constructs import Construct


class BucketCompliant(Construct):
    @staticmethod
    def validate_props(props: s3.BucketProps) -> None:
        # List of properties that cannot be overridden
        prohibited_keys = [
            "versioned",
            "block_public_access",
            "encryption",
            "enforce_ssl",
        ]

        # Check if any prohibited keys are in props
        for key in prohibited_keys:
            if getattr(props, key, None) is not None:
                raise ValueError(
                    f"The property '{key}' cannot be overridden in CompliantS3Bucket."
                )

        # Ensure bucket_name follows naming conventions
        if not props.bucket_name:
            raise ValueError("Must specify a bucket name")

        if "dino" not in props.bucket_name:
            raise ValueError("Invalid bucket name")

    def __init__(self, scope: Construct, id: str, props: s3.BucketProps) -> None:
        super().__init__(scope, id)

        # Validate the properties
        BucketCompliant.validate_props(props)

        # Define the S3 bucket with security best practices
        self.bucket = s3.Bucket(
            self,
            "CompliantBucket",
            versioned=True,  # Enforce versioning
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,  # Block all public access
            encryption=s3.BucketEncryption.S3_MANAGED,  # Enable S3 managed encryption
            enforce_ssl=True,  # Enforce SSL
            removal_policy=RemovalPolicy.DESTROY,  # Change to RETAIN for production environments
            **props._values,  # Pass the validated properties
        )

    def grant_read_write(self, grantee: iam.IGrantable):
        """Grant read/write permissions to the bucket."""
        self.bucket.grant_read_write(grantee)

    def grant_read(self, grantee: iam.IGrantable):
        """Grant read-only permissions to the bucket."""
        self.bucket.grant_read(grantee)

    def grant_write(self, grantee: iam.IGrantable):
        """Grant write-only permissions to the bucket."""
        self.bucket.grant_write(grantee)


# class CdkPyStack(Stack):
#     def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
#         super().__init__(scope, construct_id, **kwargs)

#         bucket_props = s3.BucketProps(
#             bucket_name="dino-my-bucket",
#             lifecycle_rules=[
#                 s3.LifecycleRule(id="rule1", expiration=Duration.days(30))
#             ],
#         )
#         bucket = BucketCompliant(self, "CompliantBucketXXX", bucket_props)

#         bucket.grant_read_write(iam.AccountRootPrincipal())


# # Create an instance of the CDK app
# app = App()

# # Instantiate the stack
# stack = CdkPyStack(app, "CdkPyStack")

# # Synthesize the stack to CloudFormation template
# synth_output = app.synth()

# print(synth_output.get_stack_by_name(stack.stack_name).template)
