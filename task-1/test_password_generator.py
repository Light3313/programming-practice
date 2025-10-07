import unittest
import string
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import importlib.util
spec = importlib.util.spec_from_file_location("password_generator", "password-generator.py")
password_generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(password_generator)

PasswordGenerator = password_generator.PasswordGenerator
PasswordService = password_generator.PasswordService
PasswordGeneratorUI = password_generator.PasswordGeneratorUI


class TestPasswordGenerator(unittest.TestCase):
    
    def setUp(self):
        self.generator = PasswordGenerator(length=12)
    
    def test_init_default_length(self):
        """Тест ініціалізації з довжиною за замовчуванням."""
        gen = PasswordGenerator()
        self.assertEqual(gen.length, 12)
    
    def test_init_custom_length(self):
        """Тест ініціалізації з кастомною довжиною."""
        gen = PasswordGenerator(length=16)
        self.assertEqual(gen.length, 16)
    
    def test_characters_contain_all_types(self):
        """Тест що characters містить всі типи символів."""
        chars = self.generator.characters
        self.assertTrue(any(c.isupper() for c in chars))
        self.assertTrue(any(c.islower() for c in chars))
        self.assertTrue(any(c.isdigit() for c in chars))
        self.assertTrue(any(c in string.punctuation for c in chars))
    
    def test_generate_password_length(self):
        """Тест що згенерований пароль має правильну довжину."""
        password = self.generator.generate_password(strength_check=False)
        self.assertEqual(len(password), 12)
    
    def test_generate_password_contains_all_types(self):
        """Тест що пароль містить всі типи символів."""
        password = self.generator.generate_password(strength_check=False)
        
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_punct = any(c in string.punctuation for c in password)
        
        self.assertTrue(has_upper, "Password should contain uppercase letter")
        self.assertTrue(has_lower, "Password should contain lowercase letter")
        self.assertTrue(has_digit, "Password should contain digit")
        self.assertTrue(has_punct, "Password should contain punctuation")
    
    
    def test_generate_password_different_each_time(self):
        """Тест що паролі різні при кожній генерації."""
        password1 = self.generator.generate_password(strength_check=False)
        password2 = self.generator.generate_password(strength_check=False)
        self.assertNotEqual(password1, password2)


class TestPasswordService(unittest.TestCase):
    
    def setUp(self):
        self.generator = PasswordGenerator(length=12)
        self.service = PasswordService(self.generator)
    
    def test_generate_password_with_valid_length(self):
        """Тест генерації пароля з валідною довжиною."""
        success, result = self.service.generate_password_with_length("16")
        self.assertTrue(success)
        self.assertEqual(len(result), 16)
    
    def test_generate_password_with_invalid_length(self):
        """Тест генерації пароля з невалідною довжиною."""
        success, result = self.service.generate_password_with_length("300")
        self.assertFalse(success)
        self.assertIn("Too long", result)
    
    def test_generate_password_with_non_numeric_input(self):
        """Тест генерації пароля з нечисловим вводом."""
        success, result = self.service.generate_password_with_length("abc")
        self.assertFalse(success)
        self.assertIn("Invalid format", result)
    
    def test_generate_password_with_too_short_length(self):
        """Тест генерації пароля з занадто короткою довжиною."""
        success, result = self.service.generate_password_with_length("2")
        self.assertFalse(success)
        self.assertIn("Too short", result)


class TestPasswordGeneratorUI(unittest.TestCase):
    
    def setUp(self):
        self.generator = PasswordGenerator(length=12)
        self.service = PasswordService(self.generator)
        self.ui = PasswordGeneratorUI(self.service)
    
    def test_ui_initialization(self):
        """Тест ініціалізації UI."""
        self.assertEqual(self.ui.service, self.service)


if __name__ == '__main__':
    unittest.main()
