from passlib.context import CryptContext

pwd_context=CryptContext(schemes=["bcrypt"], deprecated='auto')

class hasher():
    @staticmethod
    def verify_pass(plain_pass, hashed_pass):
        return pwd_context.verify(plain_pass, hashed_pass)
    
    @staticmethod
    def get_pass_hashed(password):
        return pwd_context.hash(password)
    
   
