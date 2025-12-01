import tkinter as tk
from tkinter import messagebox
import random

# Question Bank
QUESTIONS = {
    "easy": [
        ("Capital of India?", ["Delhi", "Mumbai", "Kolkata", "Chennai"], "Delhi"),
        ("2 + 3 = ?", ["4", "5", "6", "3"], "5")
    ],
    "medium": [
        ("Who invented Python?", ["Guido", "Dennis", "James", "Bjarne"], "Guido"),
        ("5 * 6 = ?", ["11", "30", "25", "36"], "30")
    ],
    "hard": [
        ("Binary search complexity?", ["O(n)", "O(log n)", "O(n^2)", "O(1)"], "O(log n)"),
        ("RAM stands for?", ["Random Access Memory", "Run A Machine", "Read A Memory", "None"], "Random Access Memory")
    ]
}

class AdaptiveQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Adaptive Learning Quiz App")
        self.root.geometry("650x520")
        self.root.configure(bg="#e2dff5")  # soft background

        # Quiz variables
        self.level = "easy"
        self.score = 0
        self.total = 6
        self.answered = 0
        self.remaining = {lvl: QUESTIONS[lvl].copy() for lvl in QUESTIONS}

        # --- Header ---
        tk.Label(root, text="Adaptive Learning Quiz",
                 font=("Segoe UI", 24, "bold"),
                 bg="#b74b6d", fg="white", pady=15).pack(fill="x")

        # --- Level tag ---
        self.level_text = tk.StringVar(value="Level: Easy")
        tk.Label(root, textvariable=self.level_text, font=("Segoe UI", 14, "bold"),
                 bg="#f5dfdf", fg="#47421e").pack(pady=8)

        # --- Question card ---
        self.card = tk.Frame(root, bg="white", bd=0,
                             highlightbackground="#e3c3c2",
                             highlightthickness=2)
        self.card.pack(pady=20, padx=30, fill="x")

        self.q_text = tk.StringVar()
        tk.Label(self.card, textvariable=self.q_text, font=("Segoe UI", 17, "bold"),
                 wraplength=580, bg="white", fg="#1e2a47").pack(pady=20)

        # --- Options ---
        self.var = tk.StringVar()
        self.options = []
        for _ in range(4):
            rb = tk.Radiobutton(root, text="", variable=self.var, value="",
                                font=("Segoe UI", 14),
                                bg="#dfe7f5",
                                activebackground= "#cad6ec",
                                selectcolor="white")
            rb.pack(anchor="w", padx=60, pady=5)
            self.options.append(rb)

        # --- Modern Button ---
        self.next_btn = tk.Button(root, text="Next",
                                  font=("Segoe UI", 14, "bold"),
                                  bg="#4b6cb7", fg="white",
                                  activebackground="#3b5291",
                                  pady=8, padx=20,
                                  bd=0, cursor="hand2",
                                  command=self.check_answer)
        self.next_btn.pack(pady=25)

        self.load_question()

    def update_level_label(self):
        self.level_text.set(f"Level: {self.level.capitalize()}")

    def get_question(self, level):
        if not self.remaining[level]:
            return None
        q = random.choice(self.remaining[level])
        self.remaining[level].remove(q)
        return q

    def load_question(self):
        self.var.set("")

        qset = self.get_question(self.level)
        if qset is None:
            for lvl in ["easy", "medium", "hard"]:
                qset = self.get_question(lvl)
                if qset:
                    self.level = lvl
                    break

        if qset is None:
            self.show_result()
            return

        self.update_level_label()

        question, options, self.answer = qset
        self.q_text.set(question)

        random.shuffle(options)
        for rb, opt in zip(self.options, options):
            rb.config(text=opt, value=opt)

    def check_answer(self):
        selected = self.var.get()
        if not selected:
            messagebox.showwarning("Alert", "Please select an answer!")
            return

        # Adaptive logic
        if selected == self.answer:
            self.score += 1
            if self.level == "easy":
                self.level = "medium"
            elif self.level == "medium":
                self.level = "hard"
        else:
            if self.level == "hard":
                self.level = "medium"
            elif self.level == "medium":
                self.level = "easy"

        self.answered += 1

        if self.answered == self.total:
            self.show_result()
        else:
            self.load_question()

    def show_result(self):
        accuracy = (self.score / self.total) * 100

        # Custom beautiful result popup
        result = tk.Toplevel(self.root)
        result.title("Result")
        result.geometry("380x260")
        result.configure(bg="#f8f9ff")

        tk.Label(result, text="Quiz Completed!",
                 font=("Segoe UI", 22, "bold"),
                 bg="#f8f9ff", fg="#1e2a47").pack(pady=15)

        tk.Label(result,
                 text=f"Score: {self.score}/{self.total}\nAccuracy: {accuracy:.2f}%",
                 font=("Segoe UI", 16),
                 bg="#f8f9ff", fg="#1e2a47").pack(pady=10)

        tk.Button(result, text="Close", command=self.root.destroy,
                  bg="#4b6cb7", fg="white",
                  font=("Segoe UI", 14, "bold"),
                  bd=0, padx=15, pady=6).pack(pady=18)


root = tk.Tk()
app = AdaptiveQuiz(root)
root.mainloop()






