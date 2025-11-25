import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Global database connection variables
mydb = None
mycursor = None

def create_connection():
    #Establish connection to MySQL database
    global mydb, mycursor
    try:
        # Connect to MySQL server
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MySQLPriyesh@23",  # Change this to your MySQL password
            autocommit=False  # Demonstrating manual commit/rollback
        )
        
        if mydb.is_connected():
            mycursor = mydb.cursor()
            print("\n✓ Successfully connected to MySQL Server")
            
            # Create database if not exists
            mycursor.execute("CREATE DATABASE IF NOT EXISTS computer_sales_db")
            print("✓ Database 'computer_sales_db' created/verified")
            
            # Use the database
            mycursor.execute("USE computer_sales_db")
            
            # Create tables
            create_tables()
            
            return True
    except Error as e:
        print(f"\n✗ Error connecting to MySQL: {e}")
        return False

def create_tables():
    #Create all required tables for the system
    try:
        # Create COMPUTERS table
        
        que='''CREATE TABLE IF NOT EXISTS computers (
                computer_id INT PRIMARY KEY AUTO_INCREMENT,
                brand VARCHAR(50) NOT NULL,
                model VARCHAR(50) NOT NULL,
                processor VARCHAR(50),
                ram VARCHAR(20),
                storage VARCHAR(20),
                price DECIMAL(10, 2) NOT NULL,
                quantity INT DEFAULT 0'''
        
        
        mycursor.execute(que)
        print("✓ Table 'computers' created/verified")
        
        # Create CUSTOMERS table
        mycursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100) NOT NULL,
                phone VARCHAR(15),
                email VARCHAR(100),
                address VARCHAR(200)
            )
        ''')
        print("✓ Table 'customers' created/verified")
        
        # Create SALES table
        mycursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                sale_id INT PRIMARY KEY AUTO_INCREMENT,
                computer_id INT,
                customer_id INT,
                quantity INT NOT NULL,
                total_amount DECIMAL(10, 2) NOT NULL,
                sale_date DATE,
                FOREIGN KEY (computer_id) REFERENCES computers(computer_id),
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
            )
        ''')
        print("✓ Table 'sales' created/verified")
        
        # Create SERVICE_REQUESTS table
        mycursor.execute('''
            CREATE TABLE IF NOT EXISTS service_requests (
                service_id INT PRIMARY KEY AUTO_INCREMENT,
                customer_id INT,
                computer_brand VARCHAR(50),
                issue_description VARCHAR(500),
                status VARCHAR(20) DEFAULT 'Pending',
                service_date DATE,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
            )
        ''')
        print("✓ Table 'service_requests' created/verified")
        
        mydb.commit()  # Demonstrating commit()
        
    except Error as e:
        print(f"\n✗ Error creating tables: {e}")
        mydb.rollback()  # Demonstrating rollback()

# ==================== COMPUTER INVENTORY FUNCTIONS ====================

def add_computer():
    #Insert a new computer into inventory - Demonstrates INSERT and commit()
    print("\n" + "="*50)
    print("ADD NEW COMPUTER TO INVENTORY")
    print("\="*50)
    
    try:
        brand = input("Enter Brand: ")
        model = input("Enter Model: ")
        processor = input("Enter Processor: ")
        ram = input("Enter RAM (e.g., 8GB): ")
        storage = input("Enter Storage (e.g., 512GB SSD): ")
        price = float(input("Enter Price: "))
        quantity = int(input("Enter Quantity: "))
        
        # SQL INSERT command
        sql = '''INSERT INTO computers 
                 (brand, model, processor, ram, storage, price, quantity) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s)'''
        
        values = (brand, model, processor, ram, storage, price, quantity)
        
        mycursor.execute(sql, values)  # Demonstrating execute()
        mydb.commit()  # Demonstrating commit()
        
        print(f"\n✓ Computer added successfully! (ID: {mycursor.lastrowid})")
        print(f"✓ Rows affected: {mycursor.rowcount}")  # Demonstrating rowcount
        
    except Error as e:
        print(f"\n✗ Error adding computer: {e}")
        mydb.rollback()  # Demonstrating rollback()
    except ValueError:
        print("\n✗ Invalid input! Please enter correct data types.")

