import pandas as pd
import datetime  
import mysql.connector

db = mysql.connector.connect (
    host = 'localhost',
    user = 'rahul',
    password  = 'Rahul@123',
    database = 'my_db'
)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bakery_orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(255),
    total_amount INT
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
        print("Order found:")
        for order in orders:
            print(order)
    else:
        print(f"Order with ID {order_id} not found.")



def view_orders_from_database():
    cursor.execute("SELECT * FROM cust_bill")
    cust_bill = cursor.fetchall()

    for order in cust_bill:
        print(order)


def update_order_in_database(order_id, new_quantity, new_total_cost):
    cursor.execute("UPDATE cust_bill SET quantity = %s, total_cost = %s WHERE order_id = %s",
                   (new_quantity, new_total_cost, order_id))
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






def add_orders():
    # Insert into bakery_orders table
    cursor.execute("INSERT INTO bakery_orders (customer_name, total_amount) VALUES (%s, %s)", (cus_name, 0))
    db.commit()
    # Fetch the order_id after insertion
    cursor.execute("SELECT LAST_INSERT_ID()")
    result = cursor.fetchone()
    while True:
        # global cus_name 
        global cake 
        # cus_name = input('ENTER CUSTOMER NAME: ')
        cake = list(map(str, input("ENTER WHICH CAKE YOU WANT: ").split()))
        quantity = list(map(int, input("ENTER QUANTITY: ").split()))
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # # Insert into bakery_orders table
        # cursor.execute("INSERT INTO bakery_orders (customer_name, total_amount) VALUES (%s, %s)", (cus_name, 0))
        # db.commit()

        # Fetch the order_id after insertion
        # cursor.execute("SELECT LAST_INSERT_ID()")
        # result = cursor.fetchone()

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
            print(order)
            print(bill)
            break
        else:
            print("INVALID INPUT")
            break


def view_orders():
    sum=0
    line='__'
    space=' '
    # global current_date
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{line*40}")
    print(f"CUSTOMER NAME : {cus_name} {space:7} ORDERID : {space:13} DATE : {current_date}")
    print(f"{line*40}")
    print(f" CAKE {space:5} QUANTITY {space:5} COST_OF_EACH_CAKE {space:5} TOTAL_COST_OF_EACH _CAKE")
    print(f"{line*40}")
    for i in bill:
        sum=sum+bill[i]
        print(f"| {i:15} {order[i]} {' '*15} {menu[i]} {' '*20} {bill[i]} ")

    print(f"{line*40}")
    print(f"{' '*45}TOTAL AMOUNT : {sum}")
    print(f"{line*40}")


def update_orders():

    cake_to_update = input("ENTER THE CAKE YOU WANT TO UPDATE :")

    if cake_to_update in order:
        print(order)
        print('PRESS 1 TO CHANGE QUANTITY , 2 TO REMOVE ITEM , PRESS 3 TO GO BACK TO PREVIOUS OPTIONS')
        update_option = int(input('ENTER OPTION :'))
        if update_option == 1:
            new_quantity = int(input(f"Enter the new quantity for {cake_to_update}: "))
            order[cake_to_update] = new_quantity
            bill[cake_to_update] = new_quantity * menu[cake_to_update]
        elif update_option == 2:
            order.pop(cake_to_update)
            bill.pop(cake_to_update)
        elif update_option == 3:
            return
        else:
            print('INVALID OPTION')

        print(f"{cake_to_update} updated successfully!")
    else:
        print(f"{cake_to_update} not found in the order. Please add it first.")


def cancel_order():
    confirm_cancellation = int(input("ENTER 1 TO CANCEL YOUR ORDER ELSE PRESS 0 :"))
    if confirm_cancellation == 1:
        order.clear()
        bill.clear()
    elif confirm_cancellation == 0:
        return
    else:
        print('INVALID OPTION')



def save_to_excel():
    # Create a DataFrame with the order details
    order_df = pd.DataFrame({
                            #  'CUSTOMER NAME': [cus_name]*len(order),
                             'CAKE': list(order.keys()),
                             'QUANTITY': list(order.values()),
                             'COST PER CAKE': [menu[cake] for cake in order.keys()],
                             'TOTAL COST': list(bill.values())})
                            #  'DATE': [current_date]*len(order)})

    # Save the DataFrame to an Excel file
    file_name = input("Enter the Excel file name to save (without extension): ")
    file_path = f"{file_name}.xlsx"
    order_df.to_excel(file_path, index=False)

    print(f"Order details saved to {file_path}")




# menu = {'Classic Chocolate Cake':30,'Vanilla Bean Celebration Cake':40,'Red Velvet Delight':45,'Lemon Blueberry Bliss':35,'Cookies and Cream Dream Cake':35}
menu = {'a':30,'b':40,'c':45,'d':35,'e':35}
bill = {}
order = {}
print("MENU : ",menu)
cus_name = input('ENTER CUSTOMER NAME: ')

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
        # view_orders()
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

