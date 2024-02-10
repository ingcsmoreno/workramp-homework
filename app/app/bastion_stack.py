from aws_cdk import NestedStack, aws_ec2 as ec2
from constructs import Construct


class BastionStack(NestedStack):
    def __init__(self, scope: Construct, construct_id: str, vpc, sg, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # bastion KeyPair for remote SSH Access
        self.key_pair = ec2.KeyPair(
            self,
            "KeyPair",
            key_pair_name="BastionKey-{}".format(vpc.vpc_id),
            type=ec2.KeyPairType.RSA,
        )

        # Bastion EC2 Server
        self.bastion = ec2.BastionHostLinux(
            self,
            "bastionServer",
            vpc=vpc,
            subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            security_group=sg,
            instance_type=ec2.InstanceType(instance_type_identifier="t2.micro"),
        )

        # Assign the new KeyPair to the EC2 Instance
        self.bastion.instance.instance.add_property_override(
            "KeyName", self.key_pair.key_pair_name
        )
