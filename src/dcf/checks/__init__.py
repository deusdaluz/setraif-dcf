import device
import localization
import value

check_modules = (device, value, localization)


def is_fraud(transacao, conta):
    for check_module in check_modules:
        if check_module.is_fraud(transacao, conta):
            return True

    return False


def learn(transacao, conta):
    for check_module in check_modules:
        check_module.learn(transacao, conta)
