from datetime import timedelta
from calendar import monthrange
from decimal import Decimal, ROUND_HALF_UP

from dateutil.relativedelta import relativedelta

from dto import PostDepositInput, PostDepositOutput, DepositPeriod


def calculate_deposit(input_vector: PostDepositInput) -> PostDepositOutput:
    amount, periods = input_vector.amount, []

    for period in range(input_vector.periods):
        amount = amount * (1 + input_vector.rate / 12 / 100)
        periods.append(
            DepositPeriod(
                amount=Decimal(amount).quantize(Decimal('1.00'), ROUND_HALF_UP),
                date=input_vector.date_ + relativedelta(months=1 * period)
            )
        )

    return PostDepositOutput(period=periods)
