from aws_cdk import (
    # Duration,
    Stack,
    core,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2
    # aws_sqs as sqs,
)

from constructs import Construct

class Cdk1AlbAssnmtStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        
        # VPC
        vpc = ec2.Vpc(
            self, "EngineeringVpc",
            cidr="10.0.0.0/18",
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="PublicSubnet1",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="PublicSubnet2",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                )
            ]
        )

        # Security Groups
        webserver_sg = ec2.SecurityGroup(
            self, "WebserverSG",
            vpc=vpc,
            description="Security group for web servers",
            allow_all_outbound=True
        )
        webserver_sg.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(80),
            "Allow HTTP traffic"
        )

        webserver_sg.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(22),
            "Allow SSH traffic"
        )

        # Instances
        ami = ec2.MachineImage.latest_amazon_linux()

        for i in range(1, 3):
            ec2.Instance(
                self, f"WebServer{i}",
                instance_type=ec2.InstanceType("t2.micro"),
                machine_image=ami,
                vpc=vpc,
                security_group=webserver_sg,
                vpc_subnets=ec2.SubnetSelection(
                    subnet_type=ec2.SubnetType.PUBLIC
                ),
                key_name="YourKeyPair"
            )

        # Load Balancer
        lb = elbv2.ApplicationLoadBalancer(
            self, "EngineeringLB",
            vpc=vpc,
            internet_facing=True
        )

        listener = lb.add_listener(
            "Listener",
            port=80,
            open=True
        )

        listener.add_targets(
            "WebServerTarget",
            port=80,
            targets=[
                elbv2.InstanceTarget(
                    instance_id=instance.instance_id,
                    port=80
                ) for instance in ec2.Instance.all_instances(self)
            ]
        )

        core.CfnOutput(
            self, "LoadBalancerDNS",
            value=lb.load_balancer_dns_name
        )

        # example resource
        # queue = sqs.Queue(
        #     self, "Cdk1AlbAssnmtQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
