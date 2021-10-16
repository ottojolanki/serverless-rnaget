from aws_cdk import aws_apigateway
from aws_cdk import aws_lambda
from aws_cdk.aws_lambda_python import PythonFunction
from aws_cdk import core as cdk


from aws_solutions_constructs import aws_apigateway_lambda



RESOURCES = {
    ('projects', 'projects'): {
        ('{project_id}', 'project_id'): dict(),
        ('filters', 'project_filters'): dict(),
    },
    ('studies', 'studies'): {
        ('{studies_id}', 'studies_id'): dict(),
        ('filters', 'study_filters'): dict(),
    },
    ('expressions', 'expressions_ids'): {
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


def make_lambda(context, name, entry='serverless_rnaget/lambdas/', index='rnaget.py'):
    return PythonFunction(
        context,
        name,
        entry=entry,
        index=index,
        handler=name,
        runtime=aws_lambda.Runtime.PYTHON_3_8,
    )


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
    lambda_ = make_lambda(context, f'{name}')
    return aws_apigateway.LambdaIntegration(
        lambda_
    )


def add_resources_and_handlers(context, resources, root, action='GET'):
    for (parent_resource, parent_handler), children_resources in resources.items():
        print(parent_resource, parent_handler, children_resources)
        parent = root.add_resource(parent_resource)
        if parent_handler:
            handler = make_handler(context, parent_handler)
            parent.add_method(action, handler)
        add_resources_and_handlers(context, children_resources, parent, action)
    return root


class API(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
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
