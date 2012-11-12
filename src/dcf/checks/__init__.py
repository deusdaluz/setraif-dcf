import dcf.checks.device as device
import dcf.checks.localization as localization
import dcf.checks.value as value

check_modules = (device, value, localization)


def is_fraud(transacao, conta):
    for check_module in check_modules:
        if check_module.is_fraud(transacao, conta):
            return False

    for check_module in check_modules:
        check_module.learn(transacao, conta)
    return True
