import tkinter as tk
from tkinter import messagebox
import os
import winsound

class FruitGuessGame:
    def __init__(self, root):
        self.root = root
        self.root.title("World Adventure Guessing Game")
        self.root.geometry("950x650")
        
        #Colors:
        self.bg_dark = "#1A252F"       
        self.bg_panel = "#2C3E50"      
        self.accent_gold = "#F1C40F"    
        self.btn_color = "#34495E"      
        self.text_light = "#ECF0F1"     
        
        self.root.config(bg=self.bg_dark)
        
        #Tracking
        self.score = 0
        self.squares_revealed = 0
        self.current_try = 1 
        self.can_click = True 
        
        # Timer
        self.time_limit = 30  
        self.time_left = self.time_limit
        self.timer_job = None  
        
        # Track our location
        self.current_world_index = 0
        self.current_level_index = 0
        
        # HIGH SCORE
        self.highscore_file = "highscore.txt"
        self.high_score = self.load_high_score()
        
        self.worlds = [
            {
                "world_name": "Fruit World",
                "world_image": "fruits.png",
                "levels": [
                    {
                        "image_file": "fruit1.png",
                        "correct_answer": "Cherry",
                        "grid_size": 3,
                        "options": ["Apple", "Cherry", "Pomegranate", "Lycchee", "Grape", "Tomato"]
                    },
                    {
                        "image_file": "fruit2.png",
                        "correct_answer": "Fig",
                        "grid_size": 4,
                        "options": ["Fig", "Date", "Onion", "Passion Fruit", "Durian", "Jujube"]
                    },
                    {
                        "image_file": "fruit3.png",
                        "correct_answer": "Jackfruit",
                        "grid_size": 5,
                        "options": ["Guava", "Durian", "Pineapple", "Mango", "Jackfruit", "Papaya"]
                    }
                ]
            },
            {
                "world_name": "Vegetable World",
                "world_image": "vegetables.png",
                "levels": [
                    {
                        "image_file": "veg1.png",
                        "correct_answer": "Cabbage",
                        "grid_size": 3,
                        "options": ["Cabbage", "Gourd", "Radish", "Lettuce", "Broccoli", "Turnip"]
                    },
                    {
                        "image_file": "veg2.png",
                        "correct_answer": "Broccoli",
                        "grid_size": 4,
                        "options": ["Cabbage", "Lettuce", "Broccoli", "Cauliflower", "Kale", "Spinach"]
                    },
                    {
                        "image_file": "veg3.png",
                        "correct_answer": "Beetroot",
                        "grid_size": 5,
                        "options": ["Tomato", "Red Pepper", "Raddish", "Red Cabbage", "Chili", "Beetroot"]
                    }
                ]
            }
        ]
        
        # --- PHASE 1: Loading Screen ---
        self.main_label = tk.Label(self.root, text="Loading...", font=("Segoe UI", 50, "bold"), bg=self.bg_dark, fg=self.accent_gold)
        self.main_label.pack(pady=80)
        
        self.fruit_image_label = None
        self.start_button = None
        self.game_frame = None
        
        self.root.after(1000, self.show_world_welcome_screen)

    # GAME AUDIO ENGINE
    def play_sound(self, sound_type):
        """Triggers standard system tones asynchronously to avoid freezing game frames."""
        try:
            if sound_type == "correct":
                winsound.PlaySound("SystemAsterisk", winsound.SND_ASYNC)
            elif sound_type == "wrong":
                winsound.PlaySound("SystemHand", winsound.SND_ASYNC)
            elif sound_type == "tick":
                winsound.PlaySound("SystemDefault", winsound.SND_ASYNC)
        except Exception:
            pass  # Silent fallback if system audio channels are busy

    # HARD DRIVE FILE SAVING SYSTEM
    def load_high_score(self):
        if os.path.exists(self.highscore_file):
            try:
                with open(self.highscore_file, "r") as file:
                    return int(file.read().strip())
            except Exception:
                return 0
        return 0

    def save_new_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            try:
                with open(self.highscore_file, "w") as file:
                    file.write(str(self.high_score))
                return True
            except Exception as e:
                print(f"Error saving high score file: {e}")
        return False

    # GAME COUNTDOWN TIMER
    def start_countdown(self):
        """Begins or ticks forward the level countdown clock thread."""
        if self.time_left > 0:
            self.time_left -= 1
            if hasattr(self, 'timer_label') and self.timer_label.winfo_exists():
                self.timer_label.config(text=f"⏳ Time Remaining: {self.time_left}s")
                # Highlight critical remaining moments in bright red
                if self.time_left <= 5:
                    self.timer_label.config(fg="#E74C3C")
                    self.play_sound("tick")
            self.timer_job = self.root.after(1000, self.start_countdown)
        else:
            self.handle_time_out()

    def stop_countdown(self):
        """Safely untethers running clock processes to clear space for screen rebuilds."""
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

    def handle_time_out(self):
        """Forcibly triggers level failure conditions when countdown reaches 0."""
        self.play_sound("wrong")
        messagebox.showerror("Time's Up!", "⏰ Clock ran out before you made a valid choice! Resetting level...")
        self.reset_current_level()

    # --- PHASE 2: World Interstitial Splash Card ---
    def show_world_welcome_screen(self):
        self.stop_countdown()
        current_world = self.worlds[self.current_world_index]
        world_title = current_world["world_name"]
        total_lvl_count = len(current_world["levels"])
        
        self.main_label.config(text=f"Welcome to {world_title}!", font=("Segoe UI", 32, "bold"), fg=self.accent_gold)
        
        self.sub_label = tk.Label(
            self.root, 
            text=f"This world contains {total_lvl_count} challenges.\n🏆 All-Time High Score Record: {self.high_score} 🏆", 
            font=("Segoe UI", 14, "italic"),
            bg=self.bg_dark,
            fg=self.text_light
        )
        self.sub_label.pack(pady=5)
        
        try:
            self.bg_image = tk.PhotoImage(file=current_world["world_image"])
            self.fruit_image_label = tk.Label(self.root, image=self.bg_image, bg=self.bg_dark)
            self.fruit_image_label.pack(pady=15)
        except Exception:
            self.bg_image = None
            self.fruit_image_label = tk.Label(self.root, text=f"[ Welcome Graphic to {world_title} ]", font=("Segoe UI", 18), bg=self.bg_dark, fg=self.text_light)
            self.fruit_image_label.pack(pady=15)

        self.start_button = tk.Button(
            self.root, text="Enter World", font=("Segoe UI", 14, "bold"), 
            bg="#2ECC71", fg="white", activebackground="#27AE60", activeforeground="white",
            padx=20, pady=5, bd=0, cursor="hand2", command=self.start_game
        )
        self.start_button.pack(pady=15)

    # --- PHASE 3: Clear and Start Gameplay ---
    def start_game(self):
        if self.fruit_image_label:
            self.fruit_image_label.pack_forget()
        if self.start_button:
            self.start_button.pack_forget()
        if hasattr(self, 'sub_label'):
            self.sub_label.pack_forget()
            
        self.setup_gameplay_screen()

    # --- PHASE 4: Core Interactive Game Logic Layout ---
    def setup_gameplay_screen(self):
        self.stop_countdown()
        self.time_left = self.time_limit  
        
        current_world = self.worlds[self.current_world_index]
        current_level_data = current_world["levels"][self.current_level_index]
        
        self.main_label.config(
            text=f"{current_world['world_name']} — Level {self.current_level_index + 1}/{len(current_world['levels'])}", 
            font=("Segoe UI", 20, "bold"), 
            fg=self.text_light
        )
        self.main_label.pack(pady=15)
        
        self.game_frame = tk.Frame(self.root, bg=self.bg_dark)
        self.game_frame.pack(pady=10)
        
        # High contrast canvas background panel
        self.canvas = tk.Canvas(self.game_frame, width=400, height=400, bg="#34495E", highlightthickness=2, highlightbackground=self.accent_gold)
        self.canvas.pack(side=tk.LEFT, padx=20)
        
        try:
            self.active_level_photo = tk.PhotoImage(file=current_level_data["image_file"])
            self.canvas.create_image(200, 200, image=self.active_level_photo)  
        except Exception:
            self.canvas.create_text(200, 200, text=f"[{current_level_data['correct_answer']} Picture]", font=("Segoe UI", 16, "bold"), fill=self.text_light)

        size = current_level_data["grid_size"]
        self.total_squares = size * size
        self.create_grid(rows=size, cols=size)
        
        # Sidebar Assembly Dashboard Panel
        self.sidebar = tk.Frame(self.game_frame, bg=self.bg_panel, padx=20, pady=15, highlightthickness=1, highlightbackground="#465C71")
        self.sidebar.pack(side=tk.RIGHT, padx=20, fill=tk.Y)
        
        self.score_label = tk.Label(self.sidebar, text=f"Total Score: {self.score}", font=("Segoe UI", 16, "bold"), bg=self.bg_panel, fg="#2ECC71")
        self.score_label.pack(pady=5)
        
        self.best_label = tk.Label(self.sidebar, text=f"Record to Beat: {self.high_score}", font=("Segoe UI", 11, "bold"), bg=self.bg_panel, fg="#95A5A6")
        self.best_label.pack(pady=2)
        
        # New countdown visual tracking element 
        self.timer_label = tk.Label(self.sidebar, text=f"⏳ Time Remaining: {self.time_left}s", font=("Segoe UI", 12, "bold"), bg=self.bg_panel, fg=self.accent_gold)
        self.timer_label.pack(pady=8)
        
        self.turn_instruction = tk.Label(self.sidebar, text=f"Grid Complexity: {size}x{size}", font=("Segoe UI", 11, "bold"), bg=self.bg_panel, fg="#9B59B6")
        self.turn_instruction.pack(pady=2)
        
        self.action_instruction = tk.Label(self.sidebar, text="Click a square to reveal!", font=("Segoe UI", 11, "italic"), bg=self.bg_panel, fg="#3498DB")
        self.action_instruction.pack(pady=5)
        
        tk.Label(self.sidebar, text="Make your selection guess:", font=("Segoe UI", 12), bg=self.bg_panel, fg=self.text_light).pack(pady=8)
        
        # Render high fidelity styled answer option choice nodes
        for option in current_level_data["options"]:
            btn = tk.Button(
                self.sidebar, text=option, font=("Segoe UI", 11, "bold"), width=18,
                bg=self.btn_color, fg=self.text_light, activebackground=self.accent_gold, activeforeground=self.bg_dark,
                bd=0, pady=4, cursor="hand2", command=lambda opt=option: self.check_guess(opt)
            )
            btn.pack(pady=4)
            
        # Spin up clock tick thread cycle
        self.start_countdown()

    def create_grid(self, rows, cols):
        w = 400 / cols
        h = 400 / rows
        for r in range(rows):
            for c in range(cols):
                x1, y1 = c * w, r * h
                x2, y2 = x1 + w, y1 + h
                # UPGRADED: Midnight slate covers with gold borders
                sid = self.canvas.create_rectangle(x1, y1, x2, y2, fill="#2C3E50", outline=self.accent_gold, width=1, tags="cover")
                self.canvas.tag_bind(sid, "<Button-1>", lambda e, s=sid: self.reveal_square(s))

    def reveal_square(self, square_id):
        if not self.can_click:
            return  
        self.canvas.delete(square_id)
        self.squares_revealed += 1
        self.can_click = False 
        self.action_instruction.config(text=f"Try #{self.current_try}: Make a guess choice!", fg="#E74C3C")

    def check_guess(self, guessed_fruit):
        current_world = self.worlds[self.current_world_index]
        current_level_data = current_world["levels"][self.current_level_index]
        
        if self.squares_revealed == 0:
            self.play_sound("wrong")
            messagebox.showwarning("Wait!", "You must reveal at least one square before guessing!")
            return

        if guessed_fruit == current_level_data["correct_answer"]:
            self.stop_countdown()  # Halt time consumption loop immediately
            self.play_sound("correct")
            
            points_earned = max(10, 110 - (self.current_try * 10))
            self.score += points_earned
            
            self.save_new_high_score()
            
            messagebox.showinfo("Correct!", f"You got it! It's a {current_level_data['correct_answer']}.\n"
                                            f"You scored {points_earned} points on Try #{self.current_try}!")
            self.advance_game_progression()
        else:
            self.play_sound("wrong")
            if self.squares_revealed >= (self.total_squares - 1):
                self.stop_countdown()
                messagebox.showerror("Game Over", f"Incorrect guess! Game over for this level. The answer was {current_level_data['correct_answer']}!")
                self.reset_current_level() 
            else:
                messagebox.showerror("Wrong!", "That's not correct. Reveal another square and try again!")
                self.current_try += 1
                self.can_click = True
                self.action_instruction.config(text="Reveal another square!", fg="#3498DB")

    def advance_game_progression(self):
        if self.game_frame:
            self.game_frame.destroy()
            
        current_world_data = self.worlds[self.current_world_index]
        self.current_level_index += 1
        
        if self.current_level_index < len(current_world_data["levels"]):
            self.squares_revealed = 0
            self.current_try = 1
            self.can_click = True
            self.setup_gameplay_screen()
        else:
            self.current_world_index += 1
            self.current_level_index = 0 
            
            self.squares_revealed = 0
            self.current_try = 1
            self.can_click = True
            
            if self.current_world_index < len(self.worlds):
                messagebox.showinfo("World Cleared!", f"Congratulations! You've completely beaten {current_world_data['world_name']}!")
                self.show_world_welcome_screen() 
            else:
                self.main_label.config(text="🏆 Grand Champion! 🏆", font=("Segoe UI", 32, "bold"), fg=self.accent_gold)
                messagebox.showinfo("Ultimate Victory!", f"Amazing! You completed all Worlds and all Levels!\nFinal Score: {self.score}")

    def reset_current_level(self):
        self.stop_countdown()
        if self.game_frame:
            self.game_frame.destroy()
        
        self.score = 0 
        self.squares_revealed = 0
        self.current_try = 1
        self.can_click = True
        self.setup_gameplay_screen()


if __name__ == "__main__":
    root = tk.Tk()
    app = FruitGuessGame(root)
    root.mainloop()