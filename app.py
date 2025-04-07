from models import Base, session, Product, engine
import datetime
import csv
import time


def menu():
    while True:
        print('''
            \nSTORE INVENTORY
            \r(V)iew Product Details
            \r(A)dd a New Product
            \r(B)ackup Database
            \r(E)xit\n''')
        choice = input('What would you like to do?  >')
        if choice in ['V', 'A', 'B', 'E', 'e', 'v', 'a', 'b']:
            return choice
        else:
            input('''
            \nThat selection was not a valid selection.
            \rPlease enter a letter corresponding to one of the choices given above
            \r(The letter in parenthesis)\n
            \rPress enter to try again''')

def clean_date(date_str):
    try:
        split_date = date_str.split('/')
        month = int(split_date[0])
        day = int(split_date[1])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except ValueError:
        input('''
            \n******* DATE ERROR *******
            \rThat date is not valid
            \rThe date must ba a date that exists in the past, and must be in the following format: MM/DD/YYY
            \rPress Enter to try again.
            \r**************************''')
        return
    else:
        return return_date
        



def clean_price(price_str):
    dollarsign = '$'
    if dollarsign in price_str:
        sans_dollarsign = price_str.replace(dollarsign, '')
        price_str = sans_dollarsign
    price_float = float(price_str)
    return int(price_float * 100)


def clean_quantity(quantity_str):
    return int(quantity_str)

def clean_id(id_str, options):
    try:
        product_id = int(id_str)
    except ValueError:
        input('''
            \n****** ID ERROR******
            \rThe id should be a number.
            \rPress enter to try again.
            \r***********************''')
        return
    else:
        if product_id in options:
            return product_id
        else:
            input(f'''
                \n****** ID ERROR******
                \rThe ID you entered was not valid.
                \rPress enter to try again.
                \r***********************''')
            return


def add_csv():
    with open('store-inventory\inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        next(data)
        for row in data:
            product_in_db = session.query(Product).filter(Product.product_name==row[0]).one_or_none()
            if product_in_db == None:
                product_name = row[0]
                product_price = clean_price(row[1])
                product_quantity = clean_quantity(row[2])
                date_updated = clean_date(row[3])
                new_product = Product(product_name = product_name, product_price = product_price, product_quantity = product_quantity, date_updated = date_updated)
                session.add(new_product)
        session.commit()


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice.lower() == 'v':
            id_options = []
            for product in session.query(Product):
                id_options.append(product.product_id)
            id_error = True
            while id_error:
                id_choice = input(f'''
                    \nID Options: {id_options}
                    \nProduct id: ''')
                id_choice = clean_id(id_choice, id_options)
                if type(id_choice) == int:
                    id_error = False
            the_product = session.query(Product).filter(Product.product_id==id_choice).first()
            print(f'''
                \nPRODUCT DETAILS
                \rProduct name: {the_product.product_name}
                \rProduct Price: ${the_product.product_price / 100}
                \rQuantity: {the_product.product_quantity}
                \rDate Updated: {the_product.date_updated}\n''')
        elif choice.lower() == 'a':
            # add new
            product_name = input('Product name: ')
            price_error = True
            while price_error:
                product_price = input('Product price (Ex: 7.99): ')
                product_price = clean_price(product_price)
                if type(product_price) == int:
                    price_error = False
            product_quantity = input('Product quantity: ')
            date_error = True
            while date_error:
                date_updated = input('Date (Ex: MM/DD/YYYY): ')
                date_updated = clean_date(date_updated)
                if type(date_updated) == datetime.date:
                    date_error = False
            for product in session.query(Product):
                if product.product_name == product_name:
                    product_update = product
                    new_product = False
                    print('new product is False')
                else:
                    new_product = True

            if new_product == True:
                print('new product is True')
                new_product_addition = Product(product_name = product_name, product_price = product_price, product_quantity = product_quantity, date_updated = date_updated)
                session.add(new_product_addition)                
                session.commit()
                print('Product Added')
            else:
                print('Old product is being updated')
                product_update.product_price = product_price
                product_update.product_quantity = product_quantity
                product_update.date_updated = date_updated
                session.commit()
                print('Product Has been Updated')

            time.sleep(1.5)

        elif choice.lower() == 'b':
            # backup db
            current_product_data = session.query(Product)
            with open('backup.csv', 'w', newline='') as csvfile:
                fieldnames = ['product_name','product_price','product_quantity','date_updated']
                teachwriter = csv.DictWriter(csvfile, fieldnames = fieldnames)

                teachwriter.writeheader()
                for product in current_product_data:
                    teachwriter.writerow({
                            'product_name': product.product_name,
                            'product_price': product.product_price,
                            'product_quantity': product.product_quantity,
                            'date_updated': product.date_updated
                        })
                
            print('Backup Created')
        else:
            # exit
            print('GOODBYE')
            app_running = False




if __name__ == '__main__':
    Base.metadata.create_all(engine) # Creating the datbase

    add_csv()
    app()
        
    #for product in session.query(Product):
        #print(product)
    #for product in session.query(Product.product_name):
        #print(product)
    
    