def view_all_computers():
    #Display all computers - Demonstrates SELECT and fetchall()
    print("\n" + "\="*50)
    print("ALL COMPUTERS IN INVENTORY")
    print("\="*50)
    
    try:
        # SQL SELECT command
        mycursor.execute("SELECT * FROM computers")
        
        computers = mycursor.fetchall()  # Demonstrating fetchall()
        
        if mycursor.rowcount == 0:  # Demonstrating rowcount
            print("\n✗ No computers found in inventory!")
            return
        
        print(f"\nTotal computers: {mycursor.rowcount}")
        print("\-" * 150)
        print(f"{'ID':<5} {'Brand':<15} {'Model':<20} {'Processor':<25} {'RAM':<10} {'Storage':<15} {'Price':<10} {'Qty':<5}")
        print("\-" * 150)
        
        for computer in computers:
            print(f"{computer[0]:<5} {computer[1]:<15} {computer[2]:<20} {computer[3]:<25} {computer[4]:<10} {computer[5]:<15} ₹{computer[6]:<9.2f} {computer[7]:<5}")
            
    except Error as e:
        print(f"\n✗ Error fetching computers: {e}")

def search_computer():
    #Search computer by brand - Demonstrates SELECT with WHERE and fetchall()
    print("\n" + "\="*50)
    print("SEARCH COMPUTER BY BRAND")
    print("\="*50)
    
    try:
        brand = input("Enter brand to search: ")
        
        # SQL SELECT with WHERE clause
        sql = "SELECT * FROM computers WHERE brand LIKE %s"
        mycursor.execute(sql, (f"%{brand}%",))
        
        computers = mycursor.fetchall()  # Demonstrating fetchall()
        
        if mycursor.rowcount == 0:
            print(f"\n✗ No computers found for brand '{brand}'")
            return
        
        print(f"\nFound {mycursor.rowcount} computer(s)")
        print("\-" * 150)
        print(f"{'ID':<5} {'Brand':<15} {'Model':<20} {'Processor':<25} {'RAM':<10} {'Storage':<15} {'Price':<10} {'Qty':<5}")
        print("\-" * 150)
        
        for computer in computers:
            print(f"{computer[0]:<5} {computer[1]:<15} {computer[2]:<20} {computer[3]:<25} {computer[4]:<10} {computer[5]:<15} ₹{computer[6]:<9.2f} {computer[7]:<5}")
            
    except Error as e:
        print(f"\n✗ Error searching computers: {e}")

def update_computer_price():
    #Update computer price - Demonstrates UPDATE and commit()
    print("\n" + "\="*50)
    print("UPDATE COMPUTER PRICE")
    print("\="*50)
    
    try:
        computer_id = int(input("Enter Computer ID to update: "))
        new_price = float(input("Enter new price: "))
        
        # SQL UPDATE command
        sql = "UPDATE computers SET price = %s WHERE computer_id = %s"
        mycursor.execute(sql, (new_price, computer_id))
        
        mydb.commit()  # Demonstrating commit()
        
        if mycursor.rowcount > 0:  # Demonstrating rowcount
            print(f"\n✓ Price updated successfully!")
            print(f"✓ Rows affected: {mycursor.rowcount}")
        else:
            print(f"\n✗ No computer found with ID {computer_id}")
            
    except Error as e:
        print(f"\n✗ Error updating price: {e}")
        mydb.rollback()  # Demonstrating rollback()
    except ValueError:
        print("\n✗ Invalid input!")

def delete_computer():
    #Delete computer from inventory - Demonstrates DELETE and commit()
    print("\n" + "\="*50)
    print("DELETE COMPUTER FROM INVENTORY")
    print("\="*50)
    
    try:
        computer_id = int(input("Enter Computer ID to delete: "))
        
        confirm = input(f"Are you sure you want to delete computer ID {computer_id}? (yes/no): ")
        
        if confirm.lower() == 'yes':
            # SQL DELETE command
            sql = "DELETE FROM computers WHERE computer_id = %s"
            mycursor.execute(sql, (computer_id,))
            
            mydb.commit()  # Demonstrating commit()
            
            if mycursor.rowcount > 0:  # Demonstrating rowcount
                print(f"\n✓ Computer deleted successfully!")
                print(f"✓ Rows affected: {mycursor.rowcount}")
            else:
                print(f"\n✗ No computer found with ID {computer_id}")
        else:
            print("\n✗ Deletion cancelled!")
            
    except Error as e:
        print(f"\n✗ Error deleting computer: {e}")
        mydb.rollback()  # Demonstrating rollback()
    except ValueError:
        print("\n✗ Invalid input!")

# ==================== CUSTOMER MANAGEMENT FUNCTIONS ====================

