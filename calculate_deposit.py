from datetime import date, timedelta
from calendar import monthrange

from dto import PostDepositInput, PostDepositOutput, DepositPeriod


def calculate_deposit(input_vector: PostDepositInput) -> PostDepositOutput:
    amount, periods, date_ = input_vector.amount, [], input_vector.date_

    for period in range(input_vector.periods):
        periods.append(DepositPeriod(amount=amount, date=date_))
        amount = round(amount * (1 + input_vector.rate / 12 / 100), 2)
        date_ += timedelta(
            days=monthrange(
                year=date_.year,
                month=date_.month + 1 if date_.month <= 11 else date_.month - 11
            )[1]
        )

    return PostDepositOutput(period=periods)
