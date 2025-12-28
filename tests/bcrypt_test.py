from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

hashed = pwd_context.hash("Admin@1234")
print(hashed)

print(pwd_context.verify("Admin@1234", hashed))
