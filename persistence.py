import sqlite3
import atexit
from dbtools import Dao


# Data Transfer Objects:
class Employee(object):
    def __init__(self, id, name, salary, branch):
        self.id = id
        self.name = name
        self.salary = salary
        self.branch = branch


class Supplier(object):
    def __init__(self, id, name, contact_information):
        self.id = id
        self.name = name
        self.contact_information = contact_information


class Product(object):
    def __init__(self, id, description, price, quantity):
        self.id = id
        self.description = description
        self.price = price
        self.quantity = quantity


class Branch(object):
    def __init__(self, id, location, number_of_employees):
        self.id = id
        self.location = location
        self.number_of_employees = number_of_employees


class Activity(object):
    def __init__(self, product_id, quantity, activator_id, date):
        self.product_id = product_id
        self.quantity = quantity
        self.activator_id = activator_id
        self.date = date


# Repository
class Repository(object):
    def __init__(self):
        self._conn = sqlite3.connect('bgumart.db')
        self._conn.text_factory = bytes
        self.employees = Dao(Employee, self._conn)
        self.suppliers = Dao(Supplier, self._conn)
        self.products = Dao(Product, self._conn)
        self.branches = Dao(Branch, self._conn)
        self.activities = Dao(Activity, self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()
    def get_employee_report(self):
        c = self._conn.cursor()
        return c.execute("""SELECT employees.name, employees.salary, branches.location 
        FROM (employees INNER JOIN branches ON employees.branch = branches.id) ORDER BY employees.name ASC""").fetchall()

    def get_all_activities(self):
        c = self._conn.cursor()
        return c.execute("SELECT * FROM activities ORDER BY activities.date ASC").fetchall()

    def get_all_branches(self):
        c = self._conn.cursor()
        return c.execute("SELECT * FROM branches ORDER BY branches.id ASC").fetchall()

    def get_all_employees(self):
        c = self._conn.cursor()
        return c.execute("SELECT * FROM employees ORDER BY employees.id ASC").fetchall()

    def get_all_products(self):
        c = self._conn.cursor()
        return c.execute("SELECT * FROM products ORDER BY products.id ASC").fetchall()

    def get_all_suppliers(self):
        c = self._conn.cursor()
        return c.execute("SELECT * FROM suppliers ORDER BY suppliers.id ASC").fetchall()

    def insert_branch(self, splittedline: list[str]):
        c = self._conn.cursor()
        c.execute("INSERT INTO branches (id, location, number_of_employees) VALUES (?,?,?)",
                  [splittedline[0], splittedline[1], splittedline[2]])
    def insert_supplier(self, splittedline: list[str]):
        c = self._conn.cursor()
        c.execute("INSERT INTO suppliers (id, name, contact_information) VALUES (?,?,?)",
                  [splittedline[0], splittedline[1], splittedline[2]])
    def insert_product(self, splittedline: list[str]):
        c = self._conn.cursor()
        c.execute("INSERT INTO products (id, description, price, quantity) VALUES (?,?,?,?)",
                  [splittedline[0], splittedline[1], splittedline[2], splittedline[3]])
    def insert_employee(self, splittedline: list[str]):
        c = self._conn.cursor()
        c.execute("INSERT INTO employees (id, name, salary, branch) VALUES (?,?,?,?)",
                  [splittedline[0], splittedline[1], splittedline[2], splittedline[3]])

    def create_tables(self):
        self._conn.executescript("""
            CREATE TABLE employees (
                id              INT         PRIMARY KEY,
                name            TEXT        NOT NULL,
                salary          REAL        NOT NULL,
                branch    INT REFERENCES branches(id)
            );
    
            CREATE TABLE suppliers (
                id                   INTEGER    PRIMARY KEY,
                name                 TEXT       NOT NULL,
                contact_information  TEXT
            );

            CREATE TABLE products (
                id          INTEGER PRIMARY KEY,
                description TEXT    NOT NULL,
                price       REAL NOT NULL,
                quantity    INTEGER NOT NULL
            );

            CREATE TABLE branches (
                id                  INTEGER     PRIMARY KEY,
                location            TEXT        NOT NULL,
                number_of_employees INTEGER
            );
    
            CREATE TABLE activities (
                product_id      INTEGER REFERENCES products(id),
                quantity        INTEGER NOT NULL,
                activator_id    INTEGER NOT NULL,
                date            TEXT    NOT NULL
            );
        """)

    def execute_command(self, script: str) -> list:
        return self._conn.cursor().execute(script).fetchall()


# singleton
repo = Repository()
atexit.register(repo._close)
