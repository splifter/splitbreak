import csv
import os
import argparse
from splitwise import Splitwise
from splitwise.expense import Expense, ExpenseUser
from dotenv import load_dotenv


# Funktion zum Laden der Umgebungsvariablen oder Überschreiben durch CLI-Argumente
def load_config_from_env_or_cli(args):
    config = {
        "CONSUMER_KEY": os.getenv("CONSUMER_KEY") if not args.consumer_key else args.consumer_key,
        "CONSUMER_SECRET": os.getenv("CONSUMER_SECRET") if not args.consumer_secret else args.consumer_secret,
        "API_KEY": os.getenv("API_KEY") if not args.api_key else args.api_key,
        "GROUP_ID": os.getenv("GROUP_ID") if not args.group_id else args.group_id,
    }
    # Für jeden Benutzer die ID und den Anteil hinzufügen
    config["USERS"] = {args.user_ids[i]: float(args.user_shares[i]) for i in range(len(args.user_ids))}
    return config


# Hauptfunktion für die Verarbeitung von Ausgaben
def process_expenses(csv_file, config):
    sObj = Splitwise(config["CONSUMER_KEY"], config["CONSUMER_SECRET"], api_key=config["API_KEY"])

    with open(csv_file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            description = row['description']
            date = row['date']
            cost = float(row['cost'])
            print(f"Processing expense: {description}, on {date} with cost {cost}")
            # Erstellen und Einreichen des Expense-Objekts
            expense = create_expense(cost, description, date, config)
            nExpense, errors = sObj.createExpense(expense=expense)
            if errors:
                # Verbesserte Fehlerausgabe
                print(f"errors: {str(errors)}")
                continue
            if nExpense:
                print(f"Expense ID: {nExpense.getId()}")

def adjust_cost_and_shares(cost, user_shares):
    total_share = sum(user_shares.values())
    owed_shares = {user_id: round(cost * (share / total_share), 2) for user_id, share in user_shares.items()}
    sum_owed_shares = sum(owed_shares.values())

    # Runden, um Ungenauigkeiten im Floating-Point zu vermeiden
    cost_rounded = round(cost, 2)
    sum_owed_shares = round(sum_owed_shares, 2)

    # Überprüfe, ob die Summe der owed_shares gleich cost ist, sonst erhöhe die Gesamtkosten um einen Cent
    if sum_owed_shares != cost_rounded:
        # Kosten um einen Cent erhöhen
        cost_rounded += 0.01
        # Nach der Kostenkorrektur, erneut owed_shares berechnen
        owed_shares = {user_id: round(cost_rounded * (share / total_share), 2) for user_id, share in user_shares.items()}

    return cost_rounded, owed_shares

# Funktion zum Erstellen des Expense-Objekts basierend auf den Benutzerdaten
def create_expense(cost, description, date, config):
    # Hier wird adjust_cost_and_shares aufgerufen, um cost und owed_shares anzupassen
    adjusted_cost, owed_shares = adjust_cost_and_shares(cost, config["USERS"])

    expense = Expense()
    expense.setCost(str(round(adjusted_cost, 2)))
    expense.setDescription(description)
    expense.setDate(date)
    expense.setGroupId(config["GROUP_ID"])

    for user_id, owed_share in owed_shares.items():
        user = ExpenseUser()
        user.setId(int(user_id))
        user.setOwedShare(str(owed_share))
        # Füge dies hinzu, um z.B. den paidShare für den ersten User zu setzen
        if user_id == list(owed_shares.keys())[0]:
            user.setPaidShare(str(round(adjusted_cost, 2)))
        expense.addUser(user)

    return expense


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Creates expenses from a CSV file with user contributions.")
    parser.add_argument('--csv', required=True, help='Path to the CSV file containing expenses.')
    parser.add_argument('--user_ids', nargs='+', required=True, help='User IDs.')
    parser.add_argument('--user_shares', nargs='+', required=True, help='Shares of each user.')
    parser.add_argument('--consumer_key', help='Splitwise Consumer Key')
    parser.add_argument('--consumer_secret', help='Splitwise Consumer Secret')
    parser.add_argument('--api_key', help='API Key for Splitwise')
    parser.add_argument('--group_id', help='Group ID for the expense.')

    args = parser.parse_args()

    # Umgebungsvariablen laden, falls vorhanden
    load_dotenv()

    # Konfiguration aus den Kommandozeilenargumenten oder .env Datei laden
    config = load_config_from_env_or_cli(args)

    process_expenses(args.csv, config)