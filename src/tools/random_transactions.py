import csv
import random
from datetime import datetime, timedelta
from collections import defaultdict

random.seed()

CATEGORIES = {
    "Housing": 615.0,
    "Transportation": 600.0,
    "Food": 2000.0,
    "Healthcare": 400.0,
    "Debt Payments": 500.0,
    "Investments": 6000.0,
    "Entertainment & Leisure": 2000.0,
    "Personal Care": 400.0,
    "Education": 500.0,
    "Miscellaneous": 900.0
}

CATEGORY_DESCRIPTIONS_TR = {
    "Housing": ["Yurt", "Kira", "Aidat"],
    "Transportation": ["Otobüs bileti", "Taksi", "Metro kart dolumu"],
    "Food": ["Market alışverişi", "Restoran", "Kafede yemek"],
    "Healthcare": ["Reçete", "Doktor muayenesi", "Eczane"],
    "Debt Payments": ["Kredi taksidi", "Borç ödemesi"],
    "Investments": ["Hisse senedi alımı", "Fon yatırımı"],
    "Entertainment & Leisure": ["Sinema", "Tiyatro", "Kitap alımı"],
    "Personal Care": ["Berber", "Kozmetik", "Cilt bakımı"],
    "Education": ["Kitap", "Kurs ücreti", "Sertifika programı"],
    "Miscellaneous": ["Hediye", "Ofis malzemesi", "A101 fişi"]
}

USER_ID = 1
YEAR = 2025
DAYS_IN_MONTH = 30

TOTAL_MONTHLY_BUDGET = sum(CATEGORIES.values())
DAILY_BUDGET_AVG = TOTAL_MONTHLY_BUDGET / DAYS_IN_MONTH
DAILY_MIN = DAILY_BUDGET_AVG - 300
DAILY_MAX = DAILY_BUDGET_AVG + 300
MONTHLY_MIN = DAILY_MIN * DAYS_IN_MONTH
MONTHLY_MAX = TOTAL_MONTHLY_BUDGET + 4000


def generate_random_date(month):
    """
    Generate a random datetime within the given month of YEAR.
    """
    start = datetime(YEAR, month, 1)
    end = start + timedelta(days=DAYS_IN_MONTH) - timedelta(seconds=1)
    delta = end - start
    random_offset = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_offset)


def generate_transactions():
    transactions = []
    transaction_id = 0

    for month in range(1, 13):
        monthly_total = 0.0
        category_spent = defaultdict(float)
        attempts = 0

        while (len([t for t in transactions if datetime.strptime(t[2], '%Y-%m-%d %H:%M:%S').month == month]) < 30
               or monthly_total < MONTHLY_MIN) and attempts < 2000:
            attempts += 1

            cat = random.choice(list(CATEGORIES.keys()))
            remaining_cat = CATEGORIES[cat] - category_spent[cat]
            if remaining_cat <= 0:
                continue

            max_amount = min(remaining_cat, MONTHLY_MAX - monthly_total)
            if max_amount < 1:
                continue
            amount = round(random.uniform(1, max_amount), 2)

            dt = generate_random_date(month).strftime('%Y-%m-%d %H:%M:%S')
            desc = random.choice(CATEGORY_DESCRIPTIONS_TR[cat])

            transactions.append([
                transaction_id,
                USER_ID,
                dt,
                cat,
                amount,
                desc
            ])
            transaction_id += 1
            monthly_total += amount
            category_spent[cat] += amount

        if monthly_total > MONTHLY_MAX:
            print(f"Warning: Month {month} total {monthly_total} exceeds budget {MONTHLY_MAX}")

    return transactions


def write_to_csv(transactions, filename='transactions.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['transactionid', 'userid', 'date', 'categoryname', 'amount', 'description'])
        writer.writerows(transactions)


if __name__ == '__main__':
    txs = generate_transactions()
    write_to_csv(txs)
    print(f"{len(txs)} transactions written to '{'transactions.csv'}'")