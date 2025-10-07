import secrets # for generating random characters
import string # for generating characters
import zxcvbn # for checking password strength
from enum import Enum

ACCEPTABLE_STRENGTH = 3
MAX_STRENGTH_CHECK_ATTEMPTS = 20

class ValidationError(Enum):
    INVALID_FORMAT = "Invalid format: must be a number"
    TOO_SHORT = "Too short: minimum length is 4 characters"
    TOO_LONG = "Too long: maximum length is 256 characters"

class PasswordGenerator:    
    def __init__(self, length: int = 12):
        self.length = length
        self.characters = string.ascii_letters + string.digits + string.punctuation
        self.uppercase = string.ascii_uppercase
        self.lowercase = string.ascii_lowercase
        self.digits = string.digits
        self.symbols = string.punctuation
    
    def _is_password_strong(self, password: str) -> bool:
        result = zxcvbn.zxcvbn(password)
        strength = result['score']
        return strength >= ACCEPTABLE_STRENGTH

    def generate_password(self, strength_check: bool) -> str:
        def_password_chars = [
            secrets.choice(self.uppercase),
            secrets.choice(self.lowercase),
            secrets.choice(self.digits),
            secrets.choice(self.symbols),
        ]

        counter = 0
        is_password_strong = False
        if strength_check:
            while not is_password_strong and counter < MAX_STRENGTH_CHECK_ATTEMPTS: # MAX_STRENGTH_CHECK_ATTEMPTS attempts to generate a strong password
                password_chars = def_password_chars.copy()
                password_chars += [secrets.choice(self.characters) for _ in range(self.length - len(def_password_chars))]
                password = ''.join(password_chars)
                is_password_strong = self._is_password_strong(password)
                counter += 1
        else:
            password_chars = def_password_chars.copy()
            password_chars += [secrets.choice(self.characters) for _ in range(self.length - len(def_password_chars))]
            password = ''.join(password_chars)
            is_password_strong = True
        
        return password

class PasswordService:    
    def __init__(self, generator: PasswordGenerator):
        self.generator = generator
    
    def validate_input(self, length_str: str) -> tuple[bool, int | None, ValidationError | None]:
        try:
            length = int(length_str)
            if length < 4:
                return False, None, ValidationError.TOO_SHORT
            if length > 256:
                return False, None, ValidationError.TOO_LONG
            return True, length, None
        except ValueError:
            return False, None, ValidationError.INVALID_FORMAT

    def generate_password_with_length(self, length_str: str) -> tuple[bool, str]:
        success, length, error = self.validate_input(length_str)
        if not success:
            return False, error.value

        strength_check = True
        self.length = length
        if length > 72:
            print("\n\t WARNING: Password length must not exceed 72 characters for security checks")
            print("\t - pattern matching and frequency checks are disabled\n")
            strength_check = False
        
        password = self.generator.generate_password(strength_check)
        return True, password

class PasswordGeneratorUI:
    def __init__(self, service: PasswordService):
        self.service = service
    
    def run(self) -> None:
        print("Welcome to the Password Generator!")
        
        length_input = input("Enter the length of the password: ")     
        success, result = self.service.generate_password_with_length(length_input)
        
        if success:
            print(f"Generated password: {result}")
        else:
            print(f"Error: {result}")


def main() -> None:
    generator = PasswordGenerator()
    service = PasswordService(generator)
    ui = PasswordGeneratorUI(service)
    ui.run()

if __name__ == "__main__":
    main()
