from argon2 import PasswordHasher
from argon2.exceptions import VerificationError,VerifyMismatchError

hasher = PasswordHasher()

def hash_password(password : str) -> str :
    return hasher.hash(password)

def verify_password(hashed_password : str,raw_password : str) -> int :
    try : 
        hasher.verify(hashed_password,raw_password)
        print("Password Matched !! ✅")
        return 1
    except VerifyMismatchError:
        print('Invalid password !! ❌')
        return -1
    except VerificationError :
        print('Corrupted password !! 🚨')
        return -1