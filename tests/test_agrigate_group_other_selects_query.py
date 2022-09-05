import datetime
from decimal import Decimal
import pytest


@pytest.mark.usefixtures('init_db')
class TestAgrigateGroupOtherSelectQueries:
    def test_001_all_data_from_deprt_table(self, get_connection):
        get_connection.execute("SELECT * FROM department;")
        actual_result = get_connection.fetchall()
        assert actual_result == [
            ('it-department', 5, '1', datetime.date(2020, 3, 1)),
            ('sales', 4, '1', datetime.date(2021, 5, 1)),
            ('office', 3, '2', datetime.date(2022, 12, 1))]

    def test_005_validate_distinct_employee_in_works_on_table(self, get_connection):
        get_connection.execute("""
                SELECT DISTINCT essn
                FROM works_on;""")
        actual_result = get_connection.fetchall()
        actual_result_list = []
        for i in range(len(actual_result)):
            actual_result_list.append(actual_result[i][0])
        assert actual_result_list == ['2', '3', '1'], "The actual and expected results are NOT MATCH"

    def test_006_fetch_employee_without_dependency(self, get_connection):
        get_connection.execute("""
                SELECT first_name, last_name
                FROM employee
                WHERE NOT EXISTS (SELECT * FROM dependent WHERE ssn = essn);""")
        actual_result = get_connection.fetchall()
        actual_result_list = []
        for i in range(len(actual_result)):
            actual_result_list.append(actual_result[i])
        assert actual_result_list == [('Donna', 'Karan'),('Cristian', 'Crist'),('Albert', 'Alt'),('Dora', 'Dor')], "The actual and expected results are NOT MATCH"

    def test_007_fetch_employee_from_one_location(self, get_connection):
        get_connection.execute("""
                SELECT first_name, last_name
                FROM employee
                WHERE address LIKE '%Canada%';""")
        actual_result = get_connection.fetchall()
        actual_result_list = []
        for i in range(len(actual_result)):
            actual_result_list.append(actual_result[i])
        assert actual_result_list == [('Anna', 'Sui'), ('Albert', 'Alt')], "The actual and expected results are NOT MATCH"

    def test_008_fetch_employee_where_salary_between_4800_10000(self, get_connection):
        get_connection.execute("""
                SELECT first_name, last_name
                FROM employee
                WHERE salary BETWEEN '80000' AND '85000';""")
        actual_result = get_connection.fetchall()
        actual_result_list = []
        for i in range(len(actual_result)):
            actual_result_list.append(actual_result[i])
        assert actual_result_list == [('Dora', 'Dor'), ('Andrea','Andr')], "The actual and expected results are NOT MATCH"

    def test_010_fetch_employees_without_dependencies(self, get_connection):
        get_connection.execute("""
                SELECT ssn, first_name, last_name 
                FROM employee 
                WHERE NOT EXISTS (SELECT * FROM dependent WHERE ssn = essn);""")
        actual_result = get_connection.fetchall()
        actual_result_list = []
        for i in range(len(actual_result)):
            actual_result_list.append(actual_result[i])
        assert actual_result_list == [('2', 'Donna', 'Karan'),
                                      ('3', 'Cristian', 'Crist'),
                                      ('4', 'Albert', 'Alt'),
                                      ('5', 'Dora', 'Dor')]

    def test_011_fetch_employees_with_three_char_last_name(self, get_connection):
        get_connection.execute("""
                SELECT ssn, first_name, last_name 
                FROM employee 
                WHERE last_name LIKE '___';""")
        actual_result = get_connection.fetchall()
        actual_result_list = []
        for i in range(len(actual_result)):
            actual_result_list.append(actual_result[i])
        assert actual_result_list == [('1', 'Anna', 'Sui'), ('4', 'Albert', 'Alt'), ('5', 'Dora', 'Dor')]

    def test_012_fetch_employees_with_increased_salary_on_particular_project(self, get_connection):
        get_connection.execute("""
                SELECT e.first_name, e.last_name, 1.2* e.salary AS INCREASED_SALARY
                FROM employee AS e, works_on AS w, project AS p
                WHERE e.ssn = w.essn AND p.project_number = w.project_num AND p.project_name = 'New --it-- project - One';""")
        actual_result = get_connection.fetchall()
        actual_result_list = []
        for i in range(len(actual_result)):
            actual_result_list.append(actual_result[i])
        assert actual_result_list == [('Anna', 'Sui', Decimal('108000.000')), ('Cristian', 'Crist', Decimal('104400.000'))]

    def test_013_calc_total_min_max_salary(self, get_connection):
        get_connection.execute("SELECT SUM(salary), MIN(salary), MAX(salary) FROM employee;")
        actual_result = get_connection.fetchone()
        print()
        print(actual_result[0], actual_result[1], actual_result[2])
        assert [actual_result[0], actual_result[1], actual_result[2]] == [Decimal('487000.00'), Decimal('73000.00'), Decimal('90000.00')]

    def test_014_fetch_employees_order_by_salary(self, get_connection):
        get_connection.execute("""
                SELECT first_name, last_name, salary
                FROM employee
                ORDER BY salary DESC;""")
        actual_result = get_connection.fetchall()
        actual_result_list = []
        for i in range(len(actual_result)):
            actual_result_list.append(actual_result[i])
        assert actual_result_list == [('Anna', 'Sui', Decimal('95000.00')),
                                        ('Cristian', 'Crist', Decimal('87000.00')),
                                        ('Andrea', 'Andr', Decimal('82000.00')),
                                        ('Dora', 'Dor', Decimal('81000.00')),
                                        ('Donna', 'Karan', Decimal('74000.00')),
                                        ('Albert', 'Alt', Decimal('73000.00'))]

    def test_017_fetch_projects_are_in_progress(self, get_connection):
        get_connection.execute("""
                SELECT p.project_number, p.project_name, COUNT(*)
                FROM project AS p, works_on AS w
                WHERE p.project_number = w.project_num
                GROUP BY p.project_number
                HAVING COUNT(*)>=2;""")
        actual_result = get_connection.fetchall()
        actual_result_list = []
        for i in range(len(actual_result)):
            actual_result_list.append(actual_result[i])
        print(actual_result)
        assert actual_result_list == [(70, 'New --office-- project - Three', 2), (50, 'New --it-- project - One', 2)]

    def test_019_fetch_first_three_employee_with_top_salary(self, get_connection):
        get_connection.execute("""
                SELECT first_name, last_name, salary
                FROM employee
                ORDER BY salary DESC
                LIMIT 3;""")
        actual_result = get_connection.fetchall()
        actual_result_list = []
        for i in range(len(actual_result)):
            actual_result_list.append(actual_result[i])
        assert actual_result_list == [('Anna', 'Sui', Decimal('95000.00')), ('Cristian', 'Crist', Decimal('87000.00')), ('Andrea', 'Andr', Decimal('82000.00'))]








