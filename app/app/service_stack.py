from aws_cdk import NestedStack, aws_ec2 as ec2
from constructs import Construct

with open("./user_data/service.sh") as f:
    user_data = f.read()


# This stack is for testing bastion can access the backend services on private networks.
class ServiceStack(NestedStack):
    def __init__(self, scope: Construct, construct_id: str, vpc, sg, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # EC2 Instances running an HTTP Server (provisioned on User Data)
        self.instance = ec2.Instance(
            self,
            "targetInstance",
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
            ),
            security_group=sg,
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO
            ),
            machine_image=ec2.AmazonLinuxImage(
                generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2
            ),
            user_data=ec2.UserData.custom(user_data),
        )
