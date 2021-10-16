import json


DEFAULT_RESPONSE = {
    'statusCode': 200,
    'headers': {
        'Content-Type': 'application/json'
    },
    'body': json.dumps(
        {
            'message': 'success'
        }
    )
}


NOT_IMPLEMENTED_RESPONSE = {
    'statusCode': 501,
    'headers': {
        'Content-Type': 'application/json'
    },
    'body': json.dumps(
        {
            'message': 'The server does not support the action requested by the browser.'
        }
    )
}


SERVICE_INFO = {
    'id': 'org.ga4gh.encodeproject',
    'name': 'ENCODE RNAget',
    'type': {
        'group': 'org.encodeproject',
        'artifact': 'rnaget',
        'version': '1.2.0'
    },
    'description': 'This service implements the GA4GH RNAget API for ENCODE data',
    'organization': {
        'name': 'ENCODE',
        'url': 'https://www.encodeproject.org'
    },
    'contactUrl': 'mailto:encode-help@lists.stanford.edu',
    'version': '0.0.2',
    'supported': {
        'projects': True,
        'studies': True,
        'expressions': True,
        'continuous': False
    }
}


def default(event, context):
    return NOT_IMPLEMENTED_RESPONSE


def projects(event, context):
    return DEFAULT_RESPONSE


def project_id(event, context):
    return DEFAULT_RESPONSE


def project_filters(event, context):
    return DEFAULT_RESPONSE


def studies(event, context):
    return DEFAULT_RESPONSE


def studies_id(event, context):
    return DEFAULT_RESPONSE


def studies_filters(event, context):
    return DEFAULT_RESPONSE


def expression_ids(event, context):
    return DEFAULT_RESPONSE


def expressions_formats(event, context):
    return DEFAULT_RESPONSE


def expressions_units(event, context):
    return DEFAULT_RESPONSE


def expressions_ticket(event, context):
    return DEFAULT_RESPONSE


def expressions_id_ticket(event, context):
    return DEFAULT_RESPONSE


def expressions_bytes(event, context):
    return DEFAULT_RESPONSE


def expressions_id_bytes(event, context):
    return DEFAULT_RESPONSE


def expressions_filters(event, context):
    return DEFAULT_RESPONSE


def service_info(event, context):
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(SERVICE_INFO)
    }
