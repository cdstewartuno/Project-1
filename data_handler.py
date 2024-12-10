import csv
import os
from constants import EXCEL_FILE

def initialize_csv():
    """Initializes the CSV file with headers if it doesn't exist."""
    if not os.path.exists(EXCEL_FILE):
        with open(EXCEL_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Voter_ID", "Candidate"])  # Headers

def add_vote(voter_id, candidate):
    """Adds a vote to the CSV if the voter hasn't voted already."""
    if not get_voter(voter_id):
        with open(EXCEL_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([voter_id, candidate])
        return True
    return False  # Voter has already voted

def get_voter(voter_id):
    """Checks if a voter has already voted by their ID."""
    with open(EXCEL_FILE, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if row[0] == voter_id:
                return True
    return False

def get_votes(candidates):
    """Returns a dictionary of vote counts for each candidate, including 'Other' candidates."""
    votes = {candidate: 0 for candidate in candidates}
    other_votes = {}  # Tracks votes for "Other" candidates

    with open(EXCEL_FILE, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            candidate = row[1]
            if candidate in candidates:
                votes[candidate] += 1
            else:
                if candidate in other_votes:
                    other_votes[candidate] += 1
                else:
                    other_votes[candidate] = 1

    # Include "Other" in the main dictionary if there are votes
    if other_votes:
        total_other_votes = sum(other_votes.values())
        votes["Other"] = total_other_votes
        majority_candidate = max(other_votes, key=other_votes.get)
        if other_votes[majority_candidate] > total_other_votes / 2:
            votes[majority_candidate] = other_votes[majority_candidate]

    return votes
