import sqlite3

def create_tables():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Authors (
            author_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author_id INTEGER,
            read_before TEXT,
            num_pages INTEGER,
            FOREIGN KEY (author_id) REFERENCES Authors(author_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_author(name):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Authors (name) VALUES (?)', (name,))
    author_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return author_id

def add_book(title, author_name, read_before, num_pages):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT author_id FROM Authors WHERE name = ?', (author_name,))
    author = cursor.fetchone()
    
    if author is None:
        author_id = add_author(author_name)
    else:
        author_id = author[0]
    
    cursor.execute('''
        INSERT INTO Books (title, author_id, read_before, num_pages)
        VALUES (?, ?, ?, ?)
    ''', (title, author_id, read_before, num_pages))
    
    conn.commit()
    conn.close()

def lookup_books(keyword):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT Books.title, Authors.name, Books.read_before, Books.num_pages
        FROM Books
        JOIN Authors ON Books.author_id = Authors.author_id
        WHERE Books.title LIKE ? OR Authors.name LIKE ?
    ''', ('%' + keyword + '%', '%' + keyword + '%'))
    books = cursor.fetchall()
    conn.close()
    return books

def display_books():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT Books.title, Authors.name, Books.read_before, Books.num_pages
        FROM Books
        JOIN Authors ON Books.author_id = Authors.author_id
    ''')
    books = cursor.fetchall()
    conn.close()
    return books

def main():
    create_tables()
    
    choice = 0
    while choice != 4:
        print("* Books Manager *")
        print("1) Add a book")
        print("2) Lookup a book")
        print("3) Display books")
        print("4) Quit")
        choice = int(input())
        
        if choice == 1:
            print("Adding a book...")
            nBook = input("Enter the name of the book >>> ")
            nAuthor = input("Enter the name of the author >>> ")
            rBefore = input("Have you read it before? >>> ")
            nPages = input("Enter the number of pages >>> ")
            add_book(nBook, nAuthor, rBefore, nPages)
        
        elif choice == 2:
            print("Looking up for a book...")
            keyword = input("Enter Search Term: ")
            books = lookup_books(keyword)
            for book in books:
                print(book)
        
        elif choice == 3:
            print("Displaying all books...")
            books = display_books()
            for book in books:
                print(book)
        
        elif choice == 4:
            print("Quitting Program")
    
    print("Program Terminated!")

if __name__ == "__main__":
    main()