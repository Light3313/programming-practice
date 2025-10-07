#!/usr/bin/env python3
"""
Простий тест для wordlist_password_check.py
"""

import unittest
import tempfile
import os
import csv
import wordlist_password_check


class TestWordlistPasswordCheck(unittest.TestCase):
    
    def setUp(self):
        """Підготовка тестових даних перед кожним тестом."""
        # Створюємо тимчасову папку
        self.temp_dir = tempfile.mkdtemp()
        
        # Створюємо тестовий CSV файл
        self.test_csv_path = os.path.join(self.temp_dir, "test_users.csv")
        with open(self.test_csv_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['username', 'password'])  # заголовок
            writer.writerow(['alice', '123456'])
            writer.writerow(['bob', 'password'])
            writer.writerow(['carol', 'strongpass123'])
        
        # Створюємо тестовий wordlist файл
        self.test_wordlist_path = os.path.join(self.temp_dir, "test_wordlist.txt")
        with open(self.test_wordlist_path, 'w') as file:
            file.write("123456\n")
            file.write("password\n")
            file.write("admin\n")
    
    def tearDown(self):
        """Очищення після кожного тесту."""
        import shutil
        shutil.rmtree(self.temp_dir)
        
        # Видаляємо report.txt якщо існує
        if os.path.exists('report.txt'):
            os.remove('report.txt')
    
    def test_read_users_csv(self):
        """Тест читання користувачів з CSV файлу."""
        users = wordlist_password_check.read_users_csv(self.test_csv_path)
        
        # Має пропустити заголовок і повернути 3 користувачів
        self.assertEqual(len(users), 3)
        self.assertEqual(users[0], ['alice', '123456'])
        self.assertEqual(users[1], ['bob', 'password'])
        self.assertEqual(users[2], ['carol', 'strongpass123'])
    
    def test_load_wordlist(self):
        """Тест завантаження wordlist з файлу."""
        wordlist = wordlist_password_check.load_wordlist(self.test_wordlist_path)
        
        # Має повернути set
        self.assertIsInstance(wordlist, set)
        
        # Має містити всі паролі в нижньому регістрі
        expected_passwords = {'123456', 'password', 'admin'}
        self.assertEqual(wordlist, expected_passwords)
    
    def test_check_passwords_against_wordlist(self):
        """Тест перевірки паролів проти wordlist."""
        users = [
            ['alice', '123456'],
            ['bob', 'password'],
            ['carol', 'strongpass123']
        ]
        wordlist = {'123456', 'password', 'admin'}
        
        vulnerable_users = wordlist_password_check.check_passwords_against_wordlist(users, wordlist)
        
        # Має знайти 2 вразливих користувачів
        self.assertEqual(len(vulnerable_users), 2)
        self.assertIn(['alice', '123456'], vulnerable_users)
        self.assertIn(['bob', 'password'], vulnerable_users)
        self.assertNotIn(['carol', 'strongpass123'], vulnerable_users)
    
    def test_check_passwords_case_insensitive(self):
        """Тест що перевірка паролів не залежить від регістру."""
        users = [
            ['alice', 'PASSWORD'],
            ['bob', 'Admin']
        ]
        wordlist = {'password', 'admin'}
        
        vulnerable_users = wordlist_password_check.check_passwords_against_wordlist(users, wordlist)
        
        # Має знайти обох користувачів незважаючи на регістр
        self.assertEqual(len(vulnerable_users), 2)
        self.assertIn(['alice', 'PASSWORD'], vulnerable_users)
        self.assertIn(['bob', 'Admin'], vulnerable_users)
    
    def test_generate_report(self):
        """Тест створення звіту."""
        vulnerable_users = [
            ['alice', '123456'],
            ['bob', 'password']
        ]
        
        wordlist_password_check.generate_report(vulnerable_users)
        
        # Перевіряємо що report.txt створений
        self.assertTrue(os.path.exists('report.txt'))
        
        # Перевіряємо вміст
        with open('report.txt', 'r') as file:
            content = file.read()
        
        expected_content = "alice: 123456\nbob: password\n"
        self.assertEqual(content, expected_content)
    
    def test_full_workflow(self):
        """Тест повного циклу роботи програми."""
        # Читаємо користувачів
        users = wordlist_password_check.read_users_csv(self.test_csv_path)
        self.assertEqual(len(users), 3)
        
        # Завантажуємо wordlist
        wordlist = wordlist_password_check.load_wordlist(self.test_wordlist_path)
        self.assertIsInstance(wordlist, set)
        
        # Перевіряємо паролі
        vulnerable_users = wordlist_password_check.check_passwords_against_wordlist(users, wordlist)
        self.assertEqual(len(vulnerable_users), 2)
        
        # Створюємо звіт
        wordlist_password_check.generate_report(vulnerable_users)
        self.assertTrue(os.path.exists('report.txt'))
        
        # Перевіряємо вміст звіту
        with open('report.txt', 'r') as file:
            content = file.read()
        
        self.assertIn('alice: 123456', content)
        self.assertIn('bob: password', content)
        self.assertNotIn('carol: strongpass123', content)


if __name__ == '__main__':
    unittest.main()
