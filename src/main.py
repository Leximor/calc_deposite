import calendar
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Dict
from dateutil.relativedelta import relativedelta

app = FastAPI()


class DepositRequest(BaseModel):
    date: str = Field(...)
    periods: int = Field(..., ge=1, le=60)
    amount: int = Field(..., ge=10000, le=3000000)
    rate: float = Field(..., ge=1, le=8)

    @field_validator('date')
    def validate_date(cls, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError('Неверный формат даты, должен быть dd.mm.YYYY')
        return value


def calculate_deposit(date: str,
                      periods: int,
                      amount: int,
                      rate: float) -> Dict[str, float]:
    results = {}
    current_date = datetime.strptime(date, "%d.%m.%Y")
    current_amount = amount
    start_day = current_date.day

    for _ in range(periods):
        current_amount *= (1 + rate / 12 / 100)

        next_date = current_date + relativedelta(months=1)
        last_day_of_next_month = calendar.monthrange(next_date.year,
                                                     next_date.month)[1]
        if start_day > last_day_of_next_month:
            next_date = next_date.replace(day=last_day_of_next_month)
        else:
            next_date = next_date.replace(day=start_day)

        results[next_date.strftime("%d.%m.%Y")] = round(current_amount, 2)
        current_date = next_date

    return results


@app.post("/calculate", response_model=Dict[str, float])
def calculate_deposit_endpoint(deposit: DepositRequest):
    try:
        result = calculate_deposit(deposit.date,
                                   deposit.periods,
                                   deposit.amount,
                                   deposit.rate)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
