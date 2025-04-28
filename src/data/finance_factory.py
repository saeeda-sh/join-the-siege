from .data_factory import SyntheticDataFactory
from .generators import (
    generate_invoice_text,
    generate_bank_statement_text,
    generate_license_text,
)

# Using class method to register the industry and its generators
SyntheticDataFactory.register_industry(
    "finance",
    {
        "invoice": generate_invoice_text,
        "bank_statement": generate_bank_statement_text,
        "drivers_license": generate_license_text,
    },
)

SyntheticDataFactory.register_industry(
    "government",
    {
        "drivers_license": generate_license_text,
    },
)
