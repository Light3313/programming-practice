import secrets # for generating random characters
import string # for generating characters
import zxcvbn # for checking password strength

ACCEPTABLE_STRENGTH = 3
MAX_STRENGTH_CHECK_ATTEMPTS = 20

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
    
    def set_length(self, length: int) -> None:
        if length < 4:
            raise ValueError("Password length must be at least 4 character")
        if length > 256:
            raise ValueError("Password length must not exceed 256 characters")
        self.length = length


class PasswordService:    
    def __init__(self, generator: PasswordGenerator):
        self.generator = generator
    
    def generate_password_with_length(self, length_str: str, strength_check: bool) -> tuple[bool, str]:
        try:
            length = int(length_str)
            self.generator.set_length(length)
            password = self.generator.generate_password(strength_check)
            return True, password
        except ValueError as e:
            return False, str(e)


class PasswordGeneratorUI:
    def __init__(self, service: PasswordService):
        self.service = service
    
    def run(self) -> None:
        print("Welcome to the Password Generator!")
        
        length_input = input("Enter the length of the password: ")
        strength_check = True
        if int(length_input) > 72:
            print("\n\t WARNING: Password length must not exceed 72 characters for security checks")
            print("\t - pattern matching and frequency checks are disabled\n")
            strength_check = False
        
        success, result = self.service.generate_password_with_length(length_input, strength_check)
        
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
