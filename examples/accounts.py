from vivialconnect import Account


def billing_status(account_id=None):
    status = Account.billing_status(account_id=account_id)
    return status


def update_account(id, company_name=None):
    account = Account.find(id)
    account.company_name = company_name
    account.save()
    return account


def get_account(id):
    account = Account.find(id)
    return account
