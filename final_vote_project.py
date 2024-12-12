from typing import Dict, List
import tkinter as tk
from tkinter import messagebox
import os


def separator(length: int = 47, char: str = '-') -> str:
    return char * length


class VoteManager:
    def __init__(self, data_file: str):
        self.data_file = data_file
        self.votes = {"Bianca": 0, "Edward": 0, "Felicia": 0}
        self.voted_ids = set()
        self.load_votes()

    def load_votes(self) -> None:
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith("ID:"):
                        voter_id = line.strip().split(":")[1]
                        self.voted_ids.add(voter_id)
                    else:
                        candidate, count = line.strip().split(',')
                        self.votes[candidate] = int(count)

    def save_votes(self) -> None:
        with open(self.data_file, 'w') as f:
            for candidate, count in self.votes.items():
                f.write(f"{candidate},{count}\n")
            for voter_id in self.voted_ids:
                f.write(f"ID:{voter_id}\n")

    def reset_votes(self) -> None:
        self.votes = {candidate: 0 for candidate in self.votes}
        self.voted_ids.clear()
        self.save_votes()

    def add_vote(self, candidate: str, voter_id: str) -> None:
        if voter_id in self.voted_ids:
            raise ValueError("Duplicate vote detected. You have already voted.")
        if candidate in self.votes:
            self.votes[candidate] += 1
            self.voted_ids.add(voter_id)
        else:
            raise ValueError(f"Invalid candidate: {candidate}")

    def get_vote_summary(self) -> Dict[str, int]:
        total_votes = sum(self.votes.values())
        return {**self.votes, "Total": total_votes}


class VoteApp:
    def __init__(self, root: tk.Tk, vote_manager: VoteManager):
        self.root = root
        self.vote_manager = vote_manager
        self.root.title("Voting System")
        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        tk.Label(self.root, text="Voting System", font=("Arial", 16)).pack(pady=10)
        separator_frame = tk.Frame(self.root, height=2, bd=1, relief=tk.SUNKEN)
        separator_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(self.root, text="Enter Voter ID:").pack(pady=5)
        self.voter_id_entry = tk.Entry(self.root)
        self.voter_id_entry.pack(pady=5)

        tk.Button(self.root, text="Vote for Bianca", command=lambda: self.cast_vote("Bianca"), width=20).pack(pady=5)
        tk.Button(self.root, text="Vote for Edward", command=lambda: self.cast_vote("Edward"), width=20).pack(pady=5)
        tk.Button(self.root, text="Vote for Felicia", command=lambda: self.cast_vote("Felicia"), width=20).pack(pady=5)
        tk.Button(self.root, text="View Results", command=self.view_results, width=20).pack(pady=5)

    def cast_vote(self, candidate: str):
        voter_id = self.voter_id_entry.get().strip()
        if not voter_id:
            messagebox.showerror("Error", "Voter ID is required.")
            return
        try:
            self.vote_manager.add_vote(candidate, voter_id)
            self.vote_manager.save_votes()
            messagebox.showinfo("Vote Recorded", f"Successfully voted for {candidate}.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def view_results(self):
        results = self.vote_manager.get_vote_summary()
        result_str = "\n".join([f"{candidate}: {count}" for candidate, count in results.items()])
        messagebox.showinfo("Vote Results", result_str)

    def on_close(self):
        """Handle window close event."""
        if messagebox.askyesno("Exit", "Are you sure you want to exit? All votes will be reset."):
            self.vote_manager.reset_votes()
            self.root.destroy()


if __name__ == "__main__":
    vote_file = "votes.txt"
    vote_manager = VoteManager(vote_file)
    try:
        root = tk.Tk()
        app = VoteApp(root, vote_manager)
        root.mainloop()
    except KeyboardInterrupt:
        print("Resetting votes due to KeyboardInterrupt...")
        vote_manager.reset_votes()
        print("Votes have been reset.")
