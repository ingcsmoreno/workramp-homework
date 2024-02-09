import aws_cdk as core
import aws_cdk.assertions as assertions

from app.vpc_stack import VPCStack

# example tests. To run these tests, uncomment this file along with the example
# resource in app/app_stack.py


def test_sqs_queue_created():
    app = core.App()
    stack = VPCStack(app, "VPC")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::EC2::VPC", {"CidrBlock": "10.0.0.0/16"})
