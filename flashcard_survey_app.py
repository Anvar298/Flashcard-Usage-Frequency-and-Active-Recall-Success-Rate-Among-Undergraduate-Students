import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, filedialog, ttk

# -------- REQUIRED VARIABLE TYPES --------
version_float = 1.0
allowed_ext = {".json"}
used_files = set()
student_record = {}

# -------- QUESTIONS --------
questions = [
    {
        "q": "Do you use digital flashcard tools (e.g., Anki, Quizlet) as part of your regular study strategy?",
        "opts": [
            ("Never use them", 0),
            ("Rarely use them", 1),
            ("Occasionally use them", 2),
            ("Regularly use them", 3),
            ("Always use them", 4)
        ]
    },
    {
        "q": "When did you first begin using digital flashcard tools?",
        "opts": [
            ("Before entering university", 0),
            ("During my first year", 1),
            ("During my second year", 2),
            ("During my third year or later", 3),
            ("I have not used them", 4)
        ]
    },
    {
        "q": "How often do you use flashcards during an active study period for an upcoming exam?",
        "opts": [
            ("Every day", 4),
            ("5-6 days per week", 3),
            ("3-4 days per week", 2),
            ("1-2 days per week", 1),
            ("Only the day before the exam", 0)
        ]
    },
    {
        "q": "After an exam is completed, do you continue reviewing the same flashcard deck?",
        "opts": [
            ("Yes, I maintain consistent daily reviews", 4),
            ("Sometimes, for subjects that build on prior material", 3),
            ("Rarely", 2),
            ("Never - I stop reviewing after each exam", 1),
            ("Not applicable", 0)
        ]
    },
    {
        "q": "When reviewing a flashcard, which best describes your typical approach?",
        "opts": [
            ("I actively recall the answer before flipping the card", 4),
            ("I try to recall but often peek quickly", 3),
            ("I read both sides simultaneously", 2),
            ("I click through cards quickly and read", 1),
            ("No consistent strategy", 0)
        ]
    },
    {
        "q": "Which style of flashcard do you prefer when studying?",
        "opts": [
            ("Cloze deletion / fill-in-the-blank", 4),
            ("Basic question-and-answer", 3),
            ("Image occlusion (hidden image regions)", 2),
            ("Mixed styles", 1),
            ("No preference / never used", 0)
        ]
    },
    {
        "q": "Which type of flashcard decks do you primarily use?",
        "opts": [
            ("I create my own cards from lecture notes", 4),
            ("Mix of self-made and pre-made decks", 3),
            ("Mostly pre-made decks from classmates", 2),
            ("Entirely downloaded online decks", 1),
            ("I do not use flashcard decks", 0)
        ]
    },
    {
        "q": "What percentage of your total study time do flashcards represent?",
        "opts": [
            ("More than 60%", 4),
            ("40-60%", 3),
            ("20-40%", 2),
            ("Less than 20%", 1),
            ("I do not use flashcards", 0)
        ]
    },
    {
        "q": "To what extent do you agree that flashcard-based active recall contributes to your academic success?",
        "opts": [
            ("Strongly Agree", 4),
            ("Agree", 3),
            ("Neutral", 2),
            ("Disagree", 1),
            ("Strongly Disagree", 0)
        ]
    },
    {
        "q": "How does completing your scheduled flashcard reviews affect your confidence before an exam?",
        "opts": [
            ("Large increase in confidence", 4),
            ("Moderate increase in confidence", 3),
            ("No noticeable change", 2),
            ("Slight decrease (feel overwhelmed)", 1),
            ("I do not use scheduled reviews", 0)
        ]
    },
    {
        "q": "How often do you feel accomplished after completing your daily flashcard reviews?",
        "opts": [
            ("Always", 4),
            ("Often", 3),
            ("Sometimes", 2),
            ("Rarely", 1),
            ("Never", 0)
        ]
    },
    {
        "q": "How often do you feel anxious or frustrated when you miss your scheduled flashcard reviews?",
        "opts": [
            ("Always", 4),
            ("Often", 3),
            ("Sometimes", 2),
            ("Rarely", 1),
            ("Never", 0)
        ]
    },
    {
        "q": "I use flashcards while engaged in other daily activities (commuting, exercising, eating).",
        "opts": [
            ("Always", 4),
            ("Often", 3),
            ("Sometimes", 2),
            ("Rarely", 1),
            ("Never", 0)
        ]
    },
    {
        "q": "Have you lost sleep in order to complete flashcard reviews before an exam?",
        "opts": [
            ("Always", 4),
            ("Often", 3),
            ("Sometimes", 2),
            ("Rarely", 1),
            ("Never", 0)
        ]
    },
    {
        "q": "Following your studies, how likely are you to continue using flashcard-based active recall?",
        "opts": [
            ("Very likely", 4),
            ("Somewhat likely", 3),
            ("Unsure", 2),
            ("Unlikely", 1),
            ("Very unlikely", 0)
        ]
    }
]

