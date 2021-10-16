from aws_cdk import aws_apigateway
from aws_cdk import aws_lambda
from aws_cdk import aws_elasticsearch
from aws_cdk import aws_ec2
from aws_cdk.aws_lambda_python import PythonFunction
from aws_cdk import core as cdk


from aws_solutions_constructs import aws_apigateway_lambda

ELASTICSEARCH = 'https://vpc-rna-expression-dro56qntagtgmls6suff2m7nza.us-west-2.es.amazonaws.com'

FUNCTION_REGISTRY = {}

RESOURCES = {
    ('projects', 'projects'): {
        ('{project_id}', 'project_id'): dict(),
        ('filters', 'project_filters'): dict(),
    },
    ('studies', 'studies'): {
        ('{studies_id}', 'studies_id'): dict(),
        ('filters', 'study_filters'): dict(),
    },
    ('expressions', 'expression_ids'): {
        ('formats', 'expressions_formats'): dict(),
        ('units', 'expressions_units'): dict(),
        ('ticket', 'expressions_ticket'): dict(),
        ('{expression_id}', None): {
            ('ticket', 'expressions_id_ticket'): dict(),
            ('bytes', 'expressions_id_bytes'): dict(),
        },
        ('bytes', 'expressions_bytes'): dict(),
        ('filters', 'expressions_filters'): dict(),
    },
    ('service-info', 'service_info'): dict(),
}

VPC_LAMBDAS = [
    'expressions_bytes',
]


def make_lambda_in_vpc(context, name, entry='serverless_rnaget/lambdas/', index='rnaget.py'):
    return PythonFunction(
        context,
        name,
        entry=entry,
        index=index,
        handler=name,
        runtime=aws_lambda.Runtime.PYTHON_3_8,
        vpc=context.internal_network.vpc,
        security_group=context.internal_network.security_group,
        allow_public_subnet=True,
    )


def make_lambda(context, name, entry='serverless_rnaget/lambdas/', index='rnaget.py'):
    return PythonFunction(
        context,
        name,
        entry=entry,
        index=index,
        handler=name,
        runtime=aws_lambda.Runtime.PYTHON_3_8,
    )


def make_lambda_factory(context, name):
    if name in VPC_LAMBDAS:
        return make_lambda_in_vpc(context, name)
    return make_lambda(context,name)


def make_api_gateway_to_lambda(context, name, lambda_):
    return aws_apigateway_lambda.ApiGatewayToLambda(
        context,
        name,
        existing_lambda_obj=lambda_,
        api_gateway_props=aws_apigateway.RestApiProps(
            default_method_options=aws_apigateway.MethodOptions(
                authorization_type=aws_apigateway.AuthorizationType.NONE,
            )
        )
    )


def make_handler(context, name):
    lambda_ = make_lambda_factory(context, f'{name}')
    FUNCTION_REGISTRY[name] = lambda_
    return aws_apigateway.LambdaIntegration(
        lambda_
    )


def add_resources_and_handlers(context, resources, root, action='GET'):
    for (parent_resource, parent_handler), children_resources in resources.items():
        parent = root.add_resource(parent_resource)
        if parent_handler:
            handler = make_handler(context, parent_handler)
            parent.add_method(action, handler)
        add_resources_and_handlers(context, children_resources, parent, action)
    return root


class VPCSecurity(cdk.Construct):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.vpc = aws_ec2.Vpc.from_lookup(self, 'VPC', vpc_id='vpc-ea3b6581')
        self.security_group = aws_ec2.SecurityGroup.from_security_group_id(
            self,
            "SG",
            "sg-022ea667",
            mutable=False
        )


class API(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.internal_network = VPCSecurity(self, 'VPCSecurity')
        self.default_lambda = make_lambda(
            self,
            'default',
        )
        self.gateway_to_lambda = make_api_gateway_to_lambda(
            self,
            'RNAGetAPI',
            self.default_lambda,
        )
        self.gateway = self.gateway_to_lambda.api_gateway
        self.resources = add_resources_and_handlers(
            self,
            RESOURCES,
            self.gateway.root
        )
        self.domain = aws_elasticsearch.Domain.from_domain_endpoint(
            self,
            "RNAGetExpressions",
            ELASTICSEARCH
        )
