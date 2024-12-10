from GUI import VotingApp
from data_handler import initialize_csv

if __name__ == "__main__":
    # Ensure the CSV file is set up
    initialize_csv()

    # Start the voting application
    VotingApp().run()
