import random

import pandas as pd
from faker import Faker


def get_players():
    """
    A function that returns the details of a team's full squad,
    combining both faker and given data together.

    Args:
        None
    Return:
        The dataframe of the players information
    """
    full_squad = [
        {"Player": "Alisson Becker", "Position": "Goalkeeper",
         "Jersey Number": 1},
        {"Player": "Giorgi Mamardashvili", "Position": "Goalkeeper",
         "Jersey Number": 13},
        {"Player": "Ármin Pécsi", "Position": "Goalkeeper",
         "Jersey Number": 31},
        {"Player": "Freddie Woodman", "Position": "Goalkeeper",
         "Jersey Number": 22},
        {"Player": "Joe Gomez", "Position": "Defender", "Jersey Number": 2},
        {"Player": "Virgil van Dijk", "Position": "Defender",
         "Jersey Number": 4},
        {"Player": "Ibrahima Konaté", "Position": "Defender",
         "Jersey Number": 5},
        {"Player": "Kostas Tsimikas", "Position": "Defender",
         "Jersey Number": 21},
        {"Player": "Calvin Ramsay", "Position": "Defender",
         "Jersey Number": 22},
        {"Player": "Andy Robertson", "Position": "Defender",
         "Jersey Number": 26},
        {"Player": "Rhys Williams", "Position": "Defender",
         "Jersey Number": 46},
        {"Player": "Conor Bradley", "Position": "Defender",
         "Jersey Number": 84},
        {"Player": "Jeremie Frimpong", "Position": "Defender",
         "Jersey Number": 20},
        {"Player": "Milos Kerkez", "Position": "Defender",
         "Jersey Number": 3},
        {"Player": "Florian Wirtz", "Position": "Midfielder",
         "Jersey Number": 10},
        {"Player": "Wataru Endo", "Position": "Midfielder",
         "Jersey Number": 3},
        {"Player": "Dominik Szoboszlai", "Position": "Midfielder",
         "Jersey Number": 8},
        {"Player": "Alexis Mac Allister", "Position": "Midfielder",
         "Jersey Number": 10},
        {"Player": "Curtis Jones", "Position": "Midfielder",
         "Jersey Number": 17},
        {"Player": "Harvey Elliott", "Position": "Midfielder",
         "Jersey Number": 19},
        {"Player": "Ryan Gravenberch", "Position": "Midfielder",
         "Jersey Number": 38},
        {"Player": "Stefan Bajcetic", "Position": "Midfielder",
         "Jersey Number": 43},
        {"Player": "James McConnell", "Position": "Midfielder",
         "Jersey Number": 53},
        {"Player": "Tyler Morton", "Position": "Midfielder",
         "Jersey Number": 80},
        {"Player": "Treymaurice Nyoni", "Position": "Midfielder",
         "Jersey Number": 81},
        {"Player": "Hugo Ekitike", "Position": "Forward",
         "Jersey Number": 9},
        {"Player": "Luis Díaz", "Position": "Forward",
         "Jersey Number": 7},
        {"Player": "Darwin Núñez", "Position": "Forward",
         "Jersey Number": 9},
        {"Player": "Mohamed Salah", "Position": "Forward",
         "Jersey Number": 11},
        {"Player": "Federico Chiesa", "Position": "Forward",
         "Jersey Number": 23},
        {"Player": "Cody Gakpo", "Position": "Forward",
         "Jersey Number": 18},
        {"Player": "Ben Doak", "Position": "Forward",
         "Jersey Number": 50},
        {"Player": "Rio Ngumoha", "Position": "Forward",
         "Jersey Number": 90},
        {"Player": "Jayden Danns", "Position": "Forward",
         "Jersey Number": 76},
    ]

    fake = Faker()

    for player in full_squad:
        player["player_id"] = fake.unique.uuid4()
        player["nationality"] = fake.country()
        player["date_of_birth"] = fake.date_of_birth(
            minimum_age=17, maximum_age=38
        )

    df_players = pd.DataFrame(full_squad)
    df_players["date_of_birth"] = pd.to_datetime(df_players["date_of_birth"])
    df_players["age"] = (
        pd.to_datetime("today").year - df_players["date_of_birth"].dt.year
    )

    df_players = df_players[
        [
            "player_id",
            "Player",
            "Position",
            "Jersey Number",
            "date_of_birth",
            "age",
            "nationality",
        ]
    ]
    return df_players


def generate_transactions():
    """
    A function that generates synthetic football transaction data
    using the Faker library.

    Args:
        None
    Returns:
        A transactional dataframe is returned.
    """
    fake = Faker()
    df_players = get_players()
    num_transactions = random.randint(500000, 1000000)

    transaction_types = [
        "transfer_fee",
        "loan_fee",
        "monthly_salary",
        "match_fee",
        "goal_bonus",
        "assist_bonus",
        "clean_sheet_bonus",
        "win_bonus",
        "fine",
        "endorsement_payment",
    ]
    payment_methods = [
        "bank_transfer",
        "cash",
        "cheque",
        "mobile_payment",
        "crypto",
        "international_wire",
        "direct_deposit",
        "club_credit",
        "agent_disbursement",
        "performance_wallet",
    ]
    clubs = [
        "Arsenal",
        "Aston Villa",
        "Bournemouth",
        "Brentford",
        "Brighton & Hove Albion",
        "Burnley",
        "Chelsea",
        "Crystal Palace",
        "Everton",
        "Fulham",
        "Leeds United",
        "Liverpool",
        "Manchester City",
        "Manchester United",
        "Newcastle United",
        "Nottingham Forest",
        "Sunderland",
        "Tottenham Hotspur",
        "West Ham United",
        "Wolverhampton Wanderers",
    ]

    football_finance = []

    for i in range(num_transactions):
        player = df_players.sample(1).iloc[0]
        transaction = {
            "transaction_id": fake.unique.uuid4(),
            "player_id": player["player_id"],
            "player_name": player["Player"],
            "jersey_number": player["Jersey Number"],
            "nationality": player["nationality"],
            "date_of_birth": player["date_of_birth"],
            "transaction_type": random.choice(transaction_types),
            "transaction_date": fake.date_time_this_decade(),
            "amount": fake.random_int(min=500, max=1000000),
            "payment_method": random.choice(payment_methods),
            "from_club": random.choice(clubs),
            "to_club": "Liverpool",
            "competition": "Premier League",
            "currency_name": fake.currency_name(),
            "currency_code": fake.currency_code(),
            "contract_duration": fake.random_int(min=1, max=10),
            "created_at": fake.date_time_this_year(),
            "updated_at": fake.date_time_this_year(),
        }
        football_finance.append(transaction)

    df_transactions = pd.DataFrame(football_finance)
    today = pd.to_datetime("today")
    df_transactions["age"] = (
        (today - df_transactions["date_of_birth"]).dt.days // 365
    )

    return df_transactions
