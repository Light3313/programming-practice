# Напишіть програму для пошуку слабких паролів у списку користувачів.
# Використовуйте базу поширених паролів (wordlist)

import csv

CSV_USERS_FILE_PATH = "users_table.csv"
WORDLIST_FILE_PATH = "word_lists/000webhost.txt"

def read_users_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Пропускаємо заголовок
        return list(reader)

def load_wordlist(wordlist_path):
    with open(wordlist_path, 'r') as file:
        return set(line.strip().lower() for line in file)
    
def check_passwords_against_wordlist(users, wordlist):
    vulnerable_users = []
    for user in users:
        if user[1].lower() in wordlist:
            vulnerable_users.append(user)
    return vulnerable_users

def generate_report(vulnerable_users):
    with open('report.txt', 'w') as file:
        for user in vulnerable_users:
            file.write(f"{user[0]}: {user[1]}\n")

def _print_report():
    print("\n======= Vulnerable users =======\n")
    with open('report.txt', 'r') as file:
        for line in file:
            print(line.strip())

def maybe_print_report(vulnerable_users):
    input_print_report = input("Print report? (y/n): ")
    if input_print_report == "y" and vulnerable_users:
        _print_report()
    elif input_print_report == "y" and not vulnerable_users:
        print("No vulnerable users found")
    else:
        print("Report can be found in report.txt")

def main():
    users = read_users_csv(CSV_USERS_FILE_PATH)
    wordlist = load_wordlist(WORDLIST_FILE_PATH)
    vulnerable_users = check_passwords_against_wordlist(users, wordlist)
    generate_report(vulnerable_users)
    maybe_print_report(vulnerable_users)

if __name__ == "__main__":
    main()