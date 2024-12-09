import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk1_alb_assnmt.cdk1_alb_assnmt_stack import Cdk1AlbAssnmtStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk1_alb_assnmt/cdk1_alb_assnmt_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Cdk1AlbAssnmtStack(app, "cdk1-alb-assnmt")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
