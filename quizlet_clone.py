import tkinter as tk
from tkinter import messagebox
import os
import csv

def load_vocabulary_from_csv(filename="vocabulary.csv"):
    """Đọc hàng nghìn từ vựng từ file CSV và tự động chia thành các phần 20 từ"""
    decks = {}
    all_cards = []
    
    if os.path.exists(filename):
        with open(filename, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:
                    all_cards.append({"term": row[0].strip(), "definition": row[1].strip()})
    else:
        # Dữ liệu dự phòng nếu chưa tạo file csv
        all_cards = [
            {"term": "acerbic", "definition": "(adj.) harsh or sharply critical in tone, or bitter in taste."},
            {"term": "ubiquitous", "definition": "(adj.) present, appearing, or found everywhere."}
        ]

    # Tự động chia nhóm mỗi phần 20 từ (1000 từ sẽ tự động thành 50 phần, 10000 từ thành 500 phần)
    chunk_size = 20
    for i in range(0, len(all_cards), chunk_size):
        chunk = all_cards[i:i + chunk_size]
        part_num = (i // chunk_size) + 1
        deck_name = f"Phần {part_num}: IELTS Vocab ({i+1}-{min(i+chunk_size, len(all_cards))})"
        decks[deck_name] = chunk
        
    return decks

# Tải tự động toàn bộ kho từ vựng khủng từ file ngoài
IELTS_DECKS = load_vocabulary_from_csv("vocabulary.csv")

class AnkiStyleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Massive IELTS Flashcards (File-based)")
        self.root.geometry("650x550")
        self.root.config(bg="#1e1e2f")

        self.deck_names = list(IELTS_DECKS.keys())
        if not self.deck_names:
            messagebox.showerror("Lỗi", "Không tìm thấy từ vựng trong file vocabulary.csv!")
            root.destroy()
            return

        self.current_deck_name = self.deck_names[0]
        self.cards = IELTS_DECKS[self.current_deck_name]
        self.current_index = 0
        self.is_flipped = False

        self.stats = {"Xem lại": 0, "Khó": 0, "Ổn": 0, "Dễ": 0}

        self.create_widgets()
        self.load_card()

    def create_widgets(self):
        # --- TOP BAR ---
        self.top_frame = tk.Frame(self.root, bg="#1e1e2f")
        self.top_frame.pack(fill="x", padx=20, pady=15)

        self.back_btn = tk.Button(self.top_frame, text="☰ Chọn phần học", font=("Arial", 11, "bold"), bg="#2d2d44", fg="white", bd=0, padx=10, pady=5, command=self.select_deck_menu)
        self.back_btn.pack(side="left")

        self.progress_label = tk.Label(self.top_frame, text="0 / 20", font=("Arial", 14, "bold"), bg="#1e1e2f", fg="white")
        self.progress_label.pack(side="right", padx=10)

        # --- THANH TIẾN ĐỘ ---
        self.canvas_progress = tk.Canvas(self.root, height=6, bg="#2d2d44", highlightthickness=0)
        self.canvas_progress.pack(fill="x", padx=30, pady=5)
        self.progress_line = self.canvas_progress.create_rectangle(0, 0, 0, 6, fill="#ff9800", width=0)

        # --- CARD KHUNG CHÍNH ---
        self.card_frame = tk.Frame(self.root, bg="#27273a", bd=0, relief="flat")
        self.card_frame.pack(fill="both", expand=True, padx=30, pady=15)

        self.status_tag = tk.Label(self.card_frame, text="Mới", font=("Arial", 10, "bold"), bg="#3e3e59", fg="#b0b0c3", padx=8, pady=3)
        self.status_tag.place(x=25, y=20)

        self.card_text = tk.Label(self.card_frame, text="", font=("Arial", 24, "bold"), bg="#27273a", fg="white", wraplength=500, justify="center")
        self.card_text.place(relx=0.5, rely=0.5, anchor="center")

        # --- FOOTER ---
        self.flip_btn = tk.Button(self.root, text="LẬT XEM ĐỊNH NGHĨA", font=("Arial", 12, "bold"), bg="#3b82f6", fg="white", padx=20, pady=12, bd=0, command=self.flip_card)
        self.flip_btn.pack(fill="x", padx=30, pady=10)

        self.rating_frame = tk.Frame(self.root, bg="#1e1e2f")
        
        btn_configs = [
            ("Xem lại\n< 1 phút", "#ef4444", "Xem lại"),
            ("Khó\n< 5 phút", "#f97316", "Khó"),
            ("Ổn\n< 10 phút", "#3b82f6", "Ổn"),
            ("Dễ\n4 ngày", "#10b981", "Dễ")
        ]
        
        for text, color, key in btn_configs:
            b = tk.Button(self.rating_frame, text=text, font=("Arial", 10, "bold"), bg=color, fg="white", padx=10, pady=8, bd=0, command=lambda k=key: self.rate_card(k))
            b.pack(side="left", expand=True, fill="x", padx=4)

    def load_card(self):
        if self.current_index < len(self.cards):
            self.is_flipped = False
            total = len(self.cards)
            self.progress_label.config(text=f"{self.current_index} / {total}")
            
            w = 590 * (self.current_index / total)
            self.canvas_progress.coords(self.progress_line, 0, 0, w, 6)

            self.status_tag.config(text="Mới", bg="#3e3e59", fg="#b0b0c3")
            self.card_text.config(text=self.cards[self.current_index]["term"], fg="white", font=("Arial", 28, "bold"))
            
            self.rating_frame.pack_forget()
            self.flip_btn.pack(fill="x", padx=30, pady=10)
        else:
            self.show_summary()

    def flip_card(self):
        if not self.is_flipped:
            self.is_flipped = True
            self.status_tag.config(text="Định nghĩa (Anh - Anh)", bg="#065f46", fg="#34d399")
            self.card_text.config(text=self.cards[self.current_index]["definition"], fg="#34d399", font=("Arial", 18))
            
            self.flip_btn.pack_forget()
            self.rating_frame.pack(fill="x", padx=30, pady=10)

    def rate_card(self, rating):
        self.stats[rating] += 1
        self.current_index += 1
        self.load_card()

    def show_summary(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        summary_frame = tk.Frame(self.root, bg="#27273a", bd=0)
        summary_frame.pack(fill="both", expand=True, padx=40, pady=30)

        tk.Label(summary_frame, text=f"🎉 Hoàn thành {self.current_deck_name}!", font=("Arial", 18, "bold"), bg="#27273a", fg="white").pack(pady=15)
        
        tk.Label(summary_frame, text=f"🔴 Xem lại: {self.stats['Xem lại']}", font=("Arial", 13), bg="#27273a", fg="#ef4444").pack(pady=3)
        tk.Label(summary_frame, text=f"🟠 Khó: {self.stats['Khó']}", font=("Arial", 13), bg="#27273a", fg="#f97316").pack(pady=3)
        tk.Label(summary_frame, text=f"🔵 Ổn: {self.stats['Ổn']}", font=("Arial", 13), bg="#27273a", fg="#3b82f6").pack(pady=3)
        tk.Label(summary_frame, text=f"🟢 Dễ: {self.stats['Dễ']}", font=("Arial", 13), bg="#27273a", fg="#10b981").pack(pady=3)

        restart_btn = tk.Button(summary_frame, text="Học lại phần này", font=("Arial", 11, "bold"), bg="#3b82f6", fg="white", width=25, pady=8, bd=0, command=self.restart)
        restart_btn.pack(pady=10)

        select_other_btn = tk.Button(summary_frame, text="📚 Chọn phần học khác", font=("Arial", 11, "bold"), bg="#10b981", fg="white", width=25, pady=8, bd=0, command=self.select_deck_menu)
        select_other_btn.pack(pady=5)

    def restart(self):
        self.root.destroy()
        new_root = tk.Tk()
        AnkiStyleApp(new_root)
        new_root.mainloop()

    def select_deck_menu(self):
        select_window = tk.Toplevel(self.root)
        select_window.title("Chọn bộ từ vựng")
        select_window.geometry("450x450")
        select_window.config(bg="#1e1e2f")

        tk.Label(select_window, text="📚 Chọn phần học từ vựng", font=("Arial", 13, "bold"), bg="#1e1e2f", fg="white").pack(pady=15)

        # Thanh cuộn danh sách hàng trăm phần học
        canvas_list = tk.Canvas(select_window, bg="#1e1e2f", highlightthickness=0)
        scrollbar = tk.Scrollbar(select_window, orient="vertical", command=canvas_list.yview)
        scrollable_frame = tk.Frame(canvas_list, bg="#1e1e2f")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas_list.configure(scrollregion=canvas_list.bbox("all"))
        )

        canvas_list.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas_list.configure(yscrollcommand=scrollbar.set)

        for deck_name in IELTS_DECKS.keys():
            btn = tk.Button(scrollable_frame, text=deck_name, font=("Arial", 10), bg="#27273a", fg="white", width=38, pady=6, bd=0,
                            command=lambda d=deck_name: self.load_specific_deck(d, select_window))
            btn.pack(pady=3)

        canvas_list.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")

    def load_specific_deck(self, deck_name, win):
        self.current_deck_name = deck_name
        self.cards = IELTS_DECKS[deck_name]
        self.current_index = 0
        self.stats = {"Xem lại": 0, "Khó": 0, "Ổn": 0, "Dễ": 0}
        win.destroy()
        
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_widgets()
        self.load_card()

if __name__ == "__main__":
    root = tk.Tk()
    app = AnkiStyleApp(root)
    root.mainloop()