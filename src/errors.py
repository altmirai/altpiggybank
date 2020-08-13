import requests
import click
import ecdsa
import json


def addr(error, context, config, **kwargs):
    # Connection Timeout Error
    if isinstance(error, requests.exceptions.ConnectTimeout):
        raise click.UsageError(
            'API connection timeout, please try again later', context)
    # API status_code NOT 200
    elif isinstance(error, AssertionError):
        raise click.UsageError(error.args[0], context)
    # VerifyingKey.from_pem failed due to bad file format
    elif isinstance(error, ecdsa.der.UnexpectedDER):
        raise click.UsageError(
            'Incorrect file, please provide a PEM formatted public key file', context)
    else:
        unkown_error(error, context)


def refresh(error, context, config, **kwargs):
    # Connection Timeout Error
    if isinstance(error, requests.exceptions.ConnectTimeout):
        raise click.UsageError(
            'API connection timeout, please try again later', context)
    # API status_code NOT 200, PEM not present in JSON file
    elif isinstance(error, AssertionError):
        raise click.UsageError(error.args[0], context)
    # File not JSON
    elif isinstance(error, json.decoder.JSONDecodeError):
        raise click.UsageError(
            'Incorrect file, please provide a JSON formatted addr file created by piggy addr', context)
    else:
        unkown_error(error, context)


def fee(error, context, config, **kwargs):
    # Connection Timeout Error
    if isinstance(error, requests.exceptions.ConnectTimeout):
        raise click.UsageError(
            'API connection timeout, please try again later', context)
    # API status_code NOT 200, PEM not present in JSON file
    elif isinstance(error, AssertionError):
        raise click.UsageError(error.args[0], context)
    # File not JSON
    elif isinstance(error, json.decoder.JSONDecodeError):
        raise click.UsageError(
            'Incorrect file, please provide a JSON formatted addr file created by piggy addr', context)
    else:
        unkown_error(error, context)


def tx(error, context, config, **kwargs):
    # Connection Timeout Error
    if isinstance(error, requests.exceptions.ConnectTimeout):
        raise click.UsageError(
            'API connection timeout, please try again later', context)
    # API status_code NOT 200
    elif isinstance(error, AssertionError):
        raise click.UsageError(error.args[0], context)
    else:
        unkown_error(error, context)


def signed(error, context, config, **kwargs):
    # Connection Timeout Error
    if isinstance(error, requests.exceptions.ConnectTimeout):
        raise click.UsageError(
            'API connection timeout, please try again later', context)
    # API status_code NOT 200
    elif isinstance(error, AssertionError):
        raise click.UsageError(error.args[0], context)
    else:
        unkown_error(error, context)


def unkown_error(error, context):
    file_name = error.__traceback__.tb_frame.f_code.co_filename
    line_num = error.__traceback__.tb_lineno
    raise click.UsageError(
        f'This is embarrassing, There was a {type(error).__name__}({error}) on line {line_num} in {file_name}', context)
