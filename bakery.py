import pandas as pd
import datetime  
import mysql.connector
from prettytable import PrettyTable

#  lenovo
# db = mysql.connector.connect (
#     host = 'localhost',
#     user = 'root',
#     password  = 'Rahul@123',
#     database = 'my_db',
#     port = '3307'
# )
# acer
db = mysql.connector.connect (
    host = 'localhost',
    user = 'rahul',
    password  = 'Rahul@123',
    database = 'my_db',
    port = '3306'
)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bakery_orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(255)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS cust_bill (
    order_id INT,
    customer_name VARCHAR(255),
    cake VARCHAR(255),
    quantity INT,
    cost_per_cake INT,
    sum_of_each_cake INT,
    order_date DATETIME,
    FOREIGN KEY (order_id) REFERENCES bakery_orders(order_id)
)         
""")

db.commit()

def add_order_to_database(order_id, customer_name, cake, quantity, cost_per_cake, total_cost, order_date):
    # Check if the cake already exists in the order
    cursor.execute("SELECT * FROM cust_bill WHERE order_id = %s AND cake = %s", (order_id, cake))
    existing_cake = cursor.fetchone()

    if existing_cake:
        # Cake already exists, update the quantity and total cost
        new_quantity = existing_cake[3] + quantity
        new_total_cost = existing_cake[5] + total_cost
        cursor.execute("UPDATE cust_bill SET quantity = %s, sum_of_each_cake = %s WHERE order_id = %s AND cake = %s",
                       (new_quantity, new_total_cost, order_id, cake))
    else:
        # Cake does not exist, create a new entry
        sql = """
        INSERT INTO cust_bill (order_id, customer_name, cake, quantity, cost_per_cake, sum_of_each_cake, order_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (order_id, customer_name, cake, quantity, cost_per_cake, total_cost, order_date)
        cursor.execute(sql, values)

    db.commit()



def get_order_by_id():
    order_id = int(input('ENTER ORDER ID TO SEARCH: '))
    cursor.execute("SELECT * FROM cust_bill WHERE order_id = %s", (order_id,))
    
    # Fetch all results and check if any row is returned
    orders = cursor.fetchall()

    if orders:
        # Define the table headers
        table = PrettyTable(["order_id", "customer_name", "cake", "quantity", "cost_per_cake", "sum_of_each_cake", "order_date"])

        # Add the order details to the table
        for order in orders:
            table.add_row(order)

        # Set the alignment of each column
        table.align["order_id"] = "r"
        table.align["customer_name"] = "l"
        table.align["cake"] = "l"
        table.align["quantity"] = "r"
        table.align["cost_per_cake"] = "r"
        table.align["sum_of_each_cake"] = "r"
        table.align["order_date"] = "l"

        cursor.execute("SELECT SUM(sum_of_each_cake) FROM cust_bill WHERE order_id = %s GROUP BY order_id", (order_id,))
        total_amount = cursor.fetchone()

        # Print the table
        print(table)
        print(f"{' ' * 62}Total Amount: {total_amount[0]}")
    else:
        print(f"Order with ID {order_id} not found.")



def view_orders_from_database():
    cursor.execute("SELECT * FROM cust_bill")
    cust_bill = cursor.fetchall()

    if not cust_bill:
        print("No orders found.")
        return

    # Define the table headers
    table = PrettyTable(["order_id", "customer_name", "cake", "quantity", "cost_per_cake", "sum_of_each_cake", "order_date"])

    # Add rows to the table
    for order in cust_bill:
        table.add_row(order)

    # Set the alignment of each column
    table.align["order_id"] = "r"
    table.align["customer_name"] = "l"
    table.align["cake"] = "l"
    table.align["quantity"] = "r"
    table.align["cost_per_cake"] = "r"
    table.align["sum_of_each_cake"] = "r"
    table.align["order_date"] = "l"

    # Print the table
    print(table)



def update_order_in_database(order_id, new_cake, new_quantity, new_total_cost):
    cursor.execute("UPDATE cust_bill SET quantity = %s, sum_of_each_cake = %s WHERE order_id = %s AND cake = %s",
                   (new_quantity, new_total_cost, order_id, new_cake))
    db.commit()



def cancel_order_in_database():
    order_id = int(input('ENTER ORDER ID TO CANCEL YOUR ORDER: '))
    
    # Check if the order_id exists before attempting to delete
    cursor.execute("SELECT * FROM cust_bill WHERE order_id = %s", (order_id,))
    existing_order = cursor.fetchall()

    if existing_order:
        cursor.execute("DELETE FROM cust_bill WHERE order_id = %s", (order_id,))
        cursor.execute("DELETE FROM bakery_orders WHERE order_id = %s", (order_id,))
        db.commit()
        print(f"Order with ID {order_id} has been canceled.")
    else:
        print(f"Order with ID {order_id} not found. No changes made.")


def remove_item_from_database(orderid,new_cake):
    cursor.fetchall()
    cursor.execute("SELECT * FROM cust_bill WHERE order_id = %s AND cake = %s", (orderid, new_cake))
    existing_cake = cursor.fetchall()

    if existing_cake:
        cursor.execute("DELETE FROM cust_bill WHERE order_id = %s AND cake = %s", (orderid, new_cake))
        db.commit()
        print("Updating .................")
    else:
        print(f"{new_cake} not found. No changes made.")


def add_cake_to_order(orderid, new_cake):
    quantity = int(input(f"Enter the quantity for {new_cake}: "))
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Assuming 'menu' is a dictionary containing the menu items and their costs
    cost_per_cake = menu.get(new_cake, 0)
    
    if cost_per_cake == 0:
        print(f"{new_cake} not found in the menu. Please enter a valid cake.")
        return

    # Fetch the customer name before executing another query
    cursor.execute("SELECT customer_name FROM cust_bill WHERE order_id = %s", (orderid,))
    existing_cus = cursor.fetchone()

    # Fetch and discard the unread result
    cursor.fetchall()

    if existing_cus:
        # Fetch the result before executing another query
        existing_cus = existing_cus[0]

        # Insert the new cake into the cust_bill table
        sum_of_each_cake = quantity * cost_per_cake
        add_order_to_database(orderid, existing_cus, new_cake, quantity, cost_per_cake, sum_of_each_cake, current_date)
        print(f"{new_cake} added successfully!")
    else:
        print(f"Customer not found for order ID {orderid}. Please check your order.")



def add_orders():
    # Insert into bakery_orders table
    global cus_name 
    cus_name = input('ENTER CUSTOMER NAME: ')
    cursor.execute("INSERT INTO bakery_orders (customer_name) VALUES (%s)", (cus_name,))
    db.commit()
    # Fetch the order_id after insertion
    cursor.execute("SELECT LAST_INSERT_ID()")
    result = cursor.fetchone()

    while True:
        cake = list(map(str, input("ENTER WHICH CAKE YOU WANT: ").split()))
        quantity = list(map(int, input("ENTER QUANTITY: ").split()))
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if result:
            order_id = result[0]
        else:
            print("Error: Failed to fetch order_id.")
            return
        
        for i in range(len(cake)):
            if cake[i] not in bill:
                bill.update({cake[i]: 0})
                order.update({cake[i]: quantity[i]})
                temp = menu[cake[i]] * quantity[i]
                bill[cake[i]] = bill[cake[i]] + temp
                add_order_to_database(order_id, cus_name, cake[i], quantity[i], menu[cake[i]], bill[cake[i]], current_date)
            else:
                temp = menu[cake[i]] * quantity[i]
                bill[cake[i]] = temp + bill[cake[i]]
                order[cake[i]] = order[cake[i]] + quantity[i]
                add_order_to_database(order_id, cus_name, cake[i], quantity[i], menu[cake[i]], bill[cake[i]], current_date)

        q = int(input("DO YOU WANT ANYTHING ELSE? PRESS 1 ELSE 0: "))
        if q == 1:
            continue
        elif q == 0:
            print('ORDER ADDED SUCCESSFULLY !!!')
            break
        else:
            print("INVALID INPUT")
            break


def update_orders():
    orderid = int(input("ENTER THE ORDER ID YOU WANT TO UPDATE: "))

    cursor.execute("SELECT * FROM cust_bill WHERE order_id = %s", (orderid,))
    existing_order = cursor.fetchall()

    if existing_order:
        print('PRESS 1 TO CHANGE QUANTITY, 2 TO REMOVE CAKE, 3 TO ADD CAKE, PRESS 4 TO GO BACK TO PREVIOUS OPTIONS')

        update_option = int(input('ENTER OPTION: '))

        if update_option == 1:
            new_cake = input('ENTER THE CAKE YOU WANT TO UPDATE:')
            cursor.execute("SELECT * FROM cust_bill WHERE cake = %s AND order_id = %s", (new_cake, orderid))
            existing_cake = cursor.fetchone()
            if existing_cake:
                new_quantity = int(input(f"Enter the new quantity for order ID {orderid}: "))
                new_total_cost = new_quantity * existing_cake[4]  
                update_order_in_database(orderid, new_cake, new_quantity, new_total_cost)
                print(f"Order ID {orderid} updated successfully!")
            else:
                print('CAKE NOT FOUND IN THE SPECIFIED ORDER. ENTER CORRECT CAKE')
        elif update_option == 2:
            new_cake = input('ENTER THE CAKE YOU WANT TO REMOVE:')
            cursor.execute("SELECT * FROM cust_bill WHERE cake = %s AND order_id = %s", (new_cake, orderid))
            existing_cake = cursor.fetchone()
            if existing_cake:
                remove_item_from_database(orderid,new_cake)
                print(f"Order ID {new_cake} removed successfully!")
            else:
                print("CAKE NOT FOUND IN THE SPECIFIED ORDER. CAN'T REMOVE SPECIFIED CAKE")
        elif update_option == 3:
            new_cake = input('ENTER THE CAKE YOU WANT TO ADD:')
            add_cake_to_order(orderid, new_cake)
            # print(f"{new_cake} added successfully!")
        elif update_option == 4:
            return
        else:
            print('INVALID OPTION')
    else:
        print(f"Order ID {orderid} not found in the order. Please add it first.")



def save_to_excel():
    cursor.execute("SELECT * FROM cust_bill")
    cust_bill = cursor.fetchall()

    if not cust_bill:
        print('NO ORDERS FOUND.')
        return
    
    order_df = pd.DataFrame(cust_bill, columns=['order_id', 'customer_name', 'cake', 'quantity', 'cost_per_cake', 'sum_of_each_cake', 'order_date'])

    # Save the DataFrame to an Excel file
    file_name = input("Enter the Excel file name to save (without extension): ")
    file_path = f"{file_name}.xlsx"
    order_df.to_excel(file_path, index=False)

    print(f"Order details saved to {file_path}")


menu = {'Classic_Chocolate':30,'Vanilla':40,'Red_Velvet':45,'Bliss':35,'Cookies':35}
# menu = {'a':30,'b':40,'c':45,'d':35,'e':35}
bill = {}
order = {}
print("MENU : ",menu)
# cus_name = ''
# cus_name = input('ENTER CUSTOMER NAME: ')

while True:
    print('1. ADD ORDERS')
    print('2. VIEW ALL ORDERS')
    print('3. VIEW ORDER BY ORDER ID')
    print('4. UPDATE ORDERS')
    print('5. CANCEL ORDER')
    print('6. SAVE TO EXCEL')
    print('7. EXIT')
    options = int(input('ENTER YOUR OPTIONS:'))
    if options == 1:
        add_orders()
    elif options == 2:
        view_orders_from_database()
    elif options == 3:
        get_order_by_id()
    elif options == 4:
        update_orders()
    elif options == 5:
        cancel_order_in_database()
    elif options == 6:
        save_to_excel()
    elif options == 7:
        exit()
    else:
        print('ENTER VALID OPTIONS')
