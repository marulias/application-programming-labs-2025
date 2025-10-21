import re


def read_data_file():

    try:
        with open('data.txt', 'r', encoding='utf-8') as file:
            return file.readlines()
    except FileNotFoundError:
        print("Ошибка: Файл 'data.txt' не найден в текущей папке")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None


def extract_email(text):

    email_pattern = r'[A-Za-z0-9._%+-]{1,64}@(gmail\.com|mail\.ru|yandex\.ru)'
    match = re.search(email_pattern, text)
    if match:
        return match.group().lower()
    return None


def parse_profiles(lines):

    profiles = []
    current_profile = {}

    for line in lines:
        line = line.strip()


        if not line:
            if current_profile:
                profiles.append(current_profile)
                current_profile = {}
            continue


        email = extract_email(line)
        if email:
            current_profile['email'] = email
            current_profile['raw_data'] = current_profile.get('raw_data', []) + [line]
        else:
            current_profile['raw_data'] = current_profile.get('raw_data', []) + [line]


    if current_profile:
        profiles.append(current_profile)

    return profiles


def find_duplicate_emails(profiles):

    email_count = {}
    duplicate_emails = set()


    for profile in profiles:
        if 'email' in profile:
            email = profile['email']
            email_count[email] = email_count.get(email, 0) + 1
            if email_count[email] > 1:
                duplicate_emails.add(email)


    duplicate_profiles = []
    for profile in profiles:
        if 'email' in profile and profile['email'] in duplicate_emails:
            duplicate_profiles.append(profile)

    return duplicate_profiles


def main():

    lines = read_data_file()
    if lines is None:
        return


    profiles = parse_profiles(lines)

    if not profiles:
        print("В файле не найдено анкет")
        return

    print(f"Всего найдено анкет: {len(profiles)}")

    duplicate_profiles = find_duplicate_emails(profiles)

    if duplicate_profiles:
        print("\nНайдены анкеты с дублирующимися email:")
        print("=" * 50)

        email_groups = {}
        for profile in duplicate_profiles:
            email = profile['email']
            if email not in email_groups:
                email_groups[email] = []
            email_groups[email].append(profile)

        for email, profiles_list in email_groups.items():
            print(f"\nEmail: {email}")
            print(f"Количество дубликатов: {len(profiles_list)}")
            print("-" * 30)

            for i, profile in enumerate(profiles_list, 1):
                print(f"Дубликат {i}:")
                for line in profile['raw_data']:
                    print(f"  {line}")
                print()
    else:
        print("\nДублирующихся email не найдено - все email уникальны!")

    emails_found = sum(1 for profile in profiles if 'email' in profile)
    print(f"\nСтатистика:")
    print(f"Всего анкет: {len(profiles)}")
    print(f"Анкет с email: {emails_found}")
    print(f"Анкет без email: {len(profiles) - emails_found}")


if __name__ == "__main__":
    main()