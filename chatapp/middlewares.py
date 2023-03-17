from rest_framework.authtoken.models import Token
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser


@database_sync_to_async
def returnUser(token_string):
	try:
		user = Token.objects.get(key=token_string).user
	except:
		user = AnonymousUser()
	return user


class TokenAuthMiddleWare:
	def __init__(self, app):
		self.app = app

	async def __call__(self, scope, receive, send):
		query_string = scope["query_string"]
		headers = scope['headers']
		query_params = query_string.decode()
		query_dict = parse_qs(query_params)
		token = query_dict["token"][0]
		user = await returnUser(token)
		scope["user"] = user
		return await self.app(scope, receive, send)




#

from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

@database_sync_to_async
def get_user(token_key):
    try:
        token = Token.objects.get(key=token_key)
        return token.user
    except Token.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware2(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        try:
            token_key = (dict((x.split('=') for x in scope['query_string'].decode().split("&")))).get('token', None)
        except ValueError:
            token_key = None
        scope['user'] = AnonymousUser() if token_key is None else await get_user(token_key)
        return await super().__call__(scope, receive, send)



