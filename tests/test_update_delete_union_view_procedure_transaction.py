import pytest


@pytest.mark.usefixtures('init_db')
class TestUpdateDeleteUnionViewProcedure:
    def test_003_update_salary_employee_table(self, get_connection):
        get_connection.execute("""
                UPDATE employee
                SET salary = '95000'
                WHERE ssn = '1';""")
        get_connection.execute("""
                SELECT salary FROM employee
                WHERE ssn = '1';""")
        actual_result = get_connection.fetchone()
        assert actual_result[0] == 95000.00, "The actual and expected results are NOT MATCH"

    def test_004_delete_row_from_works_on_table(self, get_connection):
        get_connection.execute("""
                DELETE FROM works_on 
                WHERE essn = '1'  AND project_num = '1';""")
        get_connection.execute("""
                SELECT * FROM works_on
                WHERE essn = '1'  AND project_num = '1';""")
        actual_result = get_connection.fetchone()
        assert actual_result == None, "The actual and expected results are NOT MATCH"

    def test_009_fetch_employees_department_and_projects_works_on_without_join(self, get_connection):
        get_connection.execute("""
                (SELECT DISTINCT p.project_name, p.project_number
                FROM project AS p, employee AS e, department AS d
                WHERE p.d_number = d.d_number AND d.mgr_ssn = e.ssn AND e.last_name = 'Sui')
                UNION 
                (SELECT DISTINCT  p.project_name, p.project_number
                FROM works_on AS w, employee AS e, project AS p
                WHERE w.project_num = p.project_number AND w.essn = e.ssn AND e.last_name = 'Sui');""")
        actual_result = get_connection.fetchall()
        actual_result_list = []
        for i in range(len(actual_result)):
            actual_result_list.append(actual_result[i])
        assert actual_result_list == [('New --it-- project - One', 50),('New --sales-- project - Two', 60),('New --office-- project - Three', 70)]

    def test_024_employee_list_as_view(self, get_connection):
        get_connection.execute("DROP VIEW IF EXISTS salary_list_view;")
        get_connection.execute("""
                CREATE VIEW salary_list_view 
                AS SELECT e.first_name, e.last_name, d.d_name
                FROM employee AS e
                JOIN department AS d
                ON e.department_num = d.d_number;""")
        get_connection.execute("SELECT * FROM salary_list_view;")
        actual_result = get_connection.fetchall()
        actual_result_list = []
        for i in range(len(actual_result)):
            actual_result_list.append(actual_result[i])
        assert actual_result_list == [('Donna', 'Karan', 'sales'), ('Cristian', 'Crist', 'sales'),
                                        ('Albert', 'Alt', 'sales'), ('Dora', 'Dor', 'office'),
                                        ('Andrea', 'Andr', 'office'), ('Anna', 'Sui', 'it-department')]

    def test_025_procedure_insert_data_dependent_table(self, get_connection):
        get_connection.execute("DROP PROCEDURE IF EXISTS insert_values CASCADE;")
        get_connection.execute("DELETE FROM dependent WHERE essn = '1' AND dependent_name = 'Lora';")
        get_connection.execute("""
                CREATE PROCEDURE insert_values (x INTEGER, first_name VARCHAR(10))
                    LANGUAGE SQL
                    AS $$
                    INSERT INTO dependent VALUES (x, first_name)
                    $$;""")
        get_connection.execute("CALL insert_values ('1', 'Lora');")
        get_connection.execute("SELECT * FROM dependent WHERE essn = '1' AND dependent_name = 'Lora';")
        actual_result = get_connection.fetchall()
        get_connection.execute("DELETE FROM dependent WHERE essn = '1' AND dependent_name = 'Lora';")
        actual_result_list = []
        for i in range(len(actual_result)):
            actual_result_list.append(actual_result[i])
        assert actual_result_list == [('1', 'Lora', None, None, None)]

    def test_026_transaction(self, get_connection):
        get_connection.execute("DELETE FROM dependent WHERE essn = '6' AND dependent_name = 'Toma';")
        get_connection.execute("""INSERT INTO dependent(essn, dependent_name, gender, date_of_birth, relationship)
                                VALUES ('6', 'Toma','female', '1988-11-08', 'spouse');""")
        get_connection.execute("BEGIN;")
        get_connection.execute("DELETE FROM dependent WHERE essn = '6' AND dependent_name = 'Toma';")
        get_connection.execute("COMMIT;")
        get_connection.execute("SELECT * FROM dependent  WHERE essn = '6' AND dependent_name = 'Toma';")
        actual_result = get_connection.fetchall()
        get_connection.execute("""INSERT INTO dependent(essn, dependent_name, gender, date_of_birth, relationship)
                                VALUES ('6', 'Toma','female', '1988-11-08', 'spouse');""")
        actual_result_list = []
        for i in range(len(actual_result)):
            actual_result_list.append(actual_result[i])
        assert actual_result_list == []






