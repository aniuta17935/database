import psycopg2
import time

class Model:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(host="localhost", port="5433",
                                               database='school', user='postgres', password='sashasasha1')
            self.cursor = self.connection.cursor()
        except (Exception, psycopg2.Error) as error:
            print("Помилка при з'єднанні з PostgreSQL", error)

    def get_col_names(self):
        return [d[0] for d in self.cursor.description]

    def get(self, tname, condition):
        try:
            query = f'SELECT * FROM {tname}'

            if condition:
                query += ' WHERE ' + condition

            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def delete(self, tname, condition):
        try:
            query = f'DELETE FROM {tname} WHERE {condition};'
            self.cursor.execute(query)
        finally:
            self.connection.commit()

    def student_get(self, id):
        try:
            query = f'SELECT * FROM student WHERE student_id = {id};'
            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def student_insert(self, name, surname, date_of_birthday, class_name):
        try:
            d, data = self.get('class', f"name = '{class_name}'")
            if len(data) == 0:
                return 'No such class'
            class_id = data[0][0]
            query = f'''INSERT INTO student (name, surname, date_of_birthday, class_id_fk)
            VALUES ('{name}', '{surname}', '{date_of_birthday}', {class_id});'''
            self.cursor.execute(query)
            return 'Insert is successful!'
        finally:
            self.connection.commit()

    def student_delete(self, id):
        try:
            self.delete('mark', 'student_id_fk = ' + id)
            query = f'DELETE FROM student WHERE student_id = {id};'
            self.cursor.execute(query)
        finally:
            self.connection.commit()

    def student_update(self, id, name, surname, date_of_birthday, class_name):
        try:
            d, data = self.get('class', f"name = '{class_name}'")
            if len(data) == 0:
                return 'No such class'
            class_id = data[0][0]
            query = f'''UPDATE student SET name = '{name}', surname = '{surname}',
            date_of_birthday = '{date_of_birthday}', class_id_fk = {class_id} WHERE student_id = {id}'''
            self.cursor.execute(query)
            return 'Update is successful!'
        finally:
            self.connection.commit()


    def mark_get(self, id):
        try:
            query = f'SELECT * FROM mark  WHERE mark_id = {id}'
            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def mark_insert(self, name, surname, subject, mark, date):
        try:
            d, data = self.get('student', f"name = '{name}' and surname = '{surname}'")
            if len(data) == 0:
                return 'No such student'
            student_id = data[0][0]
            d2, data2 = self.get('subject', f"name = '{subject}'")
            if len(data2) == 0:
                return 'No such subject'
            subject_id = data2[0][0]
            query = f'''INSERT INTO mark (student_id_fk, subject_id_fk, mark, date)
            VALUES ({student_id}, {subject_id}, {mark}, '{date}');'''
            self.cursor.execute(query)
            return 'Insert is successful!'
        finally:
            self.connection.commit()

    def mark_delete(self, id):
        try:
            query = f'DELETE FROM mark WHERE mark_id = {id};'
            self.cursor.execute(query)
        finally:
            self.connection.commit()

    def mark_update(self, id, name, surname, subject, mark, date):
        try:
            d, data = self.get('student', f"name = '{name}' and surname = '{surname}'")
            if len(data) == 0:
                return 'No such student'
            student_id = data[0][0]
            d2, data2 = self.get('subject', f"name = '{subject}'")
            if len(data2) == 0:
                return 'No such subject'
            subject_id = data2[0][0]
            query = f'''UPDATE mark SET student_id_fk = {student_id}, subject_id_fk = {subject_id},
            mark = {mark}, date = '{date}' WHERE mark_id = {id}'''
            self.cursor.execute(query)
            return 'Update is successful!'
        finally:
            self.connection.commit()

    def fillStudentByRandomData(self, count):
        try:
            query = f"select random_students({count})"
            self.cursor.execute(query)
        finally:
            self.connection.commit()

    def fillMarkByRandomData(self, count):
        try:
            query = f"select random_marks({count})"
            self.cursor.execute(query)
        finally:
            self.connection.commit()

    def student_info(self, student_id):
        try:
            query = f'''select student_id, concat(student.name, ' ', student.surname) as fullname, date_of_birthday,
                        class.name as class,  concat(teacher.name, ' ', teacher.surname) as teacher_fullname from student
                        inner join class on student.class_id_fk = class.class_id
                        inner join teacher on class.teacher_id_fk = teacher.teacher_id
                        where student.student_id = {student_id}'''
            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def class_list(self, class_id):
        try:
            query = f"select concat (name, ' ', surname) as fullname, date_of_birthday from student where student.class_id_fk = {class_id} order by surname"
            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def student_teachers(self, class_id):
        try:
            query = f'''select teacher_id, concat (t.name, ' ', surname) as fullname, s.name as subject from teacher t
                        inner join teacher_subject_class tsc on t.teacher_id = tsc.teacher_id_fk inner join subject s
                        on s.subject_id = tsc.subject_id_fk where tsc.class_id_fk = {class_id}'''
            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def student_marks(self, student_id, subject_id, date1, date2):
        try:
            query = f'''select mark, date from mark where student_id_fk = {student_id} and
                        subject_id_fk = {subject_id} and date between '{date1}' and '{date2}' order by date'''
            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def student_average_mark(self, student_id):
        try:
            query = f'''select name, round(avg(mark),2) as avg_mark from mark inner join subject
                        on mark.subject_id_fk = subject.subject_id where student_id_fk = {student_id}
                        group by name order by avg_mark desc'''
            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def class_average_subject_mark(self, class_id):
        try:
            query = f'''select subject.name,  round(avg(mark),2) as avg_mark from mark inner join student
                    on student.student_id = mark.student_id_fk inner join subject
                    on subject.subject_id = mark.subject_id_fk
                    where class_id_fk = {class_id} group by subject.name order by avg_mark desc'''
            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()

    def classes_average_mark(self):
        try:
            query = f'''select class.name,  round(avg(mark),2) as avg_mark from mark inner join student
                        on student.student_id = mark.student_id_fk inner join class
                        on class.class_id = student.class_id_fk group by class.name order by avg_mark desc'''
            self.cursor.execute(query)
            return self.get_col_names(), self.cursor.fetchall()
        finally:
            self.connection.commit()









