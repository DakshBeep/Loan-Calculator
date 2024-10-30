import math
import argparse
import sys

class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print("Incorrect parameters")
        sys.exit(1)

def calculate_diff_payment(principal, periods, interest, month):
    p = principal
    n = periods
    i = interest
    m = month
    d = p / n + i * (p - (p * (m - 1)) / n)
    return math.ceil(d)

def calculate_diff_payments(principal, periods, interest):
    total_payment = 0
    for m in range(1, periods + 1):
        payment = calculate_diff_payment(principal, periods, interest, m)
        total_payment += payment
        print(f"Month {m}: payment is {payment}")
    overpayment = total_payment - principal
    print(f"\nOverpayment = {overpayment}")

def calculate_annuity_payment(principal, periods, interest):
    payment = math.ceil(
        principal * (interest * pow(1 + interest, periods)) / (pow(1 + interest, periods) - 1)
    )
    print(f"Your annuity payment = {payment}!")
    overpayment = payment * periods - principal
    print(f"Overpayment = {overpayment}")

def calculate_loan_principal(payment, periods, interest):
    principal = payment / ((interest * pow(1 + interest, periods)) / (pow(1 + interest, periods) - 1))
    principal = math.floor(principal)
    print(f"Your loan principal = {principal}!")
    overpayment = payment * periods - principal
    print(f"Overpayment = {overpayment}")

def calculate_loan_periods(principal, payment, interest):
    periods = math.ceil(math.log(payment / (payment - interest * principal), 1 + interest))
    years = periods // 12
    months = periods % 12
    
    if years == 0:
        print(f"It will take {months} months to repay this loan!")
    elif months == 0:
        print(f"It will take {years} years to repay this loan!")
    else:
        print(f"It will take {years} years and {months} months to repay this loan!")
    
    overpayment = payment * periods - principal
    print(f"Overpayment = {overpayment}")

def validate_args(args):
    if args.type not in ["annuity", "diff"]:
        return False
    
    if args.type == "diff" and args.payment is not None:
        return False
    
    if args.interest is None:
        return False
    
    provided_args = sum(1 for arg in [args.principal, args.periods, args.payment] if arg is not None)
    if provided_args < 2:
        return False
    
    if any(float(arg) < 0 for arg in [args.principal, args.periods, args.payment, args.interest] 
           if arg is not None):
        return False
    
    return True

def main():
    parser = CustomArgumentParser()
    parser.add_argument("--type", choices=["annuity", "diff"])
    parser.add_argument("--payment", type=float)
    parser.add_argument("--principal", type=float)
    parser.add_argument("--periods", type=int)
    parser.add_argument("--interest", type=float)
    
    args = parser.parse_args()
    
    if not validate_args(args):
        print("Incorrect parameters")
        sys.exit(1)
    
    interest = float(args.interest) / (12 * 100)  # concert to monthly interest
    
    if args.type == "diff":
        calculate_diff_payments(args.principal, args.periods, interest)
    else:  # annuity
        if args.payment is None:
            calculate_annuity_payment(args.principal, args.periods, interest)
        elif args.periods is None:
            calculate_loan_periods(args.principal, args.payment, interest)
        elif args.principal is None:
            calculate_loan_principal(args.payment, args.periods, interest)

if __name__ == "__main__":
    main()
