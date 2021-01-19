import matplotlib.pyplot as plt
import time
from model import Model
from view import View

def pressEnter():
    input()
    return True


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def show_init_menu(self, msg = ''):
        print('\n' + msg + '\n')
        index = int(input('Select the table to work with | command: \n' + '1. Student \n' + '2. Mark \n' \
                          + '3. Show information about student \n' + '4. Show class list \n' \
                          + '5. Show teachers of the student \n' + '6. Show marks of the student on subject \n' \
                          + '7. Show average marks of the student \n' + '8. Show average marks of the class \n' \
                          + '9. Show average marks of classes \n' + '10. Exit \n'))
        if index == 1:
            self.show_entity_menu('student')
        elif index == 2:
            print('here')
            self.show_entity_menu('mark')
        elif index == 3:
            self.show_student_info()
        elif index == 4:
            self.show_class_list()
        elif index == 5:
            self.show_student_teachers()
        elif index == 6:
            self.show_student_marks()
        elif index == 7:
            self.show_student_average_mark()
        elif index == 8:
            self.show_class_average_subject_mark()
        elif index == 9:
            self.show_classes_average_mark()
        else:
            print('Bye, have a beautiful day!')
            exit()

    def show_entity_menu(self, tableName, msg = ''):
        print('\n' + msg + '\n')
        index = int(input('Select command: \n' + '1. Get \n' + '2. Delete \n' + '3. Update \n' \
                      + '4. Insert \n' + '5. Fill by random data \n' + '6. Back \n'))
        if index == 1:
            self.get(tableName)
        elif index == 2:
            self.delete(tableName)
        elif index == 3:
            self.update(tableName)
        elif index == 4:
            self.insert(tableName)
        elif index == 5:
            self.fillByRandom(tableName)
        else:
            self.show_init_menu()

    def get(self, tableName):
        try:
            id = input('Enter id: ')
            try:
                int(id)
            except ValueError:
                print("Incorrect data, it will be 1")
                id = 1
            if tableName == 'student':
                data = self.model.student_get(id)
            if tableName == 'mark':
                data = self.model.mark_get(id)
            self.view.print(data)
            pressEnter()
            self.show_entity_menu(tableName)
        except Exception as err:
            self.show_entity_menu(tableName, str(err))

    def insert(self, tableName):
        try:
            if tableName == 'student':
                name = input('Enter name: ')
                surname = input('Enter surname: ')
                class_name = input('Enter class name: ')
                t = True
                while t == True:
                    t = False
                    date_of_birthday = input('Enter birthday date (yyyy-mm-dd): ')
                    try:
                        time.strptime(date_of_birthday, '%Y-%m-%d')
                    except ValueError:
                        print('Invalid date!')
                        t = True
                data = self.model.student_insert(name, surname, date_of_birthday, class_name)
            if tableName == 'mark':
                name = input('Enter name: ')
                surname = input('Enter surname: ')
                subject = input('Enter subject: ')
                t = True
                while t == True:
                    t = False
                    mark = input('Enter mark: ')
                    try:
                        int(mark)
                    except ValueError:
                        print("Incorrect data")
                        t = True
                t = True
                while t == True:
                    t = False
                    date = input('Enter date (yyyy-mm-dd): ')
                    try:
                        time.strptime(date, '%Y-%m-%d')
                    except ValueError:
                        print('Invalid date!')
                        t = True
                data = self.model.mark_insert(name, surname, subject, mark, date)
            self.show_entity_menu(tableName, data)
        except Exception as err:
            self.show_entity_menu(tableName, str(err))

    def delete(self, tableName):
        try:
            id = input('Enter id: ')
            try:
                int(id)
            except ValueError:
                print("Incorrect data, it will be 1")
                id = 1
            if tableName == 'student':
                self.model.student_delete(id)
            if tableName == 'mark':
                self.model.mark_delete(id)
            self.show_entity_menu(tableName, 'Delete is successful')
        except Exception as err:
            self.show_entity_menu(tableName, str(err))

    def update(self, tableName):
        try:
            id = input('Enter id: ')
            try:
                int(id)
            except ValueError:
                print("Incorrect data, it will be 1")
                id = 1
            if tableName == 'student':
                name = input('Enter name: ')
                surname = input('Enter surname: ')
                class_name = input('Enter class name: ')
                t = True
                while t == True:
                    t = False
                    date_of_birthday = input('Enter birthday date (yyyy-mm-dd): ')
                    try:
                        time.strptime(date_of_birthday, '%Y-%m-%d')
                    except ValueError:
                        print('Invalid date!')
                        t = True
                data = self.model.student_update(id, name, surname, date_of_birthday, class_name)
            if tableName == 'mark':
                name = input('Enter name: ')
                surname = input('Enter surname: ')
                subject = input('Enter subject: ')
                t = True
                while t == True:
                    t = False
                    mark = input('Enter mark: ')
                    try:
                        int(mark)
                    except ValueError:
                        print("Incorrect data")
                        t = True
                t = True
                while t == True:
                    t = False
                    date = input('Enter date (yyyy-mm-dd): ')
                    try:
                        time.strptime(date, '%Y-%m-%d')
                    except ValueError:
                        print('Invalid date!')
                        t = True
                data = self.model.mark_update(id, name, surname, subject, mark, date)
            self.show_entity_menu(tableName, data)
        except Exception as err:
            self.show_entity_menu(tableName, str(err))


    def fillByRandom(self, tableName):
        try:
            count = input('Enter a number of rows to generate: ')
            try:
                int(count)
            except ValueError:
                print("Incorrect data, minimum will be 1000")
                count = 1000
            if tableName == 'student':
                self.model.fillStudentByRandomData(count)
            if tableName == 'mark':
                self.model.fillMarkByRandomData(count)
            self.show_init_menu('Generated successfully')
        except Exception as err:
            self.show_init_menu(str(err))

    def show_student_info(self):
        try:
            print("Show information about student")
            name = input('Enter name: ')
            surname = input('Enter surname: ')
            d, data = self.model.get('student', f"name = '{name}' and surname = '{surname}'")
            if len(data) == 0:
                self.show_init_menu('No such student')
            student_id = data[0][0]
            data = self.model.student_info(student_id)
            self.view.print(data)
            pressEnter()
            self.show_init_menu()
        except Exception as err:
            self.show_init_menu(str(err))


    def show_class_list(self):
        try:
            print("Show a list of a class")
            name = input("Enter class: ")
            d, data = self.model.get('class', f"name = '{name}'")
            if len(data) == 0:
                self.show_init_menu('No such class')
            class_id = data[0][0]
            data = self.model.class_list(class_id)
            self.view.print(data)
            pressEnter()
            self.show_init_menu()
        except Exception as err:
            self.show_init_menu(str(err))


    def show_student_teachers(self):
        try:
            print("Show the teachers of student")
            name = input('Enter name: ')
            surname = input('Enter surname: ')
            d, data = self.model.get('student', f"name = '{name}' and surname = '{surname}'")
            if len(data) == 0:
                self.show_init_menu('No such student')
            class_id = data[0][4]
            data = self.model.student_teachers(class_id)
            self.view.print(data)
            pressEnter()
            self.show_init_menu()
        except Exception as err:
            self.show_init_menu(str(err))


    def show_student_marks(self):
        try:
            print("Show the marks of student on the period")
            name = input('Enter name: ')
            surname = input('Enter surname: ')
            d, data = self.model.get('student', f"name = '{name}' and surname = '{surname}'")
            if len(data) == 0:
                self.show_init_menu('No such student')
            student_id = data[0][0]
            subject = input('Enter subject: ')
            d2, data2 = self.model.get('subject', f"name = '{subject}'")
            if len(data2) == 0:
                self.show_init_menu('No such subject')
            subject_id = data2[0][0]
            t = True
            while t == True:
                t = False
                date1 = input('Enter start date (yyyy-mm-dd): ')
                try:
                    time.strptime(date1, '%Y-%m-%d')
                except ValueError:
                    print('Invalid date!')
                    t = True
            t = True
            while t == True:
                t = False
                date2 = input('Enter end date (yyyy-mm-dd): ')
                try:
                    time.strptime(date2, '%Y-%m-%d')
                except ValueError:
                    print('Invalid date!')
                    t = True
            data = self.model.student_marks(student_id, subject_id, date1, date2)
            self.view.print(data)
            length = len(data[1])
            groups = [data[1][i][1] for i in range(length)]
            counts = [data[1][i][0] for i in range(length)]
            plt.stem(groups, counts)
            plt.pause(0)
            pressEnter()
            self.show_init_menu()
        except Exception as err:
            self.show_init_menu(str(err))

    def show_student_average_mark(self):
        try:
            print("Show student average mark")
            name = input('Enter name: ')
            surname = input('Enter surname: ')
            d, data = self.model.get('student', f"name = '{name}' and surname = '{surname}'")
            if len(data) == 0:
                self.show_init_menu('No such student')
            student_id = data[0][0]
            data = self.model.student_average_mark(student_id)
            self.view.print(data)
            length = len(data[1])
            groups = [data[1][i][0] for i in range(length)]
            counts = [data[1][i][1] for i in range(length)]
            plt.bar(groups, counts)
            plt.pause(0)
            pressEnter()
            self.show_init_menu()
        except Exception as err:
            self.show_init_menu(str(err))

    def show_class_average_subject_mark(self):
        try:
            print("Show class average mark on subject")
            name = input("Enter class: ")
            d, data = self.model.get('class', f"name = '{name}'")
            if len(data) == 0:
                self.show_init_menu('No such class')
            class_id = data[0][0]
            data = self.model.class_average_subject_mark(class_id)
            self.view.print(data)
            length = len(data[1])
            groups = [data[1][i][0] for i in range(length)]
            counts = [data[1][i][1] for i in range(length)]
            plt.bar(groups, counts)
            plt.pause(0)
            pressEnter()
            self.show_init_menu()
        except Exception as err:
            self.show_init_menu(str(err))

    def show_classes_average_mark(self):
        try:
            print("Show classes average marks")
            data = self.model.classes_average_mark()
            self.view.print(data)
            length = len(data[1])
            groups = [data[1][i][0] for i in range(length)]
            counts = [data[1][i][1] for i in range(length)]
            plt.bar(groups, counts)
            plt.pause(0)
            pressEnter()
            self.show_init_menu()
        except Exception as err:
            self.show_init_menu(str(err))






