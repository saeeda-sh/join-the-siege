import random
from datetime import timedelta
from faker import Faker

fake = Faker()


def generate_invoice_text():
    company_name = fake.company()
    company_address = fake.address().replace("\n", ", ")
    invoice_number = fake.uuid4()[:8]
    invoice_date = fake.date_this_year()

    invoice = f"Invoice: {invoice_number}\nCompany: {company_name}\nAddress: {company_address}\nDate: {invoice_date}\n\n"
    invoice += "Items:\n"

    # Random items (name, quantity, price)
    total_amount = 0
    for _ in range(random.randint(3, 8)):
        item_name = fake.word().capitalize()
        quantity = random.randint(1, 10)
        price = round(random.uniform(5, 200), 2)
        item_total = round(quantity * price, 2)

        invoice += (
            f"{item_name} (Qty: {quantity}) - ${price} each - Total: ${item_total}\n"
        )
        total_amount += item_total

    invoice += f"\nTotal Amount Due: ${round(total_amount, 2)}\n"

    return invoice


def generate_bank_statement_text():
    account_holder = fake.name()
    account_number = fake.bban()
    statement_date = fake.date_this_year()

    statement = f"Bank Statement\nAccount Holder: {account_holder}\nAccount Number: {account_number}\nDate: {statement_date}\n\n"
    statement += "Transactions:\n"

    # Random no. of transactions
    for _ in range(random.randint(5, 15)):
        transaction_date = fake.date_this_month()
        description = fake.company()
        amount = round(random.uniform(5, 500), 2)
        balance = round(random.uniform(0, 10000), 2)

        transaction = f"{transaction_date} | {description} | Amount: ${amount} | Balance: ${balance}\n"
        statement += transaction

    return statement


def generate_license_text():
    first_name = fake.first_name()
    last_name = fake.last_name()
    full_name = f"{first_name} {last_name}"
    address = fake.address().replace("\n", ", ")
    license_number = fake.bothify(text="??-########")
    date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=90)
    issue_date = fake.date_this_decade()
    expiry_date = issue_date + timedelta(days=random.randint(3650, 7300))
    gender = random.choice(["M", "F"])

    # Convert dates to string
    date_of_birth_str = date_of_birth.strftime("%Y-%m-%d")
    issue_date_str = issue_date.strftime("%Y-%m-%d")
    expiry_date_str = expiry_date.strftime("%Y-%m-%d")

    # Generate the driver's license string
    license = f"Driver's License\nName: {full_name}\nDate of Birth: {date_of_birth_str}\nGender: {gender}\n"
    license += f"Address: {address}\nLicense Number: {license_number}\nIssue Date: {issue_date_str}\n"
    license += f"Expiry Date: {expiry_date_str}\n"

    return license
