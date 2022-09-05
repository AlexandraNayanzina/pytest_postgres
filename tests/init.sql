DROP TABLE IF EXISTS dependent CASCADE;
DROP TABLE IF EXISTS works_on CASCADE;
DROP TABLE IF EXISTS project CASCADE;
DROP TABLE IF EXISTS dept_locations CASCADE;
DROP TABLE IF EXISTS department CASCADE;
DROP TABLE IF EXISTS employee CASCADE;

CREATE TABLE IF NOT EXISTS employee(
                ssn VARCHAR(10) NOT NULL PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                date_of_birth DATE,
                address TEXT NOT NULL,
                gender VARCHAR NULL,
                salary DECIMAL (10,2) NULL,
                super_ssn VARCHAR(9) NULL,
                department_num INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS department(
                d_name TEXT NOT NULL,
                d_number INTEGER NOT NULL PRIMARY KEY,
                mgr_ssn VARCHAR(10) NOT NULL,
                mgr_srart_day DATE NULL);
 CREATE TABLE IF NOT EXISTS dept_locations(
                d_number INTEGER NOT NULL,
                dept_location TEXT NOT NULL,
                PRIMARY KEY (d_number, dept_location));
CREATE TABLE IF NOT EXISTS project(
                project_name TEXT NOT NULL,
                project_number INTEGER NOT NULL,
                p_location TEXT,
                d_number INTEGER NOT NULL,
                PRIMARY KEY (project_number),
                UNIQUE (project_name));
CREATE TABLE IF NOT EXISTS works_on(
                essn VARCHAR(9) NOT NULL,
                project_num INTEGER NOT NULL,
                hours DECIMAL(3,1) NOT NULL,
                PRIMARY KEY (essn, project_num));
CREATE TABLE IF NOT EXISTS dependent(
                essn VARCHAR(9) NOT NULL,
                dependent_name TEXT NOT NULL,
                gender VARCHAR NULL,
                date_of_birth DATE,
                relationship TEXT,
                PRIMARY KEY (essn, dependent_name));
INSERT INTO employee(ssn, first_name, last_name, date_of_birth, address, gender, salary, super_ssn, department_num)
VALUES          ('1', 'Anna', 'Sui', '1990-03-03', 'Canada, Waterloo, 251 North st', 'female', 90000, Null, '5'),
                ('2', 'Donna', 'Karan', '1990-05-07', 'USA, New-York, 8 East st', 'female', 74000, '1', '4'),
                ('3', 'Cristian', 'Crist', '1986-10-09', 'France, Paris, 258 West st', 'male', 87000, '2', '4'),
				('4', 'Albert', 'Alt', '1987-10-09', 'Canada, Toronto, 11 West st', 'male', 73000, '2', '4'),
				('5', 'Dora', 'Dor', '1985-04-03', 'France, Paris, 12 South st', 'female', 81000, '3', '3'),
				('6', 'Andrea', 'Andr', '1988-02-10', 'USA, New-York, 30 West st', 'male', 82000, '3', '3');
INSERT INTO department(d_name, d_number, mgr_ssn, mgr_srart_day)
VALUES          ('it-department', '5', '1', '2020-03-01'),
                ('sales', '4', '1', '2021-05-01'),
                ('office', '3', '2', '2022-12-01');
INSERT INTO dept_locations(d_number, dept_location)
VALUES          ('5', 'Toronto'),
                ('4', 'New-York'),
                ('3', 'Paris');
INSERT INTO project(project_name, project_number, p_location, d_number)
VALUES          ('New --it-- project - One', 50,'New-York', '5'),
                ('New --sales-- project - Two', 60, 'Ottava', '4'),
                ('New --office-- project - Three', 70,'Washington', '3');
INSERT INTO works_on(essn, project_num, hours)
VALUES          ('1', 50, 20),
                ('2', 60, 40),
                ('3', 50 ,20),
                ('3', 70 ,30),
                ('1', 70 ,10);
INSERT INTO dependent(essn, dependent_name, gender, date_of_birth, relationship)
VALUES          ('1', 'Tim','female', '1990-01-01', 'spouse'),
                ('1', 'Alice','male', '2018-03-11', 'doughter'),
                ('6', 'Sarah','female', '2019-11-08', 'doughter'),
                ('6', 'Ban','male', '2018-11-08', 'son'),
                ('6', 'Toma','female', '1988-11-08', 'spouse');
ALTER TABLE department ADD FOREIGN KEY (mgr_ssn) REFERENCES employee(ssn);
ALTER TABLE employee ADD FOREIGN KEY (super_ssn) REFERENCES employee(ssn);
ALTER TABLE employee ADD FOREIGN KEY (department_num) REFERENCES department(d_number);
ALTER TABLE dept_locations ADD FOREIGN KEY (d_number) REFERENCES department(d_number);
ALTER TABLE project ADD FOREIGN KEY (d_number) REFERENCES department(d_number);
ALTER TABLE works_on ADD FOREIGN KEY (essn) REFERENCES employee(ssn);
ALTER TABLE works_on ADD FOREIGN KEY (project_num) REFERENCES project(project_number);
ALTER TABLE dependent ADD FOREIGN KEY (essn) REFERENCES employee(ssn);