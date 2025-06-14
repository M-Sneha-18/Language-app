import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
import datetime

# Constants & Styles
FONT_FAMILY = "Times New Roman"
FONT_BOLD = (FONT_FAMILY, 14, "bold")
FONT_NORMAL = (FONT_FAMILY, 12)
BG_COLOR = "#f0f0f0"
BTN_COLOR = "#007acc"
BTN_FG = "#ffffff"
QUIZ_TIME_PER_QUESTION = 15  # seconds

# Data files
PROGRESS_FILE = "progress.json"
LEADERBOARD_FILE = "leaderboard.json"
FORUM_FILE = "forum.json"

# Vocabulary Data
vocab_data = {
    "Greetings": {
        "English": ["Hi", "Hello", "Good morning", "Good evening", "Good night", "Sorry", "Thank you", "Bye"],
        "Arabic": ["مرحبا", "أهلاً", "صباح الخير", "مساء الخير", "تصبح على خير", "آسف", "شكراً", "وداعا"],
        "French": ["Salut", "Bonjour", "Bon matin", "Bonsoir", "Bonne nuit", "Désolé", "Merci", "Au revoir"],
        "Hindi": ["नमस्ते", "हैलो", "सुप्रभात", "शुभ संध्या", "शुभ रात्रि", "माफ़ कीजिये", "धन्यवाद", "अलविदा"],
        "Italian": ["Ciao", "Salve", "Buongiorno", "Buonasera", "Buonanotte", "Scusa", "Grazie", "Arrivederci"],
        "German": ["Hallo", "Guten Tag", "Guten Morgen", "Guten Abend", "Gute Nacht", "Entschuldigung", "Danke", "Tschüss"],
        "Chinese": ["你好", "您好", "早上好", "晚上好", "晚安", "对不起", "谢谢", "再见"],
        "Korean": ["안녕", "여보세요", "좋은 아침", "좋은 저녁", "안녕히 주무세요", "죄송합니다", "감사합니다", "안녕히 가세요"],
    },
    "Colors": {
        "English": ["Red", "Blue", "Green", "Yellow", "Black", "White"],
        "Arabic": ["أحمر", "أزرق", "أخضر", "أصفر", "أسود", "أبيض"],
        "French": ["Rouge", "Bleu", "Vert", "Jaune", "Noir", "Blanc"],
        "Hindi": ["लाल", "नीला", "हरा", "पीला", "काला", "सफेद"],
        "Italian": ["Rosso", "Blu", "Verde", "Giallo", "Nero", "Bianco"],
        "German": ["Rot", "Blau", "Grün", "Gelb", "Schwarz", "Weiß"],
        "Chinese": ["红色", "蓝色", "绿色", "黄色", "黑色", "白色"],
        "Korean": ["빨강", "파랑", "초록", "노랑", "검정", "하양"],
    },
    "Food": {
        "English": ["Bread", "Rice", "Milk", "Water", "Apple", "Egg"],
        "Arabic": ["خبز", "أرز", "حليب", "ماء", "تفاح", "بيض"],
        "French": ["Pain", "Riz", "Lait", "Eau", "Pomme", "Œuf"],
        "Hindi": ["रोटी", "चावल", "दूध", "पानी", "सेब", "अंडा"],
        "Italian": ["Pane", "Riso", "Latte", "Acqua", "Mela", "Uovo"],
        "German": ["Brot", "Reis", "Milch", "Wasser", "Apfel", "Ei"],
        "Chinese": ["面包", "米饭", "牛奶", "水", "苹果", "蛋"],
        "Korean": ["빵", "밥", "우유", "물", "사과", "계란"],
    },
    "Water": {
        "English": ["Water", "Drink", "Thirsty", "Wet", "Pour", "River"],
        "Arabic": ["ماء", "شرب", "عطشان", "رطب", "صب", "نهر"],
        "French": ["Eau", "Boire", "Assoiffé", "Mouillé", "Verser", "Rivière"],
        "Hindi": ["पानी", "पीना", "प्यासा", "गीला", "डालना", "नदी"],
        "Italian": ["Acqua", "Bere", "Assetato", "Bagnato", "Versare", "Fiume"],
        "German": ["Wasser", "Trinken", "Durstig", "Nass", "Gießen", "Fluss"],
        "Chinese": ["水", "喝", "口渴", "湿", "倒", "河"],
        "Korean": ["물", "마시다", "목마른", "젖은", "붓다", "강"],
    },
    "Gender": {
        "English": ["Male", "Female", "Boy", "Girl", "Man", "Woman"],
        "Arabic": ["ذكر", "أنثى", "ولد", "بنت", "رجل", "امرأة"],
        "French": ["Mâle", "Femelle", "Garçon", "Fille", "Homme", "Femme"],
        "Hindi": ["पुरुष", "महिला", "लड़का", "लड़की", "आदमी", "औरत"],
        "Italian": ["Maschio", "Femmina", "Ragazzo", "Ragazza", "Uomo", "Donna"],
        "German": ["Männlich", "Weiblich", "Junge", "Mädchen", "Mann", "Frau"],
        "Chinese": ["男", "女", "男孩", "女孩", "男人", "女人"],
        "Korean": ["남성", "여성", "소년", "소녀", "남자", "여자"],
    },
    "Family Members": {
        "English": ["Father", "Mother", "Brother", "Sister", "Son", "Daughter"],
        "Arabic": ["أب", "أم", "أخ", "أخت", "ابن", "ابنة"],
        "French": ["Père", "Mère", "Frère", "Sœur", "Fils", "Fille"],
        "Hindi": ["पिता", "माता", "भाई", "बहन", "बेटा", "बेटी"],
        "Italian": ["Padre", "Madre", "Fratello", "Sorella", "Figlio", "Figlia"],
        "German": ["Vater", "Mutter", "Bruder", "Schwester", "Sohn", "Tochter"],
        "Chinese": ["父亲", "母亲", "兄弟", "姐妹", "儿子", "女儿"],
        "Korean": ["아버지", "어머니", "형제", "자매", "아들", "딸"],
    },
    "School": {
        "English": ["School", "Teacher", "Student", "Book", "Pen", "Classroom"],
        "Arabic": ["مدرسة", "معلم", "طالب", "كتاب", "قلم", "فصل"],
        "French": ["École", "Enseignant", "Étudiant", "Livre", "Stylo", "Salle de classe"],
        "Hindi": ["स्कूल", "शिक्षक", "छात्र", "किताब", "कलम", "कक्षा"],
        "Italian": ["Scuola", "Insegnante", "Studente", "Libro", "Penna", "Aula"],
        "German": ["Schule", "Lehrer", "Schüler", "Buch", "Stift", "Klassenzimmer"],
        "Chinese": ["学校", "老师", "学生", "书", "笔", "教室"],
        "Korean": ["학교", "선생님", "학생", "책", "펜", "교실"],
    },
}

