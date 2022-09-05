import datetime
from decimal import Decimal
import pytest


@pytest.mark.usefixtures('init_db')
class TestJoins:
    def test_002_validate_deprt_location_name_join_with_department(self, get_connection):
        get_connection.execute("""
                SELECT d.d_number, d.d_name, dl.dept_location 
                FROM department AS d
                JOIN dept_locations AS dl
                ON d.d_number = dl.d_number;""")
        actual_result = get_connection.fetchall()
        assert actual_result == [(5, 'it-department', 'Toronto'), (4, 'sales', 'New-York'), (3, 'office', 'Paris')], "Test fail"


    def test_015_fetch_employees_order_by_start_day_in_department(self, get_connection):
        get_connection.execute("""
                SELECT e.first_name, e.last_name, d.d_name, d.mgr_srart_day 
                FROM employee AS e 
                JOIN department AS d
                ON e.ssn = d.mgr_ssn
                ORDER BY d.mgr_srart_day ;""")
        actual_result = get_connection.fetchall()
        actual_result_list = []
        for i in range(len(actual_result)):
            actual_result_list.append(actual_result[i])
        print(actual_result)
        assert actual_result_list == [('Anna', 'Sui', 'it-department', datetime.date(2020, 3, 1)),
                                      ('Anna', 'Sui', 'sales', datetime.date(2021, 5, 1)),
                                      ('Donna', 'Karan', 'office', datetime.date(2022, 12, 1))]

    def test_016_find_total_employess_in_department(self, get_connection):
        get_connection.execute("""
                SELECT d.d_name, COUNT(*)
                FROM employee AS e
                JOIN department AS d
                ON e.department_num = d.d_number
                GROUP BY d.d_name ;""")
        actual_result = get_connection.fetchall()
        actual_result_list = []
        for i in range(len(actual_result)):
            actual_result_list.append(actual_result[i])
        print(actual_result)
        assert actual_result_list == [('it-department', 1), ('office', 2), ('sales', 3)]

    def test_018_fetch_number_of_dependencies(self, get_connection):
        get_connection.execute("""
                SELECT e.first_name, e.last_name, COUNT(*) FROM dependent AS d
                JOIN employee AS e
                ON e.ssn = d.essn
                GROUP BY e.first_name, e.last_name;""")
        actual_result = get_connection.fetchall()
        actual_result_list = []
        for i in range(len(actual_result)):
            actual_result_list.append(actual_result[i])
        assert actual_result_list == [('Andrea', 'Andr', 3), ('Anna', 'Sui', 2)]

    def test_020_fetch_first_three_employee_with_low_salary_with_department(self, get_connection):
        get_connection.execute("""
                SELECT e.first_name, e.last_name, e.salary, d.d_name
                FROM employee AS e
                JOIN department AS d
                ON e.department_num = d.d_number
                ORDER BY e.salary ASC
                FETCH FIRST 3 ROWS ONLY;""")
        actual_result = get_connection.fetchall()
        actual_result_list = []
        for i in range(len(actual_result)):
            actual_result_list.append(actual_result[i])
        assert actual_result_list == [('Albert', 'Alt', Decimal('73000.00'), 'sales'), ('Donna', 'Karan', Decimal('74000.00'), 'sales'),
                                      ('Dora', 'Dor', Decimal('81000.00'), 'office')]

    def test_021_fetch_dependensies_that_employee_have_inner_join(self, get_connection):
        get_connection.execute("""
                SELECT e.first_name, e.last_name, d.dependent_name, d.relationship
                FROM employee AS e
                INNER JOIN dependent AS d
                ON d.essn = e.ssn;""")
        actual_result = get_connection.fetchall()
        actual_result_list = []
        for i in range(len(actual_result)):
            actual_result_list.append(actual_result[i])
        assert actual_result_list == [('Anna', 'Sui', 'Tim', 'spouse'), ('Anna', 'Sui', 'Alice', 'doughter'),
                                      ('Andrea', 'Andr', 'Sarah', 'doughter'), ('Andrea', 'Andr', 'Ban', 'son'), ('Andrea', 'Andr', 'Toma', 'spouse')]

    def test_022_fetch_employess_left_join_with_no_dependencies(self, get_connection):
        get_connection.execute("""
                SELECT e.first_name, e.last_name, d.dependent_name, d.relationship
                FROM employee AS e
                LEFT JOIN dependent AS d
                ON d.essn = e.ssn
                WHERE d.relationship IS NULL;""")
        actual_result = get_connection.fetchall()
        actual_result_list = []
        for i in range(len(actual_result)):
            actual_result_list.append(actual_result[i])
        assert actual_result_list == [('Albert', 'Alt', None, None), ('Cristian', 'Crist', None, None),
                                      ('Donna', 'Karan', None, None), ('Dora', 'Dor', None, None)]

    def test_023_fetch_correspondence_project_wors_on_with_emplyee(self, get_connection):
        get_connection.execute("""
                SELECT e.first_name, e.last_name, p.project_name
                FROM employee AS e
                FULL JOIN works_on AS w
                ON w.essn = e.ssn
                FULL JOIN project AS p
                ON p.project_number = w.project_num;""")
        actual_result = get_connection.fetchall()
        actual_result_list = []
        for i in range(len(actual_result)):
            actual_result_list.append(actual_result[i])
        assert actual_result_list == [('Anna', 'Sui', 'New --it-- project - One'), ('Donna', 'Karan', 'New --sales-- project - Two'),
                                      ('Cristian', 'Crist', 'New --it-- project - One'), ('Cristian', 'Crist', 'New --office-- project - Three'),
                                      ('Anna', 'Sui', 'New --office-- project - Three'), ('Andrea', 'Andr', None),
                                      ('Albert', 'Alt', None), ('Dora', 'Dor', None)]