def add_customer():
    #Add new customer - Demonstrates INSERT and commit()
    print("\n" +"\="*50 )
    print("ADD NEW CUSTOMER")
    print("\="*50)
    
    try:
        name = input("Enter Customer Name: ")
        phone = input("Enter Phone Number: ")
        email = input("Enter Email: ")
        address = input("Enter Address: ")
        
        # SQL INSERT command
        sql = '''INSERT INTO customers (name, phone, email, address) 
                 VALUES (%s, %s, %s, %s)'''
        
        mycursor.execute(sql, (name, phone, email, address))
        mydb.commit()
        
        print(f"\n✓ Customer added successfully! (ID: {mycursor.lastrowid})")
        
    except Error as e:
        print(f"\n✗ Error adding customer: {e}")
        mydb.rollback()

def view_all_customers():
    #View all customers - Demonstrates SELECT and fetchall()
    print("\n" + "\="*50)
    print("ALL CUSTOMERS")
    print("\="*50)
    
    try:
        mycursor.execute("SELECT * FROM customers")
        customers = mycursor.fetchall()  # Demonstrating fetchall()
        
        if mycursor.rowcount == 0:
            print("\n✗ No customers found!")
            return
        
        print(f"\nTotal customers: {mycursor.rowcount}")
        print("\-" * 120)
        print(f"{'ID':<5} {'Name':<25} {'Phone':<15} {'Email':<30} {'Address':<40}")
        print("\-" * 120)
        
        for customer in customers:
            print(f"{customer[0]:<5} {customer[1]:<25} {customer[2]:<15} {customer[3]:<30} {customer[4]:<40}")
            
    except Error as e:
        print(f"\n✗ Error fetching customers: {e}")

# ==================== SALES MANAGEMENT FUNCTIONS ====================

def record_sale():
    #Record a new sale - Demonstrates INSERT, SELECT, UPDATE and transactions
    print("\n" + "\="*50)
    print("RECORD NEW SALE")
    print("\="*50)
    
    try:
        computer_id = int(input("Enter Computer ID: "))
        customer_id = int(input("Enter Customer ID: "))
        quantity = int(input("Enter Quantity: "))
        
        # First check if computer exists and has sufficient quantity
        sql_check = "SELECT price, quantity FROM computers WHERE computer_id = %s"
        mycursor.execute(sql_check, (computer_id,))
        
        result = mycursor.fetchone()  # Demonstrating fetchone()
        
        if result is None:
            print(f"\n✗ Computer with ID {computer_id} not found!")
            return
        
        price, available_qty = result
        
        if available_qty < quantity:
            print(f"\n✗ Insufficient quantity! Available: {available_qty}")
            return
        
        # Calculate total amount
        total_amount = price * quantity
        
        # Insert sale record
        sale_date = datetime.now().date()
        sql_sale ="INSERT INTO sales (computer_id, customer_id, quantity, total_amount, sale_date) VALUES (%s, %s, %s, %s, %s)"
        
        mycursor.execute(sql_sale, (computer_id, customer_id, quantity, total_amount, sale_date))
        
        # Update computer quantity
        sql_update = "UPDATE computers SET quantity = quantity - %s WHERE computer_id = %s"
        mycursor.execute(sql_update, (quantity, computer_id))
        
        mydb.commit()  # Commit transaction
        
        print(f"\n✓ Sale recorded successfully! (Sale ID: {mycursor.lastrowid})")
        print(f"✓ Total Amount: ₹{total_amount:.2f}")
        
    except Error as e:
        print(f"\n✗ Error recording sale: {e}")
        mydb.rollback()  # Rollback on error
    except ValueError:
        print("\n✗ Invalid input!")

def view_sales_history():
    #View all sales - Demonstrates SELECT with JOIN
    print("\n" + "\="*50)
    print("SALES HISTORY")
    print("\="*50)
    
    try:
        sql = '''SELECT s.sale_id, c.brand, c.model, cu.name, s.quantity, 
                 s.total_amount, s.sale_date
                 FROM sales s
                 JOIN computers c ON s.computer_id = c.computer_id
                 JOIN customers cu ON s.customer_id = cu.customer_id
                 ORDER BY s.sale_date DESC'''
        
        mycursor.execute(sql)
        sales = mycursor.fetchall()  # Demonstrating fetchall()
        
        if mycursor.rowcount == 0:
            print("\n✗ No sales records found")
            return
        
        print(f"\nTotal sales: {mycursor.rowcount}")
        print("\-" * 120)
        print(f"{'Sale ID':<10} {'Brand':<15} {'Model':<20} {'Customer':<25} {'Qty':<5} {'Amount':<12} {'Date':<12}")
        print("\-" * 120)
        
        for sale in sales:
            print(f"{sale[0]:<10} {sale[1]:<15} {sale[2]:<20} {sale[3]:<25} {sale[4]:<5} ₹{sale[5]:<11.2f} {sale[6]}")
            
    except Error as e:
        print(f"\n✗ Error fetching sales: {e}")

