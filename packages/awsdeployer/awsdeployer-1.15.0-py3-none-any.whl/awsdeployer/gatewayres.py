from awsdeployer.__status_dict import code
from awsdeployer.status import Common, Standard, Extended


def success(body=None):
    if body is None:
        body = {}
    import json
    return json.dumps({
        'body': body
    })


def error(error_code, user_message=''):
    # check error code is known
    if isinstance(error_code, int) or isinstance(error_code, str):
        error_code = code(error_code)
        if not error_code:
            raise ValueError('Status code not found in AWSDeployer')

    if not (isinstance(error_code, Common) or isinstance(error_code, Standard) or isinstance(error_code, Extended)):
        raise ValueError('Non-enum error code provided')

    import json
    return json.dumps({
        'gatewayResponse': True,
        'status': 'error',
        'type': error_code.value[1],
        'userMessage': user_message
    })