# -------- ACTIVE RECALL STATES --------
recall_states = {
    "Minimal Engagement":       (0,  9),
    "Low Engagement":           (10, 19),
    "Below Average Engagement": (20, 29),
    "Moderate Engagement":      (30, 39),
    "Average Engagement":       (40, 44),
    "Above Average Engagement": (45, 49),
    "Good Active Recall":       (50, 54),
    "High Active Recall":       (55, 57),
    "Very High Active Recall":  (58, 59),
    "Exceptional Active Recall":(60, 60)
}

# -------- VALIDATION --------
def validate_name(name: str) -> bool:
    return name.strip() != "" and not any(c.isdigit() for c in name)

def validate_dob(dob: str) -> bool:
    try:
        datetime.strptime(dob, "%Y-%m-%d")
        return True
    except:
        return False

def interpret_score(score: int) -> str:
    for state, (low, high) in recall_states.items():
        if low <= score <= high:
            return state
    return "Unknown"

def save_json(filename: str, data: dict):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# -------- GUI APP --------
class SurveyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard Usage & Active Recall Survey")
        self.root.geometry("520x480")
        self.root.resizable(False, False)
        self.main_menu()

    # ── HELPERS ──────────────────────────────────────────
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def add_labeled_entry(self, parent, label: str, var):
        frame = tk.Frame(parent)
        frame.pack(pady=4)
        tk.Label(frame, text=label, width=30, anchor="w").pack(side="left")
        tk.Entry(frame, textvariable=var, width=22).pack(side="left")

    # ── MAIN MENU ─────────────────────────────────────────
    def main_menu(self):
        self.clear_window()

        tk.Label(self.root,
                 text="Flashcard Usage & Active Recall\nSurvey Program",
                 font=("Arial", 16, "bold"), justify="center").pack(pady=18)

        btn_cfg = {"width": 46, "pady": 4}

        tk.Button(self.root, text="1.  Load existing result file",
                  **btn_cfg, command=self.load_result_file).pack(pady=5)

        tk.Button(self.root, text="2.  Start new questionnaire",
                  **btn_cfg, command=self.start_survey_info).pack(pady=5)

        tk.Button(self.root, text="3.  Start questionnaire (load questions from file)",
                  **btn_cfg, command=self.load_questions_then_start).pack(pady=5)

        tk.Button(self.root, text="4.  Save survey questions + recall states",
                  **btn_cfg, command=self.save_questions_and_states).pack(pady=5)

        tk.Label(self.root,
                 text=f"v{version_float}  |  Flashcard & Active Recall Research Tool",
                 font=("Arial", 9), fg="grey").pack(side="bottom", pady=6)

    # ── OPTION 1 – LOAD RESULT FILE ───────────────────────
    def load_result_file(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not path:
            return
        used_files.add(path)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Pretty display in a new window
            win = tk.Toplevel(self.root)
            win.title("Loaded Result")
            win.geometry("460x420")

            text = tk.Text(win, wrap="word", font=("Courier", 10))
            text.pack(fill="both", expand=True, padx=8, pady=8)

            lines = [
                f"Name      : {data.get('name','')} {data.get('surname','')}",
                f"DOB       : {data.get('dob','')}",
                f"Student ID: {data.get('student_id','')}",
                f"Version   : {data.get('version','')}",
                f"Score     : {data.get('total_score','')}",
                f"Result    : {data.get('result','')}",
                "",
                "── Answers ──────────────────────────────────────────",
            ]
            for i, ans in enumerate(data.get("answers", []), 1):
                lines.append(f"Q{i}: {ans.get('question','')}")
                lines.append(f"    → {ans.get('selected_option','')}  (score: {ans.get('score','')})")
                lines.append("")

            text.insert("end", "\n".join(lines))
            text.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file.\n{e}")

    # ── OPTION 4 – SAVE QUESTIONS & STATES ────────────────
    def save_questions_and_states(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            initialfile="survey_questions_and_states.json",
            filetypes=[("JSON files", "*.json")]
        )
        if not path:
            return
        data = {
            "questions": questions,
            "recall_states": recall_states
        }
        save_json(path, data)
        used_files.add(path)
        messagebox.showinfo("Saved", f"Questions and recall states saved to:\n{path}")

    # ── OPTION 2 – START SURVEY (built-in questions) ──────
    def start_survey_info(self):
        self.selected_questions = questions
        self.show_user_form()

    # ── OPTION 3 – LOAD QUESTIONS FROM FILE ───────────────
    def load_questions_then_start(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not path:
            return
        used_files.add(path)
        try:
            with open(path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            # Accept either a plain list or a dict with a "questions" key
            if isinstance(loaded, list):
                self.selected_questions = loaded
            elif isinstance(loaded, dict) and "questions" in loaded:
                self.selected_questions = loaded["questions"]
            else:
                raise ValueError("Unrecognised format.")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid question file.\n{e}")
            return
        self.show_user_form()

    # ── USER DETAILS FORM ─────────────────────────────────
    def show_user_form(self):
        self.clear_window()

        tk.Label(self.root, text="Enter Your Details",
                 font=("Arial", 15, "bold")).pack(pady=12)

        self.name_var    = tk.StringVar()
        self.surname_var = tk.StringVar()
        self.dob_var     = tk.StringVar()
        self.sid_var     = tk.StringVar()
        self.inst_var    = tk.StringVar()

        self.add_labeled_entry(self.root, "Given Name:",              self.name_var)
        self.add_labeled_entry(self.root, "Surname:",                 self.surname_var)
        self.add_labeled_entry(self.root, "Date of Birth (YYYY-MM-DD):", self.dob_var)
        self.add_labeled_entry(self.root, "Student ID (digits only):", self.sid_var)

        # Institution dropdown
        frame = tk.Frame(self.root)
        frame.pack(pady=4)
        tk.Label(frame, text="Institution:", width=30, anchor="w").pack(side="left")
        institutions = [
            "UCLA – Los Angeles, CA",
            "UIUC – Urbana-Champaign, IL",
            "UNC-CH – Chapel Hill, NC",
            "UA – Tucson, AZ",
            "Other"
        ]
        inst_cb = ttk.Combobox(frame, textvariable=self.inst_var,
                               values=institutions, width=21, state="readonly")
        inst_cb.pack(side="left")

        tk.Button(self.root, text="Start Survey",
                  width=20, command=self.validate_user_form).pack(pady=14)

        tk.Button(self.root, text="← Back",
                  width=10, command=self.main_menu).pack()

    def validate_user_form(self):
        name    = self.name_var.get()
        surname = self.surname_var.get()
        dob     = self.dob_var.get()
        sid     = self.sid_var.get()
        inst    = self.inst_var.get()

        if not validate_name(name):
            return messagebox.showerror("Error", "Invalid given name.")
        if not validate_name(surname):
            return messagebox.showerror("Error", "Invalid surname.")
        if not validate_dob(dob):
            return messagebox.showerror("Error", "Invalid date of birth (use YYYY-MM-DD).")
        if not sid.isdigit():
            return messagebox.showerror("Error", "Student ID must contain digits only.")
        if not inst:
            return messagebox.showerror("Error", "Please select your institution.")

        self.record = {
            "name":        name,
            "surname":     surname,
            "dob":         dob,
            "student_id":  sid,
            "institution": inst,
            "version":     version_float
        }
        self.current_q_index = 0
        self.total_score     = 0
        self.answers         = []

        self.show_question()

    # ── SURVEY QUESTIONS ──────────────────────────────────
    def show_question(self):
        self.clear_window()

        q          = self.selected_questions[self.current_q_index]
        total_qs   = len(self.selected_questions)
        progress   = (self.current_q_index / total_qs) * 100

        # Progress bar
        tk.Label(self.root,
                 text=f"Question {self.current_q_index + 1} of {total_qs}",
                 font=("Arial", 11, "bold")).pack(pady=(12, 2))

        bar = ttk.Progressbar(self.root, length=400,
                              mode="determinate", value=progress)
        bar.pack(pady=(0, 10))

        # Question text
        tk.Label(self.root, text=q["q"],
                 wraplength=440, justify="left",
                 font=("Arial", 11)).pack(padx=20, pady=8)

        # Options
        self.selected_option = tk.IntVar(value=-1)
        for i, (opt_text, _) in enumerate(q["opts"], start=1):
            tk.Radiobutton(self.root,
                           text=opt_text,
                           variable=self.selected_option,
                           value=i,
                           anchor="w",
                           font=("Arial", 10)).pack(padx=40, fill="x")

        tk.Button(self.root, text="Next →",
                  width=14, command=self.submit_answer).pack(pady=14)

    def submit_answer(self):
        choice = self.selected_option.get()
        if choice == -1:
            return messagebox.showerror("Error", "Please select an option before continuing.")

        q         = self.selected_questions[self.current_q_index]
        opt_text, score = q["opts"][choice - 1]

        self.total_score += score
        self.answers.append({
            "question":        q["q"],
            "selected_option": opt_text,
            "score":           score
        })

        self.current_q_index += 1

        if self.current_q_index >= len(self.selected_questions):
            self.finish_survey()
        else:
            self.show_question()

    # ── RESULTS SCREEN ────────────────────────────────────
    def finish_survey(self):
        self.record["total_score"] = self.total_score
        self.record["result"]      = interpret_score(self.total_score)
        self.record["answers"]     = self.answers

        self.clear_window()

        tk.Label(self.root, text="Survey Complete!",
                 font=("Arial", 17, "bold")).pack(pady=14)

        # Score box
        frame = tk.Frame(self.root, bd=2, relief="groove", padx=16, pady=12)
        frame.pack(pady=8)

        tk.Label(frame,
                 text=f"Total Score:  {self.total_score}  / {len(self.selected_questions) * 4}",
                 font=("Arial", 13)).pack()
        tk.Label(frame,
                 text=f"Recall Level:  {self.record['result']}",
                 font=("Arial", 13, "bold"), fg="#2E75B6").pack(pady=4)

        # Score legend hint
        tk.Label(self.root,
                 text="Higher score = more frequent & effective active recall use",
                 font=("Arial", 9), fg="grey").pack(pady=2)

        tk.Button(self.root, text="💾  Save Result",
                  width=20, command=self.save_result).pack(pady=8)
        tk.Button(self.root, text="🏠  Back to Menu",
                  width=20, command=self.main_menu).pack(pady=4)

    def save_result(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            initialfile=f"result_{self.record['student_id']}.json",
            filetypes=[("JSON files", "*.json")]
        )
        if not path:
            return
        save_json(path, self.record)
        used_files.add(path)
        messagebox.showinfo("Saved", f"Result saved to:\n{path}")


# -------- RUN --------
if __name__ == "__main__":
    root = tk.Tk()
    app  = SurveyApp(root)
    root.mainloop()