# ==================== SERVICE REQUEST FUNCTIONS ====================

def add_service_request():
    #Add service request - Demonstrates INSERT
    print("\n" + "\="*50)
    print("ADD SERVICE REQUEST")
    print("\="*50)
    
    try:
        customer_id = int(input("Enter Customer ID: "))
        computer_brand = input("Enter Computer Brand: ")
        issue = input("Enter Issue Description: ")
        
        service_date = datetime.now().date()
        
        sql = '''INSERT INTO service_requests 
                 (customer_id, computer_brand, issue_description, service_date)
                 VALUES (%s, %s, %s, %s)'''
        
        mycursor.execute(sql, (customer_id, computer_brand, issue, service_date))
        mydb.commit()
        
        print(f"\n✓ Service request added! (Request ID: {mycursor.lastrowid})")
        
    except Error as e:
        print(f"\n✗ Error adding service request: {e}")
        mydb.rollback()
    except ValueError:
        print("\n✗ Invalid input!")

def view_service_requests():
    #View all service requests - Demonstrates SELECT with JOIN
    print("\n" + "\="*50)
    print("SERVICE REQUESTS")
    print("\="*50)
    
    try:
        sql = '''SELECT sr.service_id, c.name, sr.computer_brand, 
                 sr.issue_description, sr.status, sr.service_date
                 FROM service_requests sr
                 JOIN customers c ON sr.customer_id = c.customer_id
                 ORDER BY sr.service_date DESC'''
        
        mycursor.execute(sql)
        requests = mycursor.fetchall()
        
        if mycursor.rowcount == 0:
            print("\n✗ No service requests found!")
            return
        
        print(f"\nTotal requests: {mycursor.rowcount}")
        print("\-" * 130)
        print(f"{'ID':<5} {'Customer':<25} {'Brand':<15} {'Issue':<35} {'Status':<12} {'Date':<12}")
        print("\-" * 130)
        
        for req in requests:
            issue_short = req[3][:32] + "\n" 
            if len(req[3]) > 35 :
                print(f"{req[0]:<5} {req[1]:<25} {req[2]:<15} {issue_short:<35} {req[4]:<12} {req[5]}")
            else:
                req[3]
    except Error as e:
        print(f"\n✗ Error fetching service requests: {e}")

def update_service_status():
    #Update service request status - Demonstrates UPDATE
    print("\n" + "\="*50)
    print("UPDATE SERVICE STATUS")
    print("\="*50)
    
    try:
        service_id = int(input("Enter Service Request ID: "))
        print("\nStatus Options: Pending, In Progress, Completed, Cancelled")
        new_status = input("Enter new status: ")
        
        sql = "UPDATE service_requests SET status = %s WHERE service_id = %s"
        mycursor.execute(sql, (new_status, service_id))
        
        mydb.commit()
        
        if mycursor.rowcount > 0:
            print(f"\n✓ Service status updated successfully!")
        else:
            print(f"\n✗ No service request found with ID {service_id}")
            
    except Error as e:
        print(f"\n✗ Error updating status: {e}")
        mydb.rollback()
    except ValueError:
        print("\n✗ Invalid input!")

# ==================== DEMONSTRATION FUNCTIONS ====================

def demonstrate_fetchmany():
    #Demonstrate fetchmany() method
    print("\n" + "\="*50)
    print("DEMONSTRATION: fetchmany() method")
    print("\="*50)
    
    try:
        n = int(input("How many records to fetch? "))
        
        mycursor.execute("SELECT * FROM computers")
        
        computers = mycursor.fetchmany(n)  # Demonstrating fetchmany()
        
        if len(computers) == 0:
            print("\n✗ No records found!")
            return
        
        print(f"\nFetched {len(computers)} record(s)")
        print("\-" * 100)
        
        for computer in computers:
            print(f"ID: {computer[0]}, Brand: {computer[1]}, Model: {computer[2]}, Price: ₹{computer[6]}")
            
    except Error as e:
        print(f"\n✗ Error: {e}")
    except ValueError:
        print("\n✗ Invalid input!")

