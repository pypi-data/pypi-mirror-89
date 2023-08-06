import urllib

from . import http, dict, errors

noresponse = "Couldn't contact the API right now..."

def gif():
    try:
        return http.get("/gif/")["url"]
    except Exception as e:
        raise errors.NothingFound(noresponse)


def jav():
    try:
        return http.get("/jav/")["url"]
    except Exception as e:
        raise errors.NothingFound(noresponse)


def twitter():
    try:
        return http.get("/twitter/")["url"]
    except Exception as e:
        raise errors.NothingFound(noresponse)

def real():
    try:
        return http.get("/rb/")["url"]
    except Exception as e:
        raise errors.NothingFound(noresponse)

def fgo():
    try:
        return http.get("/r34/?tags=fate/grand_order")["url"]
    except Exception as e:
        raise errors.NothingFound(noresponse)

def furry():
    try:
        return http.get("/r34/?tags=furry")["url"]
    except Exception as e:
        raise errors.NothingFound(noresponse)