# Utility functions for file handling
def load_json(filename, default):
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return default
    else:
        return default

def save_json(filename, data):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving {filename}: {e}")

# Load or initialize data
progress = load_json(PROGRESS_FILE, {
    "lessons_completed": [],
    "quiz_scores": {},
    "achievements": [],
    "daily_challenge_date": "",
    "daily_challenge_score": 0
})

leaderboard = load_json(LEADERBOARD_FILE, {})

forum_messages = load_json(FORUM_FILE, [])

def save_progress():
    save_json(PROGRESS_FILE, progress)

def save_leaderboard():
    save_json(LEADERBOARD_FILE, leaderboard)

def save_forum_messages():
    save_json(FORUM_FILE, forum_messages)

# Main App Class
class LanguageApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Language Learning App")
        self.geometry("900x700")
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)

        self.create_menu()
        self.create_main_widgets()

    def create_menu(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        features_menu = tk.Menu(menu_bar, tearoff=0)
        features_menu.add_command(label="Achievements & Progress", command=self.show_achievements)
        features_menu.add_command(label="Leaderboard", command=self.show_leaderboard)
        features_menu.add_command(label="Daily Challenge", command=self.show_daily_challenge)
        features_menu.add_command(label="Community Forum", command=self.show_forum)
        menu_bar.add_cascade(label="Features", menu=features_menu)

    def create_main_widgets(self):
        tk.Label(self, text="Welcome to Language Learning App", font=FONT_BOLD, bg=BG_COLOR).pack(pady=25)
        start_btn = tk.Button(self, text="Start Quiz", font=FONT_BOLD, bg=BTN_COLOR, fg=BTN_FG, bd=0, padx=20, pady=10,
                              activebackground="#005f9e", command=self.start_quiz)
        start_btn.pack(pady=10)

    def start_quiz(self):
        QuizWindow(self)

    def show_achievements(self):
        AchievementsWindow(self)

    def show_leaderboard(self):
        LeaderboardWindow(self)

    def show_daily_challenge(self):
        DailyChallengeWindow(self)

    def show_forum(self):
        ForumWindow(self)

# Quiz Window
class QuizWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Quiz")
        self.geometry("700x550")
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)

        self.selected_category = None
        self.selected_language = None
        self.questions = []
        self.current_index = 0
        self.score = 0
        self.time_left = QUIZ_TIME_PER_QUESTION
        self.timer_id = None

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Select Category:", font=FONT_BOLD, bg=BG_COLOR).pack(pady=(15,5))
        self.category_var = tk.StringVar()
        categories = list(vocab_data.keys())
        self.category_menu = tk.OptionMenu(self, self.category_var, *categories, command=self.on_category_selected)
        self.category_menu.config(font=FONT_NORMAL)
        self.category_menu.pack()

        tk.Label(self, text="Select Language:", font=FONT_BOLD, bg=BG_COLOR).pack(pady=(15,5))
        self.language_var = tk.StringVar()
        self.language_menu = tk.OptionMenu(self, self.language_var, "")
        self.language_menu.config(font=FONT_NORMAL)
        self.language_menu.pack()

        self.start_btn = tk.Button(self, text="Start Quiz", font=FONT_BOLD, bg=BTN_COLOR, fg=BTN_FG, bd=0, padx=15, pady=8,
                                   activebackground="#005f9e", state="disabled", command=self.start_quiz)
        self.start_btn.pack(pady=25)

    def on_category_selected(self, value):
        self.selected_category = value
        languages = list(vocab_data.get(value, {}).keys())
        self.language_var.set('')
        menu = self.language_menu["menu"]
        menu.delete(0, "end")
        for lang in languages:
            menu.add_command(label=lang, command=lambda v=lang: self.language_var.set(v))
        self.language_var.trace_add('write', self.on_language_selected)
        self.start_btn.config(state="disabled")

    def on_language_selected(self, *args):
        self.selected_language = self.language_var.get()
        if self.selected_language:
            self.start_btn.config(state="normal")
        else:
            self.start_btn.config(state="disabled")

    def start_quiz(self):
        category = self.selected_category
        language = self.selected_language
        if not category or not language:
            messagebox.showwarning("Selection Error", "Please select both category and language.")
            return

        # Prepare questions as list of tuples (English word, translated word)
        english_words = vocab_data[category]["English"]
        translated_words = vocab_data[category].get(language, [])
        if not translated_words:
            messagebox.showerror("Data Error", "No vocabulary for selected language/category.")
            return

        self.questions = list(zip(english_words, translated_words))
        self.current_index = 0
        self.score = 0

        # Clear old widgets and start quiz UI
        for widget in self.winfo_children():
            widget.destroy()

        self.question_label = tk.Label(self, text="", font=FONT_BOLD, bg=BG_COLOR, wraplength=600)
        self.question_label.pack(pady=20)

        self.var_answer = tk.StringVar()
        self.radio_buttons = []
        for i in range(4):
            rb = tk.Radiobutton(self, text="", variable=self.var_answer, value="", font=FONT_NORMAL, bg=BG_COLOR, anchor="w")
            rb.pack(fill="x", padx=100, pady=3)
            self.radio_buttons.append(rb)

        self.timer_label = tk.Label(self, text="", font=FONT_NORMAL, bg=BG_COLOR)
        self.timer_label.pack(pady=10)

        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=15)

        self.submit_btn = tk.Button(btn_frame, text="Submit", font=FONT_BOLD, bg=BTN_COLOR, fg=BTN_FG, bd=0,
                                    padx=15, pady=8, activebackground="#005f9e", command=self.submit_answer)
        self.submit_btn.grid(row=0, column=0, padx=20)

        self.skip_btn = tk.Button(btn_frame, text="Skip", font=FONT_BOLD, bg="#888", fg="#eee", bd=0,
                                  padx=15, pady=8, activebackground="#555555", command=self.skip_question)
        self.skip_btn.grid(row=0, column=1, padx=20)

        self.show_question()

    def show_question(self):
        if self.current_index >= len(self.questions):
            self.finish_quiz()
            return

        self.time_left = QUIZ_TIME_PER_QUESTION
        self.var_answer.set("")

        english_word, correct_translation = self.questions[self.current_index]
        self.question_label.config(text=f"What is the translation of '{english_word}'?")

        # Prepare options: correct + 3 random others
        category = self.selected_category
        language = self.selected_language
        all_words = vocab_data[category].get(language, [])
        options = [correct_translation]

        # Add random options excluding correct
        import random
        others = [w for w in all_words if w != correct_translation]
        options.extend(random.sample(others, k=min(3, len(others))))
        random.shuffle(options)

        for i, option in enumerate(options):
            self.radio_buttons[i].config(text=option, value=option, state="normal")
            self.radio_buttons[i].pack()
        for i in range(len(options), 4):
            self.radio_buttons[i].pack_forget()

        self.update_timer()

    def update_timer(self):
        self.timer_label.config(text=f"Time left: {self.time_left} seconds")
        if self.time_left <= 0:
            self.submit_answer(timeout=True)
            return
        self.time_left -= 1
        self.timer_id = self.after(1000, self.update_timer)

    def submit_answer(self, timeout=False):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None

        english_word, correct_translation = self.questions[self.current_index]
        selected = self.var_answer.get()

        if timeout:
            messagebox.showinfo("Time's up!", f"Time over! The correct answer was '{correct_translation}'.")
        else:
            if not selected:
                messagebox.showwarning("No Answer", "Please select an answer or skip the question.")
                self.update_timer()
                return
            if selected == correct_translation:
                self.score += 1

        self.current_index += 1
        self.show_question()

    def skip_question(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        self.current_index += 1
        self.show_question()

    def finish_quiz(self):
        # Save score to progress
        key = f"{self.selected_category}_{self.selected_language}"
        prev_best = progress["quiz_scores"].get(key, 0)
        if self.score > prev_best:
            progress["quiz_scores"][key] = self.score
        if key not in progress["lessons_completed"]:
            progress["lessons_completed"].append(key)
        save_progress()

        # Ask for username to record leaderboard
        username = simpledialog.askstring("Quiz Completed",
                                          f"Your score: {self.score}/{len(self.questions)}\nEnter your username for leaderboard:")
        if username:
            self.update_leaderboard(username, self.selected_category, self.selected_language, self.score)

        messagebox.showinfo("Quiz Finished", f"Your final score: {self.score} / {len(self.questions)}")
        self.destroy()

    def update_leaderboard(self, username, category, language, score):
        key = f"{category}_{language}"
        if key not in leaderboard:
            leaderboard[key] = []
        leaderboard[key].append({"username": username, "score": score, "date": datetime.date.today().isoformat()})
        # Keep only top 10 scores sorted descending
        leaderboard[key].sort(key=lambda x: x["score"], reverse=True)
        leaderboard[key] = leaderboard[key][:10]
        save_leaderboard()

# Achievements and Progress Window
class AchievementsWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Achievements & Progress")
        self.geometry("700x600")
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Achievements & Progress", font=FONT_BOLD, bg=BG_COLOR).pack(pady=15)

        # Achievements
        achv_frame = tk.LabelFrame(self, text="Achievements", font=FONT_BOLD, bg=BG_COLOR, padx=15, pady=15)
        achv_frame.pack(fill="both", expand=True, padx=20, pady=10)

        achievements_list = progress.get("achievements", [])

        if not achievements_list:
            tk.Label(achv_frame, text="No achievements yet. Complete quizzes to earn achievements!",
                     font=FONT_NORMAL, bg=BG_COLOR).pack()
        else:
            for achv in achievements_list:
                tk.Label(achv_frame, text=f"- {achv}", font=FONT_NORMAL, bg=BG_COLOR, anchor="w").pack(fill="x")

        # Progress
        prog_frame = tk.LabelFrame(self, text="Progress", font=FONT_BOLD, bg=BG_COLOR, padx=15, pady=15)
        prog_frame.pack(fill="both", expand=True, padx=20, pady=10)

        lessons_completed = progress.get("lessons_completed", [])
        tk.Label(prog_frame, text=f"Lessons Completed: {len(lessons_completed)} / {len(vocab_data)}",
                 font=FONT_NORMAL, bg=BG_COLOR).pack(anchor="w")

        # Show quiz scores
        tk.Label(prog_frame, text="Quiz Scores:", font=FONT_BOLD, bg=BG_COLOR).pack(anchor="w", pady=(10, 0))
        quiz_scores = progress.get("quiz_scores", {})
        if not quiz_scores:
            tk.Label(prog_frame, text="No quizzes taken yet.", font=FONT_NORMAL, bg=BG_COLOR).pack(anchor="w")
        else:
            for key, score in quiz_scores.items():
                cat, lang = key.split("_", 1)
                tk.Label(prog_frame, text=f"{cat} - {lang}: {score}", font=FONT_NORMAL, bg=BG_COLOR).pack(anchor="w")

# Leaderboard Window
class LeaderboardWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Leaderboard")
        self.geometry("700x600")
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)
        self.selected_category = tk.StringVar()
        self.selected_language = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Leaderboard", font=FONT_BOLD, bg=BG_COLOR).pack(pady=15)

        tk.Label(self, text="Select Category:", font=FONT_NORMAL, bg=BG_COLOR).pack()
        categories = list(vocab_data.keys())
        self.selected_category.set(categories[0])
        category_menu = tk.OptionMenu(self, self.selected_category, *categories, command=self.update_leaderboard)
        category_menu.config(font=FONT_NORMAL)
        category_menu.pack()

        tk.Label(self, text="Select Language:", font=FONT_NORMAL, bg=BG_COLOR).pack(pady=(10,0))
        self.selected_language.set("English")
        language_menu = tk.OptionMenu(self, self.selected_language, "English", "Arabic", "French", "Hindi",
                                      "Italian", "German", "Chinese", "Korean", command=self.update_leaderboard)
        language_menu.config(font=FONT_NORMAL)
        language_menu.pack()

        self.leaderboard_frame = tk.Frame(self, bg=BG_COLOR)
        self.leaderboard_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.update_leaderboard()

    def update_leaderboard(self, *args):
        for widget in self.leaderboard_frame.winfo_children():
            widget.destroy()

        cat = self.selected_category.get()
        lang = self.selected_language.get()
        key = f"{cat}_{lang}"

        scores = leaderboard.get(key, [])
        if not scores:
            tk.Label(self.leaderboard_frame, text="No leaderboard data available for this category/language.",
                     font=FONT_NORMAL, bg=BG_COLOR).pack()
            return

        for idx, entry in enumerate(scores, start=1):
            text = f"{idx}. {entry['username']} - {entry['score']} points ({entry['date']})"
            tk.Label(self.leaderboard_frame, text=text, font=FONT_NORMAL, bg=BG_COLOR, anchor="w").pack(fill="x")

