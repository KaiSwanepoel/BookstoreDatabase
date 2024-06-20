import sqlite3

# Connect to database and create cursor
db = sqlite3.connect('bookstore.db')
cursor = db.cursor()

# Create table
cursor.execute('''CREATE TABLE IF NOT EXISTS book_table (
               id INT PRIMARY KEY,
               title TEXT,
               author TEXT,
               quantity INT )''')

# Populate table with books and their information
new_rows = [
    (3001, "A Tale of Two Cities", "Charles Dickens", 30),
    (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
    (3003, "The Lion, the Witch and the Wardrobe", "C.S. Lewis", 25),
    (3004, "The Lord of the Rings", "J.R.R Tolkien", 37),
    (3005, "Alice in Wonderland", "Lewis Carroll", 12)
]

# insert the books into the table and commit the database
cursor.executemany("INSERT INTO book_table (id, title, author, quantity) VALUES (?, ?, ?, ?)", new_rows)

db.commit()

# Create function to enter new book into database using try except to stop possible errors
def enter_book():
    while True:
        try:
            id = int(input("Enter the ID number of the new book?: "))
        except ValueError:
            print("\nPlease enter a valid number.")
            continue
        title = input("What is the title of the book?: ")
        author = input("Who is the author of the book?: ")
        try:
            quantity = int(input("How many copies are there?: "))
        except ValueError:
            print("\nPlease enter a valid number.")
            continue
        try:
            cursor.execute("INSERT INTO book_table (id, title, author, quantity) VALUES (?, ?, ?, ?)", (id, title, author, quantity))
            db.commit()
            print("The book has been entered into the database!")
            break
        except sqlite3.IntegrityError:
            print("\nThe book ID is already in use please enter a unique ID!")
    
# Create function to update quantity of books in the database
def update_book():
    while True:
        try:
            id = int(input("Enter the book ID to update: "))
        except ValueError:
            print("Please enter a valid number!")
            continue
        try:
            updated_quantity = int(input("Enter the new quantity of the book: "))
        except ValueError:
            print("Please enter a valid number.")
            continue
    
        cursor.execute("UPDATE book_table SET quantity = ? WHERE id = ?", (updated_quantity, id))
        db.commit()
        print("The book quantity has been updated!")
        break

# Create function to delete a book from the database
def delete_book():
    while True:
        try:
            id = int(input("Enter the book ID to delete: "))
            break
        except ValueError:
            print("Please enter a valid number!")
            continue
    
    cursor.execute("DELETE FROM book_table WHERE id = ?", (id,))
    db.commit()
    print("The book has been deleted from the database!")

# Create a function to search for a book
def search_book():
    title = input("Enter book title to search: ")
    
    cursor.execute("SELECT * FROM book_table WHERE title LIKE ?", ('%' + title + '%',))
    books = cursor.fetchall()
    
    if not books:
        print("There are no books by that title.")
    else:
        for book in books:
            print(f'''ID: {book[0]}
Title: {book[1]}
Author: {book[2]}
Quantity: {book[3]}''')

# Display options menu
while True:
    print("\nMenu:")
    print('''1 - Enter book
2 - Update book
3 - Delete book
4 - Search book
0 - Exit''')

# Create menu that links to various functions
    menu = input("What would you like to do?: ")
    
    if menu == '1':
        enter_book()
    elif menu == '2':
        update_book()
    elif menu == '3':
        delete_book()
    elif menu == '4':
        search_book()
    elif menu == '0':
        break
    else:
        print("Your number is invalid please try again!")

# Close Database
db.close()
