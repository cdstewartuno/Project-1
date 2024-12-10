import tkinter as tk
from tkinter import messagebox
from data_handler import add_vote, get_votes
from validation import is_valid_voter_id
from constants import ERROR_VOTER_ID, ERROR_ALREADY_VOTED

class VotingApp:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("Voting System")

        self.voter_id_entry = None
        self.candidate_var = tk.StringVar()
        self.candidate_list = ["John", "Jane"]
        self.custom_candidate_entry = tk.Entry(self.app)

        # Set up the custom candidate input field
        self.other_candidate_entry_label = tk.Label(self.app, text="Enter a custom candidate name:")
        self.custom_candidate_entry.grid(row=5, column=1)
        self.custom_candidate_entry.grid_forget()  # Hide it initially

    def cast_vote(self):
        voter_id = self.voter_id_entry.get().strip()
        selected_candidate = self.candidate_var.get()

        if not is_valid_voter_id(voter_id):
            messagebox.showerror("Error", ERROR_VOTER_ID)
            return

        # Handle custom "Other" candidate
        if selected_candidate == "Other":
            custom_candidate = self.custom_candidate_entry.get().strip()
            if not custom_candidate:
                messagebox.showerror("Error", "Please enter a valid candidate name.")
                return
            selected_candidate = custom_candidate

        # Ensure the voter hasn't voted already
        if add_vote(voter_id, selected_candidate):
            messagebox.showinfo("Success", "Vote cast successfully!")
            self.clear_user_inputs()  # Clear inputs after a successful vote
            self.update_percentage()
        else:
            messagebox.showerror("Error", ERROR_ALREADY_VOTED)

    def clear_user_inputs(self):
        """Clears the voter ID and custom candidate entry fields."""
        self.voter_id_entry.delete(0, tk.END)  # Clear the voter ID input
        self.custom_candidate_entry.delete(0, tk.END)  # Clear the custom candidate input
        self.candidate_var.set(self.candidate_list[0])  # Reset to the first candidate option
        self.update_entry_box_visibility()  # Ensure "Other" entry box is hidden

    def update_percentage(self):
        votes = get_votes(self.candidate_list)
        total_votes = sum(votes.values())
        result = "\n".join(
            f"{candidate}: {votes.get(candidate, 0)} votes ({(votes.get(candidate, 0) / total_votes) * 100:.2f}%)" if total_votes else f"{candidate}: 0 votes"
            for candidate in votes
        )
        self.vote_result_label.config(text=result)

    def update_entry_box_visibility(self):
        """Show or hide the custom candidate entry box depending on the selection."""
        if self.candidate_var.get() == "Other":
            self.other_candidate_entry_label.grid(row=5, column=0)
            self.custom_candidate_entry.grid(row=5, column=1)
        else:
            self.other_candidate_entry_label.grid_forget()
            self.custom_candidate_entry.grid_forget()

    def run(self):
        # Create UI Elements
        tk.Label(self.app, text="Voter ID:").grid(row=0, column=0)
        self.voter_id_entry = tk.Entry(self.app)
        self.voter_id_entry.grid(row=0, column=1)

        tk.Label(self.app, text="Candidates:").grid(row=1, column=0)

        self.candidate_var.set(self.candidate_list[0])
        for idx, candidate in enumerate(self.candidate_list + ["Other"]):
            radio_btn = tk.Radiobutton(self.app, text=candidate, variable=self.candidate_var, value=candidate, command=self.update_entry_box_visibility)
            radio_btn.grid(row=2 + idx, column=1, sticky="w")

        tk.Button(self.app, text="Vote", command=self.cast_vote).grid(row=6, column=0, columnspan=2, pady=10)

        self.vote_result_label = tk.Label(self.app, text="Votes will be shown here")
        self.vote_result_label.grid(row=7, column=0, columnspan=2, pady=10)

        self.update_entry_box_visibility()  # Initial setup
        self.app.mainloop()
