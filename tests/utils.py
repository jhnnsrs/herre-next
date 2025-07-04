import os
import urllib
import contextlib
from typing import Callable
from koil.qt import async_to_qt
from pytestqt.qtbot import QtBot

DIR_NAME = os.path.dirname(os.path.realpath(__file__))


def build_relative(path):
    return os.path.join(DIR_NAME, path)


async def fake_token_generator(*args, **kwargs):
    return {
        "access_token": "fake_access_token",
        "refresh_token": "fake_refresh_token",
    }


def construct_final_redirect_uri(auth_url, code):
    """
    Constructs the final redirect URI with the authorization code, using the redirect URI and state
    parameter from the provided authorization URL.

    Args:
    auth_url (str): The authorization URL that includes the redirect URI and possibly the state as parameters.
    code (str): The authorization code to be appended to the redirect URI.

    Returns:
    str: The complete redirect URI with the authorization code and, if present, the state parameter.
    """
    # Parse the query parameters from the authorization URL
    parsed_url = urllib.parse.urlparse(auth_url)
    query_params = urllib.parse.parse_qs(parsed_url.query)

    # Extract the redirect URI and state parameter
    redirect_uri_param = query_params.get("redirect_uri", [None])[0]
    state = query_params.get("state", [None])[0]

    if not redirect_uri_param:
        raise ValueError("Redirect URI not found in the authorization URL.")

    # Reconstruct the redirect URI with the code and state
    redirect_uri_components = list(urllib.parse.urlparse(redirect_uri_param))
    redirect_query_params = {"code": code}
    if state:
        redirect_query_params["state"] = state

    redirect_uri_components[4] = urllib.parse.urlencode(
        redirect_query_params
    )  # Set the query component
    return urllib.parse.urlunparse(redirect_uri_components)


async def redirect_result(starturl, *args, **kwargs):
    return construct_final_redirect_uri(starturl, "path")


async def loggin_wrapper_result(self, starturl, *args, **kwargs):
    return construct_final_redirect_uri(starturl, "path")
