import random
import tkinter as tk
from tkinter import ttk

MAX_LINES = 3
MIN_BET = 1
MAX_BET = 100
ROWS = 3
COLS = 3

symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8,
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2,
}

SYMBOL_COLORS = {
    "A": "#ff5c8a",
    "B": "#ffd166",
    "C": "#45d6c5",
    "D": "#8a7dff",
}


def spin_slot_machine():
    symbols = []
    for symbol, count in symbol_count.items():
        for _ in range(count):
            symbols.append(symbol)

    columns = []
    for _ in range(COLS):
        column = []
        current_symbols = symbols[:]
        for _ in range(ROWS):
            value = random.choice(current_symbols)
            column.append(value)
            current_symbols.remove(value)
        columns.append(column)

    return columns


def get_winnings(columns, lines, bet):
    winnings = 0
    winning_lines = []

    for line in range(lines):
        symbol = columns[0][line]
        for col in range(COLS):
            if columns[col][line] != symbol:
                break
        else:
            winnings += symbol_value[symbol] * bet
            winning_lines.append(line + 1)

    return winnings, winning_lines


class SlotMachineWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Slot Machines for bets")
        self.root.geometry("1200x760")
        self.root.state("zoomed")
        self.root.minsize(980, 620)
        self._configure_styles()

        self.balance = 0

        self.balance_var = tk.StringVar(value="$0")
        self.status_var = tk.StringVar(value="Enter a deposit to begin.")
        self.result_var = tk.StringVar(value="")

        main_frame = ttk.Frame(root, padding=18, style="App.TFrame")
        main_frame.pack(fill="both", expand=True)

        title = ttk.Label(main_frame, text="Betting Slots", style="Title.TLabel")
        title.pack(pady=(0, 10))

        top_row = ttk.Frame(main_frame, style="Panel.TFrame", padding=12)
        top_row.pack(fill="x", pady=5)

        ttk.Label(top_row, text="Balance:", style="Panel.TLabel").pack(side="left")
        ttk.Label(top_row, textvariable=self.balance_var, style="Balance.TLabel").pack(side="left", padx=(8, 20))

        ttk.Label(top_row, text="Lines:", style="Panel.TLabel").pack(side="left")
        self.lines_var = tk.StringVar(value="1")
        self.lines_combo = ttk.Combobox(top_row, textvariable=self.lines_var, values=["1", "2", "3"], width=5, state="readonly", style="Game.TCombobox")
        self.lines_combo.pack(side="left", padx=(8, 16))

        ttk.Label(top_row, text="Bet per line:", style="Panel.TLabel").pack(side="left")
        self.bet_var = tk.StringVar(value="5")
        self.bet_entry = ttk.Entry(top_row, textvariable=self.bet_var, width=8, style="Game.TEntry")
        self.bet_entry.pack(side="left", padx=(8, 0))

        deposit_row = ttk.Frame(main_frame, style="App.TFrame")
        deposit_row.pack(fill="x", pady=(10, 8))

        ttk.Label(deposit_row, text="Deposit:", style="App.TLabel").pack(side="left")
        self.deposit_entry = ttk.Entry(deposit_row, width=12, style="Game.TEntry")
        self.deposit_entry.pack(side="left", padx=(8, 10))
        self.deposit_button = ttk.Button(deposit_row, text="Add Deposit", command=self.add_deposit, style="Deposit.TButton")
        self.deposit_button.pack(side="left")

        self.slot_frame = ttk.Frame(main_frame, style="Reels.TFrame", padding=8)
        self.slot_frame.pack(pady=10)

        self.slot_labels = []
        for row in range(ROWS):
            row_labels = []
            for col in range(COLS):
                label = ttk.Label(self.slot_frame, text="?", style="UnknownSlot.TLabel")
                label.grid(row=row, column=col, padx=6, pady=6)
                row_labels.append(label)
            self.slot_labels.append(row_labels)

        action_row = ttk.Frame(main_frame, style="App.TFrame")
        action_row.pack(pady=(8, 6))
        self.spin_button = ttk.Button(action_row, text="SPIN", command=self.spin, style="Spin.TButton")
        self.spin_button.pack(side="left", padx=(0, 10))
        ttk.Button(action_row, text="Reset", command=self.reset_game, style="Reset.TButton").pack(side="left")

        ttk.Label(main_frame, textvariable=self.status_var, style="Status.TLabel", wraplength=520, justify="center").pack(pady=(8, 2))
        ttk.Label(main_frame, textvariable=self.result_var, style="Result.TLabel").pack(pady=(0, 6))

        self.reset_game()

    def _configure_styles(self):
        palette = {
            "background": "#11152b",
            "panel": "#202744",
            "text": "#f4f1ff",
            "muted": "#b8bfdc",
            "teal": "#45d6c5",
            "gold": "#ffd166",
            "pink": "#ff5c8a",
        }
        style = ttk.Style(self.root)
        style.theme_use("clam")
        self.root.configure(background=palette["background"])

        style.configure("App.TFrame", background=palette["background"])
        style.configure("Panel.TFrame", background=palette["panel"])
        style.configure("Reels.TFrame", background=palette["panel"])
        style.configure("App.TLabel", background=palette["background"], foreground=palette["text"], font=("Segoe UI", 10))
        style.configure("Panel.TLabel", background=palette["panel"], foreground=palette["text"], font=("Segoe UI", 10, "bold"))
        style.configure("Title.TLabel", background=palette["background"], foreground=palette["gold"], font=("Segoe UI", 26, "bold"))
        style.configure("Balance.TLabel", background=palette["panel"], foreground=palette["teal"], font=("Segoe UI", 14, "bold"))
        style.configure("Status.TLabel", background=palette["background"], foreground=palette["muted"], font=("Segoe UI", 10))
        style.configure("Result.TLabel", background=palette["background"], foreground=palette["pink"], font=("Segoe UI", 12, "bold"))
        style.configure("Game.TEntry", fieldbackground="#f4f1ff", foreground="#11152b", padding=6)
        style.configure("Game.TCombobox", fieldbackground="#f4f1ff", foreground="#11152b", padding=5)

        style.configure("UnknownSlot.TLabel", background="#303858", foreground=palette["gold"], font=("Segoe UI", 24, "bold"), width=4, padding=12, anchor="center", relief="solid", borderwidth=2)
        for symbol, color in SYMBOL_COLORS.items():
            style.configure(f"Slot{symbol}.TLabel", background=color, foreground="#11152b", font=("Segoe UI", 24, "bold"), width=4, padding=12, anchor="center", relief="solid", borderwidth=2)

        style.configure("Spin.TButton", background=palette["teal"], foreground="#11152b", font=("Segoe UI", 12, "bold"), padding=(24, 10), borderwidth=0)
        style.map("Spin.TButton", background=[("active", "#76ecdc"), ("pressed", "#2bb4a5")])
        style.configure("Deposit.TButton", background=palette["gold"], foreground="#11152b", font=("Segoe UI", 10, "bold"), padding=(12, 7), borderwidth=0)
        style.map("Deposit.TButton", background=[("active", "#ffe39a"), ("pressed", "#e6b94f")])
        style.configure("Reset.TButton", background="#59617f", foreground=palette["text"], font=("Segoe UI", 10, "bold"), padding=(14, 8), borderwidth=0)
        style.map("Reset.TButton", background=[("active", "#747e9f"), ("pressed", "#454d69")])

    def add_deposit(self):
        try:
            deposit = int(self.deposit_entry.get())
        except ValueError:
            self.status_var.set("Please enter a valid deposit number.")
            return

        if deposit <= 0:
            self.status_var.set("Deposit must be greater than zero.")
            return

        self.balance += deposit
        self.balance_var.set(f"${self.balance}")
        self.deposit_entry.delete(0, tk.END)
        self.status_var.set(f"Deposit added. Balance: ${self.balance}")
        self.result_var.set("Ready to spin!")

    def reset_game(self):
        self.balance = 0
        self.balance_var.set("$0")
        self.status_var.set("Enter a deposit to begin.")
        self.result_var.set("")
        self.clear_slots()

    def clear_slots(self):
        for row in self.slot_labels:
            for label in row:
                label.config(text="?", style="UnknownSlot.TLabel")

    def spin(self):
        if self.balance <= 0:
            self.status_var.set("Add a deposit before spinning.")
            return

        try:
            lines = int(self.lines_var.get())
            bet = int(self.bet_var.get())
        except ValueError:
            self.status_var.set("Please enter valid line and bet values.")
            return

        if not (1 <= lines <= MAX_LINES):
            self.status_var.set(f"Choose between 1 and {MAX_LINES} lines.")
            return

        if not (MIN_BET <= bet <= MAX_BET):
            self.status_var.set(f"Bet per line must be between {MIN_BET} and {MAX_BET}.")
            return

        total_bet = lines * bet
        if total_bet > self.balance:
            self.status_var.set("Bet exceeds the current balance.")
            return

        self.balance -= total_bet
        columns = spin_slot_machine()
        self.show_slots(columns)

        winnings, winning_lines = get_winnings(columns, lines, bet)
        if winnings > 0:
            self.balance += winnings
            self.result_var.set(f"You won ${winnings} on line(s): {winning_lines}")
            self.status_var.set("Nice win!")
        else:
            self.result_var.set("No winning lines this round.")
            self.status_var.set("Better luck next spin!")

        self.balance_var.set(f"${self.balance}")

        if self.balance <= 0:
            self.status_var.set("You are out of money. Add another deposit to keep playing.")

    def show_slots(self, columns):
        for row in range(ROWS):
            for col in range(COLS):
                symbol = columns[col][row]
                self.slot_labels[row][col].config(text=symbol, style=f"Slot{symbol}.TLabel")


def main():
    root = tk.Tk()
    app = SlotMachineWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
