from aws_cdk import CfnOutput, Stack, aws_ec2 as ec2
from constructs import Construct

import boto3


class BastionStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bastionSG = ec2.SecurityGroup(
            self,
            "BastionSecurityGroup",
            vpc=vpc,
            description="Allow SSH access",
            allow_all_outbound=True,
            disable_inline_rules=True,
        )
        bastionSG.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "allow SSH access from the world"
        )

        key_name = "BastionKey-{}".format(vpc.vpc_id)
        try:
            ec2_resource = boto3.resource("ec2")
            ec2_resource.KeyPair(key_name).load()
        except:  # noqa: E722
            ec2_client = boto3.client("ec2")
            print(ec2_client.create_key_pair(KeyName=key_name)["KeyMaterial"])

        self.bastion = ec2.BastionHostLinux(
            self,
            "bastionServer",
            vpc=vpc,
            subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            security_group=bastionSG,
            instance_type=ec2.InstanceType(instance_type_identifier="t2.micro"),
        )

        self.bastion.instance.instance.add_property_override("KeyName", key_name)

        CfnOutput(self, "BastionPublicIP", value=self.bastion.instance_public_ip)
