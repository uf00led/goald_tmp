from .manager import ManagerResult

from ..models import UserModel

from bcrypt import gensalt, hashpw


LENGTH_SALT = 29

class User(UserModel):
	@staticmethod
	def exists(login: str, password: str = None) -> ManagerResult:
		if password:
			if User.objects.filter(login=login, password=password).exists():
				return ManagerResult(True, "User exists")
			else:
				return ManagerResult(False, "User doesn't exist!")
		else:
			if User.objects.filter(login=login).exists():
				return ManagerResult(True, "User exists")
			else:
				return ManagerResult(False, "User doesn't exists!")

	@staticmethod
	def auth(login: str, password: str) -> ManagerResult:
		user = None
		try:
			user = User.objects.get(login=login)
		except User.DoesNotExist:
			return ManagerResult(False, "Incorrect login or password!")

		salt = user.password[:LENGTH_SALT]
		salted_hash = hashpw(bytes(password, "utf-8"), salt)

		if salted_hash != user.password:
			return ManagerResult(False, "Incorrect login or password!")

		return ManagerResult(True, "User authenticated successfully!")

	@staticmethod
	def create(login: str, password: str) -> ManagerResult:
		if User.objects.filter(login=login).exists():
			return ManagerResult(False, "User already exists!")

		salt = gensalt()
		salted_hash = hashpw(bytes(password, "utf-8"), salt)

		User.objects.create(login=login, password=salted_hash)

		return ManagerResult(True, "User created successfully!")

	@staticmethod
	def change(login: str, password: str) -> ManagerResult:
		user = User.objects.get(login=login)
		user.password = hashpw(bytes(password, "utf-8"), user.password[:LENGTH_SALT])
		user.save()

		return ManagerResult(True, "User's password changed successfully!")

	@staticmethod
	def delete(login: str) -> ManagerResult:
		User.objects.filter(login=login).delete()

		return ManagerResult(True, "User deleted successfully!")