# Daily Challenge Window
class DailyChallengeWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Daily Challenge")
        self.geometry("700x550")
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)

        self.today = datetime.date.today().isoformat()
        self.completed_today = progress.get("daily_challenge_date", "") == self.today
        self.score = 0
        self.time_left = QUIZ_TIME_PER_QUESTION
        self.timer_id = None
        self.questions = []
        self.current_index = 0

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Daily Challenge", font=FONT_BOLD, bg=BG_COLOR).pack(pady=15)

        if self.completed_today:
            tk.Label(self, text=f"You have completed today's challenge!\nScore: {progress.get('daily_challenge_score', 0)}",
                     font=FONT_NORMAL, bg=BG_COLOR).pack(pady=30)
            tk.Button(self, text="Close", font=FONT_BOLD, bg=BTN_COLOR, fg=BTN_FG, bd=0, padx=15, pady=8,
                      activebackground="#005f9e", command=self.destroy).pack(pady=10)
        else:
            tk.Label(self, text="Select Category and Language for Today's Challenge", font=FONT_NORMAL, bg=BG_COLOR).pack(pady=10)

            tk.Label(self, text="Category:", font=FONT_NORMAL, bg=BG_COLOR).pack()
            categories = list(vocab_data.keys())
            self.category_var = tk.StringVar()
            self.category_var.set(categories[0])
            category_menu = tk.OptionMenu(self, self.category_var, *categories)
            category_menu.config(font=FONT_NORMAL)
            category_menu.pack()

            tk.Label(self, text="Language:", font=FONT_NORMAL, bg=BG_COLOR).pack(pady=(10,0))
            languages = ["English", "Arabic", "French", "Hindi", "Italian", "German", "Chinese", "Korean"]
            self.language_var = tk.StringVar()
            self.language_var.set("English")
            language_menu = tk.OptionMenu(self, self.language_var, *languages)
            language_menu.config(font=FONT_NORMAL)
            language_menu.pack()

            tk.Button(self, text="Start Challenge", font=FONT_BOLD, bg=BTN_COLOR, fg=BTN_FG, bd=0, padx=15, pady=8,
                      activebackground="#005f9e", command=self.start_challenge).pack(pady=20)

    def start_challenge(self):
        category = self.category_var.get()
        language = self.language_var.get()

        english_words = vocab_data[category]["English"]
        translated_words = vocab_data[category].get(language, [])
        if not translated_words:
            messagebox.showerror("Data Error", "No vocabulary for selected language/category.")
            return

        # Use first 5 words for challenge or less
        self.questions = list(zip(english_words, translated_words))[:5]
        self.current_index = 0
        self.score = 0

        for widget in self.winfo_children():
            widget.destroy()

        self.question_label = tk.Label(self, text="", font=FONT_BOLD, bg=BG_COLOR, wraplength=600)
        self.question_label.pack(pady=20)

        self.var_answer = tk.StringVar()
        self.radio_buttons = []
        for i in range(4):
            rb = tk.Radiobutton(self, text="", variable=self.var_answer, value="", font=FONT_NORMAL, bg=BG_COLOR, anchor="w")
            rb.pack(fill="x", padx=100, pady=3)
            self.radio_buttons.append(rb)

        self.timer_label = tk.Label(self, text="", font=FONT_NORMAL, bg=BG_COLOR)
        self.timer_label.pack(pady=10)

        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=15)

        self.submit_btn = tk.Button(btn_frame, text="Submit", font=FONT_BOLD, bg=BTN_COLOR, fg=BTN_FG, bd=0,
                                    padx=15, pady=8, activebackground="#005f9e", command=self.submit_answer)
        self.submit_btn.grid(row=0, column=0, padx=20)

        self.skip_btn = tk.Button(btn_frame, text="Skip", font=FONT_BOLD, bg="#888", fg="#eee", bd=0,
                                  padx=15, pady=8, activebackground="#555555", command=self.skip_question)
        self.skip_btn.grid(row=0, column=1, padx=20)

        self.show_question()

    def show_question(self):
        if self.current_index >= len(self.questions):
            self.finish_challenge()
            return

        english_word, correct_translation = self.questions[self.current_index]
        self.question_label.config(text=f"Translate the word: '{english_word}'")

        # Generate options: include correct translation + 3 random others from the same language
        all_translations = vocab_data[self.category_var.get()].get(self.language_var.get(), [])
        options = set()
        options.add(correct_translation)
        while len(options) < 4 and len(all_translations) >= 4:
            options.add(random.choice(all_translations))
        options = list(options)
        random.shuffle(options)

        self.var_answer.set(None)
        for i, option in enumerate(options):
            self.radio_buttons[i].config(text=option, value=option, state="normal")
            self.radio_buttons[i].pack()
        for i in range(len(options), 4):
            self.radio_buttons[i].pack_forget()

        self.time_left = QUIZ_TIME_PER_QUESTION
        self.update_timer()

    def update_timer(self):
        self.timer_label.config(text=f"Time left: {self.time_left} seconds")
        if self.time_left <= 0:
            self.submit_answer(timeout=True)
            return
        self.time_left -= 1
        self.timer_id = self.after(1000, self.update_timer)

    def submit_answer(self, timeout=False):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None

        english_word, correct_translation = self.questions[self.current_index]
        selected = self.var_answer.get()

        if timeout:
            messagebox.showinfo("Time's up!", f"Time over! The correct answer was '{correct_translation}'.")
        else:
            if not selected:
                messagebox.showwarning("No Answer", "Please select an answer or skip the question.")
                self.update_timer()
                return
            if selected == correct_translation:
                self.score += 1

        self.current_index += 1
        self.show_question()

    def skip_question(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        self.current_index += 1
        self.show_question()

    def finish_challenge(self):
        progress["daily_challenge_date"] = self.today
        progress["daily_challenge_score"] = self.score
        save_progress()

        messagebox.showinfo("Challenge Finished", f"Your score: {self.score} / {len(self.questions)}")
        self.destroy()


# Main Application Window
class LanguageLearningApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Language Learning App")
        self.geometry("900x700")
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Language Learning App", font=FONT_BOLD, bg=BG_COLOR).pack(pady=20)

        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=40)

        tk.Button(btn_frame, text="Start Quiz", font=FONT_BOLD, bg=BTN_COLOR, fg=BTN_FG, bd=0,
                  padx=30, pady=15, activebackground="#005f9e", command=self.open_quiz).grid(row=0, column=0, padx=20)

        tk.Button(btn_frame, text="Achievements & Progress", font=FONT_BOLD, bg=BTN_COLOR, fg=BTN_FG, bd=0,
                  padx=30, pady=15, activebackground="#005f9e", command=self.open_achievements).grid(row=0, column=1, padx=20)

        tk.Button(btn_frame, text="Leaderboard", font=FONT_BOLD, bg=BTN_COLOR, fg=BTN_FG, bd=0,
                  padx=30, pady=15, activebackground="#005f9e", command=self.open_leaderboard).grid(row=0, column=2, padx=20)

        tk.Button(btn_frame, text="Daily Challenge", font=FONT_BOLD, bg=BTN_COLOR, fg=BTN_FG, bd=0,
                  padx=30, pady=15, activebackground="#005f9e", command=self.open_daily_challenge).grid(row=0, column=3, padx=20)

        tk.Button(self, text="Exit", font=FONT_BOLD, bg="#b22222", fg="#fff", bd=0,
                  padx=30, pady=15, activebackground="#800000", command=self.quit).pack(pady=20)

    def open_quiz(self):
        QuizWindow(self)

    def open_achievements(self):
        AchievementsWindow(self)

    def open_leaderboard(self):
        LeaderboardWindow(self)

    def open_daily_challenge(self):
        DailyChallengeWindow(self)


if __name__ == "__main__":
    app = LanguageLearningApp()
    app.mainloop()




