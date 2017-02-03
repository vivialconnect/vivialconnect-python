from vivialconnect import Account


def billing_status(account_id=None):
    status = Account.billing_status(account_id=account_id)
    print(status)


def list_subaccounts():
    subaccounts = Account.subaccounts()
    for subaccount in subaccounts:
        print(subaccount.__dict__)


def update_account(id, company_name=None):
    account = Account.find(id)
    account.company_name = company_name
    account.save()


def get_account(id):
    account = Account.find(id)
    print(account.id, account.company_name)


def create_subaccount(company_name=None):
    account = Account()
    account.company_name = company_name
    account.save()
    print(account.id, account.company_name)


def delete_subaccount(id):
    # Currently requires administrator role
    account = Account.find(id)
    account.destroy()
    print(account.id, account.company_name)
