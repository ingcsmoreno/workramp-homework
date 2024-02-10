import aws_cdk as core
import aws_cdk.assertions as assertions

from app.root_stack import RootStack

# example tests. To run these tests, uncomment this file along with the example
# resource in app/app_stack.py


def test_stacks_created():
    app = core.App()
    stack = RootStack(app, "Root")

    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::CloudFormation::Stack", 3)
    template.resource_count_is("AWS::EC2::VPC", 0)
