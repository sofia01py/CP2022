import sqlite3 as sql
import sqlite3
import json
#registration
def insert_varible_into_table(username, password):
    try:
        con = sqlite3.connect('data1.db')
        cur = con.cursor()
        print("Подключен к SQLite")

        sqlite_insert_with_param = """INSERT INTO users
                                      (Name, Password)
                                      VALUES (?,?);"""

        data_tuple = (username, password)
        cur.execute(sqlite_insert_with_param, data_tuple)
        con.commit()
        print("Переменные Python успешно вставлены в таблицу sqlitedb_developers")

        cur.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if con:
            con.close()
            print("Соединение с SQLite закрыто")

def compression(string):  # string is your input text
    dict = {}
    entry = ''
    index = 1
    for i in range(len(string)):
        entry += string[i]
        if entry not in dict:
            lst = [index]
            encoder = [dict[entry[0:len(entry) - 1]][0] if entry[0:len(entry) - 1] in dict else 0, entry[-1]]
            lst.append(encoder)
            dict[entry] = lst
            index += 1
            entry = ''
    ans = ''
    for x in dict:
        ans += f'({dict[x][1][0]},{dict[x][1][1]})'

    return ans  # 'dict' is a dictionary of each symbol with its encoded value, 'ans' is a final encoded version of input


# This function is used to convert your inputed string into an usable dictionary object
def parse(string):
    dict = {}
    index = 1
    incorrect = False
    for i in range(len(string)):
        if string[i] == '<':
            encoderIndex = ''
            encoderTail = ''
            comma = False
            i += 1
            while string[i] != '>':
                if string[i] == ',':
                    comma = True
                    i += 1
                    continue
                if comma:
                    encoderTail += string[i]
                    i += 1
                    continue
                encoderIndex += string[i]
                i += 1

            lst = [[int(encoderIndex), encoderTail], '']
            dict[index] = lst
            index += 1

    return dict


def decompression(string):  # Your input string should be in format <'index', 'entry'>,... . Ex: <0,A><0,B><2,C>
    error = False
    ans, entry = '', ''
    try:
        parse(string)
    except BaseException:
        error = True  # 'error' is true if your input string was not in the correct format.
        return error, ans, {}

    dict = parse(string)
    for x in dict:
        value = dict[x]
        entry += dict[value[0][0]][1] if value[0][0] != 0 else ''
        entry += value[0][1]

        value[1] = entry
        ans += entry
        entry = ''

    return ans


u_for_c = input('Name: ')
p_for_c = input('Password: ')
print('encoded stream:' + compression(u_for_c))
username = compression(u_for_c)
print('decoded stream:' + decompression(compression(u_for_c)))
print('encoded stream:' + compression(p_for_c))
password = compression(p_for_c)
print('decoded stream:' + decompression(compression(p_for_c)))


con = sql.connect("data1.db")
cur = con.cursor()
insert_varible_into_table(username, password)
statement = f"SELECT Name from users WHERE Name='{username}' AND Password = '{password}';"
cur.execute(statement)

if not cur.fetchone():  # An empty result evaluates to False.
    print("Login failed")
else:
    print("Welcome")