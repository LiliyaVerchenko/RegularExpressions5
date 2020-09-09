import re
from pprint import pprint
import csv
from operator import itemgetter

def get_correct_phone_number():      # приводим номера телефонов к единому формату с помощью регулрных выражений
    for person in contacts_list:
        if 'доб.' in person[-2]:
            phone_pattern_with_additional = r'(\+7|8)\s?(\(|\s)?(495)(\)|-)?\s?(\d{3})\-?(\d{2})\-?(\d{2})()(\,|\s)\(?(доб.)?\s(\d{4})\)?'
            regex = re.compile(phone_pattern_with_additional)
            correct_phone = regex.sub(r'+7(\3)\5-\6-\7 \10\11', str(person[-2])).replace('\n', '')
            person[-2] = correct_phone
        else:
            phone_pattern = r'(\+7|8)\s?\(?(495)(\)|-)?\s?(\d{3})\-?(\d{2})\-?(\d{2})'
            regex1 = re.compile(phone_pattern)
            correct_phone1 = regex1.sub(r'+7(\2)\4-\5-\6', str(person[-2])).replace('\n', '')
            person[-2] = correct_phone1
    return contacts_list

def merge_dibles():         # объединяем все дублирующиеся записи о человеке в одну и заменяем в списке 'contacts_list'
    for person_info in contacts_list:           # объединяем фио каждого контактного лица
        data = person_info[0:3]
        full_name_merge = re.compile(r'[^а-яёА-ЯЁ ]')
        result = full_name_merge.sub('', str(data))
        person_info[0:3] = [result.strip()]

    phone_book_dict = {}    # создаем словарь для сравнения дублированных строк и их объединения
    for contact in contacts_list:
        last_and_first_name = ' '.join(contact[0].split()[0:2])    # получаем фамилию и имя
        if last_and_first_name not in str(list(phone_book_dict.keys())):
            phone_book_dict[contact[0]] = contact[1:5]
        else:
            contacts_list.remove(contact)            # удаляем дубль из списка 'contacts_list'
            duplicate = {}                           # форматируем дубль из списка в словарь
            duplicate[contact[0]] = contact[1:5]
            list_keys = list(phone_book_dict.keys()) # получаем список ключей заполненного словаря
            for fio in list_keys:
                if last_and_first_name in fio:
                    for i in range(0, 4):            # объединяем данные из дублированных строк
                        if phone_book_dict[fio][i] < (list(duplicate.values())[0])[i]:
                            phone_book_dict[fio][i] = (list(duplicate.values())[0])[i]
                            # создаем новую строку с сборными данными из дублей и наполняем ее
                            contact_new = [fio]
                            contact_new.append(phone_book_dict[fio][0])
                            contact_new.append(phone_book_dict[fio][1])
                            contact_new.append(phone_book_dict[fio][2])
                            contact_new.append(phone_book_dict[fio][3])
                            # заменяем в списке 'contacts_list' дублированные строки на строку с обновленными данными
                            for full_name in contacts_list:
                                if full_name[0] == contact_new[0]:
                                    contacts_list.remove(full_name)
                                    contacts_list.append(contact_new)

    for rows in contacts_list:              # разбиваем фио на элементы и присваиваем им индексы, добавляя в список
        rows_str = str(rows[0]).split()
        rows.insert(0, rows_str[0])
        rows.insert(1, rows_str[1])
        rows[2] = rows_str[2]

    contacts_list.sort(key=itemgetter(0))   # сортируем список по алфовиту
    contacts_list.insert(0, title)          # добавляем заголовки
    return contacts_list

if __name__ == '__main__':
    # читаем телефонную книгу в формате CSV в список contacts_list
    with open("phonebook_raw.csv", encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
        title = contacts_list[0]
        del contacts_list[0]  # временно удаляем заголовки

    get_correct_phone_number()
    merge_dibles()

    # Записываем новый список в файл 'phonebook.csv'
    with open("phonebook.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(contacts_list)






