def demonstrate_database_operations():
    #Demonstrate various database operations
    print("\n" + "\="*50)
    print("DEMONSTRATION: Database Operations")
    print("\="*50)
    
    try:
        # Show databases
        print("\n1. SHOW DATABASES:")
        mycursor.execute("SHOW DATABASES")
        databases = mycursor.fetchall()
        for db in databases:
            print(f"   - {db[0]}")
        
        # Show tables
        print("\n2. SHOW TABLES:")
        mycursor.execute("SHOW TABLES")
        tables = mycursor.fetchall()
        for table in tables:
            print(f"   - {table[0]}")
        
        # Describe table structure
        print("\n3. DESCRIBE 'computers' TABLE: ")
        mycursor.execute("DESC computers")
        columns = mycursor.fetchall()
        print("\-" * 80)
        print(f"{'Field':<20} {'Type':<20} {'Null':<10} {'Key':<10} {'Default':<10}")
        print("\-" * 80)
        for col in columns:
            print(f"{col[0]:<20} {col[1]:<20} {col[2]:<10} {col[3]:<10} {str(col[4]):<10}")
        
    except Error as e:
        print(f"\n✗ Error: {e}")

# ==================== MAIN MENU ====================

def display_menu():
    #Display main menu
    print("\n" + "\="*60)
    print(" \" * 15 + \"COMPUTER SALES AND SERVICE SYSTEM")
    print("\="*60)
    print("\n--- COMPUTER INVENTORY MANAGEMENT ---")
    print("1.  Add Computer to Inventory")
    print("2.  View All Computers")
    print("3.  Search Computer by Brand")
    print("4.  Update Computer Price")
    print("5.  Delete Computer")
    
    print("\n--- CUSTOMER MANAGEMENT ---")
    print("6.  Add Customer")
    print("7.  View All Cusomers")
    
    print("\n--- SALES MANAGEMENT ---")
    print("8.  Record Sale")
    print("9.  View Sales History")
    
    print("\n--- SERVICE MANAGEMENT ---")
    print("10. Add Service Request")
    print("11. View Service Requests")
    print("12. Update Service Status")
    
    print("\n--- DEMONSTRATIONS ---")
    print("13. Demonstrate fetchmany() method")
    print("14. Demonstrate Database Operations")
    
    print("\n15. Exit")
    print("\="*60)

def main():
    #Main function - Menu-driven program
    print("\n" + "*\="*60)
    print(" \" * 10 + \"COMPUTER SALES AND SERVICE SYSTEM")
    print(" \" * 15 + \"School CS Project - Python & MySQL")
    print("*\="*60)
    
    # Establish database connection
    if not create_connection():
        print("\nFailed to connect to database. Exiting...")
        return
    
    # Main program loop
    while True:
        try:
            display_menu()
            choice = input("\nEnter your choice (1-15): ")
            
            # Computer Inventory Operations
            if choice == '1':
                add_computer()
            elif choice == '2':
                view_all_computers()
            elif choice == '3':
                search_computer()
            elif choice == '4':
                update_computer_price()
            elif choice == '5':
                delete_computer()
            
            # Customer Management
            elif choice == '6':
                add_customer()
            elif choice == '7':
                view_all_customers()
            
            # Sales Management
            elif choice == '8':
                record_sale()
            elif choice == '9':
                view_sales_history()
            
            # Service Management
            elif choice == '10':
                add_service_request()
            elif choice == '11':
                view_service_requests()
            elif choice == '12':
                update_service_status()
            
            # Demonstrations
            elif choice == '13':
                demonstrate_fetchmany()
            elif choice == '14':
                demonstrate_database_operations()
            
            # Exit
            elif choice == '15':
                print("\n\" + \"\="*60)
                print("Thank you for using Computer Sales & Service System!")
                print("\="*60)
                break
            
            else:
                print("\n✗ Invalid choice! Please enter a number between 1-15.")
            
            # Pause before showing menu again
            input("\nPress Enter to continue...")
            
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user.")
            break
        except Exception as e:
            print(f"\n✗ Unexpected error: {e}")
    
    # Close database connection
        finally:
            if mycursor:
                mycursor.close()  # Demonstrating cursor.close()
            if mydb and mydb.is_connected():
                mydb.close()  # Demonstrating connection.close()
                print("✓ Database connection closed.")

# Run the program
if __name__ == "__main__":
    main()

