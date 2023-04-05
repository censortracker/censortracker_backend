from rest_framework import authentication


class TokenAuthentication(authentication.TokenAuthentication):
    keyword = "Bearer"
