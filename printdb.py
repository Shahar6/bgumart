from persistence import *


def main():
    print('Activities')
    for activitie in repo.activities.find_all_by("activities.date ASC"):
        t = (activitie.product_id, activitie.quantity, activitie.activator_id, activitie.date)
        print(t)

    print('Branches')
    for branche in repo.branches.find_all():
        t = (branche.id, branche.location, branche.number_of_employees)
        print(t)

    print('Employees')
    for employee in repo.employees.find_all():
        t = (employee.id, employee.name, employee.salary, employee.branche)
        print(t)

    print('Products')
    for product in repo.products.find_all():
        t = (product.id, product.description, product.price, product.quantity)
        print(t)

    print('Suppliers')
    for supplier in repo.suppliers.find_all():
        t = (supplier.id, supplier.name, supplier.contact_information)
        print(t)

    print('\nEmployees report')
    for employee in repo.employees.find_all_by("employees.name ASC"):
        sum = 0
        for activitie in repo.activities.find_all():
            if activitie.activator_id == employee.id:
                product = repo.products.find(id=activitie.product_id)[0]
                sum += activitie.quantity * product.price
        sum = abs(sum)
        print(employee.name + " " + str(employee.salary) + " " + repo.branches.find(id=employee.branche)[
            0].location + " " + str(sum))

    print('\nActivities report')
    c = repo._conn.cursor()
    acs = c.execute("""SELECT activities.activator_id, activities.date, products.description, activities.quantity
            FROM (activities INNER JOIN products ON activities.product_id = products.id) ORDER BY activities.date ASC""").fetchall()
    for activitie in acs:
        if activitie[3] > 0:
            t = (activitie[1], activitie[2], activitie[3], "None", repo.suppliers.find(id=activitie[0])[0].name)
        else:
            t = (activitie[1], activitie[2], activitie[3], repo.employees.find(id=activitie[0])[0].name, "None")
        print(t)


if __name__ == '__main__':
    main()
