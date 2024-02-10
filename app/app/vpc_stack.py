from aws_cdk import NestedStack, aws_ec2 as ec2
from constructs import Construct


class VPCStack(NestedStack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc(
            self,
            "VPC",
            availability_zones=["us-east-1a", "us-east-1b", "us-east-1c"],
            restrict_default_security_group=True,
            cidr="10.0.0.0/16",
            # Will create 2 groups in 3 AZs (6 subnets).
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PUBLIC, name="Public", cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    name="Private",
                    cidr_mask=24,
                ),
            ],
            nat_gateways=1,
        )

        self.frontSG = ec2.SecurityGroup(
            self,
            "FrontendSecurityGroup",
            vpc=self.vpc,
            description="Allow web access",
            allow_all_outbound=True,
            disable_inline_rules=True,
        )
        # This will add the rule as an external cloud formation construct
        self.frontSG.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "allow HTTP access from the world"
        )
        self.frontSG.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(433), "allow HTTPS access from the world"
        )
        self.frontSG.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "allow SSH access from the world"
        )

        self.backSG = ec2.SecurityGroup(
            self,
            "BackendSecurityGroup",
            vpc=self.vpc,
            description="Allow web access",
            allow_all_outbound=True,
            disable_inline_rules=True,
        )
        self.frontSG.connections.allow_from(
            self.frontSG, ec2.Port.tcp(80), "allow HTTP access"
        )
        self.frontSG.connections.allow_from(
            self.frontSG, ec2.Port.tcp(443), "allow HTTPS access"
        )
