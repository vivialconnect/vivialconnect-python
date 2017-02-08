from vivialconnect import Account


def billing_status(account_id=None):
    status = Account.billing_status(account_id=account_id)
    return status


def list_subaccounts():
    subaccounts = Account.subaccounts()
    for subaccount in subaccounts:
        yield subaccount


def update_account(id, company_name=None):
    account = Account.find(id)
    account.company_name = company_name
    account.save()
    return account


def get_account(id):
    account = Account.find(id)
    return account


def create_subaccount(company_name=None):
    account = Account()
    account.company_name = company_name
    account.save()
    return account


def delete_subaccount(id):
    # Currently requires administrator role
    account = Account.find(id)
    account.destroy()
    return True
