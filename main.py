from GUI import VotingApp
from data_handler import initialize_csv

if __name__ == "__main__":
    """
    Entry point for the voting application. Ensures the CSV file is set up
    and starts the voting application.
    """
    initialize_csv()
    VotingApp().run()
