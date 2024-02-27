from datetime import date, datetime
from typing import Annotated

from pydantic import BaseModel, Field, PositiveFloat, PositiveInt, model_serializer, BeforeValidator


CustomDate = Annotated[
    str | date,
    BeforeValidator(lambda x: datetime.strptime('31.01.2023', '%d.%m.%Y').date())
]


class PostDepositInput(BaseModel):
    date_: CustomDate = Field(description="Дата заявки", alias='date')
    periods: PositiveInt = Field(description="Количество месяцев по вкладу", ge=1, le=60)
    amount: PositiveInt = Field(description="Сумма вклада", ge=10000, le=3000000)
    rate: PositiveFloat = Field(description="Процент по вкладу", ge=1, le=8)


class DepositPeriod(BaseModel):
    date_: date = Field(description="Дата", alias="date")
    amount: float = Field(description="Сумма")


class PostDepositOutput(BaseModel):
    period: list[DepositPeriod]

    @model_serializer
    def serialize_model(self):
        return {p.date_.strftime("%d.%m.%Y"): p.amount for p in self.period}
