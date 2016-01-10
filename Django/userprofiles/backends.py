from django.contrib.auth.models import User


class EmailBackend(object):
	def authenticate(self, username=None, password=None):
		try:
			user = User.objects.get(username=username)
			if user.check_password(password):
				return user

		except User.DoesNotExist:
			try:
				user = User.objects.get(email=username)
				if user.check_password(password):
					return user
			except User.DoesNotExist:
				return None

	def get_user(self, user_id):
		try:
			return User.objects.get(id=user_id)
		except User.DoesNotExist:
			return None


