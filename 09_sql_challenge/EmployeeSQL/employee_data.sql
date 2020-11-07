-- HW Tables
CREATE TABLE departments (
    dept_no VARCHAR(225)   NOT NULL,
    dept_name VARCHAR(225)   NOT NULL,
    CONSTRAINT pk_departments PRIMARY KEY (
        dept_no
     )
);

CREATE TABLE dept_emp (
    emp_no INT   NOT NULL,
    dept_no VARCHAR(225)   NOT NULL
);

CREATE TABLE dept_manager (
    dept_no VARCHAR(225)   NOT NULL,
    emp_no INT   NOT NULL
);

CREATE TABLE employees (
    emp_no INT   NOT NULL,
    emp_title_id VARCHAR(225)   NOT NULL,
    birth_date VARCHAR(225)   NOT NULL,
    first_name VARCHAR(225)   NOT NULL,
    last_name VARCHAR(225)   NOT NULL,
    sex VARCHAR(225)   NOT NULL,
    hire_date VARCHAR(225)   NOT NULL,
    CONSTRAINT pk_employees PRIMARY KEY (
        emp_no
     )
);

CREATE TABLE salaries (
    emp_no INT   NOT NULL,
    salary INT   NOT NULL
);

CREATE TABLE titles (
    title_id VARCHAR(225)   NOT NULL,
    title VARCHAR(225)   NOT NULL,
    CONSTRAINT pk_titles PRIMARY KEY (
        title_id
     )
);

ALTER TABLE dept_emp ADD CONSTRAINT fk_dept_emp_emp_no FOREIGN KEY(emp_no)
REFERENCES employees (emp_no);

ALTER TABLE dept_emp ADD CONSTRAINT fk_dept_emp_dept_no FOREIGN KEY(dept_no)
REFERENCES departments (dept_no);

ALTER TABLE dept_manager ADD CONSTRAINT fk_dept_manager_dept_no FOREIGN KEY(dept_no)
REFERENCES departments (dept_no);

ALTER TABLE dept_manager ADD CONSTRAINT fk_dept_manager_emp_no FOREIGN KEY(emp_no)
REFERENCES employees (emp_no);

ALTER TABLE employees ADD CONSTRAINT fk_employees_emp_title_id FOREIGN KEY(emp_title_id)
REFERENCES titles (title_id);

ALTER TABLE salaries ADD CONSTRAINT fk_salaries_emp_no FOREIGN KEY(emp_no)
REFERENCES employees (emp_no);

-- Data Analysis
-- 1. List the following details of each employee: employee number, last name, first name, sex, and salary.
SELECT emp.emp_no, emp.last_name, emp.first_name, emp.sex, s.salary
FROM employees emp
JOIN salaries s ON emp.emp_no = s.emp_no;

-- 2. List first name, last name, and hire date for employees who were hired in 1986.
SELECT first_name, last_name, hire_date
FROM employees
WHERE hire_date LIKE '%1986'

-- 3. List the manager of each department with the following information: department number, 
-- department name, the manager's employee number, last name, first name.
SELECT depts.dept_no, depts.dept_name, man.emp_no, emp.last_name, emp.first_name
FROM departments depts
JOIN dept_manager man ON depts.dept_no = man.dept_no
JOIN employees emp ON man.emp_no = emp.emp_no;

-- 4. List the department of each employee with the following information: 
-- employee number, last name, first name, and department name.
SELECT emp.emp_no, emp.last_name, emp.first_name, depts.dept_name
FROM departments depts
JOIN dept_emp ON dept_emp.dept_no = depts.dept_no
JOIN employees emp ON dept_emp.emp_no = emp.emp_no;

-- 5. List first name, last name, and sex for employees whose first name 
-- is "Hercules" and last names begin with "B."
SELECT first_name, last_name, sex
FROM employees
WHERE first_name = 'Hercules'
AND last_name LIKE 'B%';

-- 6. List all employees in the Sales department, including their employee number,
-- last name, first name, and department name.
SELECT emp.emp_no, emp.last_name, emp.first_name, depts.dept_name
FROM departments depts
JOIN dept_emp ON dept_emp.dept_no = depts.dept_no
JOIN employees emp ON emp.emp_no = dept_emp.emp_no
WHERE depts.dept_name = 'Sales';

-- 7. List all employees in the Sales and Development departments, including their
-- employee number, last name, first name, and department name.
SELECT emp.emp_no, emp.last_name, emp.first_name, depts.dept_name
FROM departments depts
JOIN dept_emp ON dept_emp.dept_no = depts.dept_no
JOIN employees emp ON emp.emp_no = dept_emp.emp_no
WHERE depts.dept_name = 'Development'
OR depts.dept_name = 'Sales';

-- 8. In descending order, list the frequency count of employee last names, 
-- i.e., how many employees share each last name.
SELECT last_name, COUNT(last_name)
FROM employees
GROUP BY last_name
ORDER BY COUNT(last_name) DESC;

