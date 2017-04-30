import tkinter as tk
import random, os, inspect, time, re, json, subprocess, sys
import tkinter.simpledialog as simpledialog
from tkinter import messagebox
from urllib import request
from webbrowser import open as wbopen

# Move Working Directory
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


def has_internet(site='http://google.co.uk'):
    try:
        request.urlopen(site, timeout=1)
        return (True)
    except:
        return (False)


def has_updates_enabled():
    return not os.path.isfile(".disableupdates")


def cause_update():
    dname = os.getcwd()
    addr = dname + '/updater.pyw'
    subprocess.Popen(['', addr], executable=sys.executable)
    os._exit(1)


with open('.version', 'r') as file:
    version = file.read()
internet_connected = has_internet()
updates_enabled = has_updates_enabled()
if internet_connected and updates_enabled and has_internet(
        'https://api.github.com/repos/JakeHillion2/ShutTheBox/releases/latest'):
    print('Checking for updates...')
    query_address = 'https://api.github.com/repos/JakeHillion2/ShutTheBox/releases/latest'
    latest_version = json.loads(request.urlopen(query_address).read().decode('utf-8'))['tag_name']
    version_nums = re.findall(r'\d+', version)
    latest_version_nums = re.findall(r'\d+', latest_version)
    if len(version_nums) != len(latest_version_nums):
        if len(version_nums) > len(latest_version_nums):
            latest_version_nums += (len(version_nums) - len(latest_version_nums)) * [0]
        else:
            version_nums += (len(latest_version_nums) - len(version_nums)) * [0]
    comp = list(zip([int(x) for x in latest_version_nums], [int(x) for x in version_nums]))
    for each in comp:
        print(each[0], ':', each[1])
        if each[0] > each[1]:
            temp_window = tk.Tk()
            update_text = 'Your version of Shut The Box (' + version + ') is not the latest available version (' + latest_version + '). Do you wish to update the game?'
            result = tk.messagebox.askyesno('Update Available', update_text, master=temp_window)
            temp_window.destroy()
            if result:
                cause_update()
            else:
                break


def std_dev(file_addr):
    h_score, l_score = 0, 1000
    if not (internet_connected and has_internet(file_addr + 'csv_stats/')):
        return ((None, None, None, None))
    try:
        request.urlopen(file_addr + 'csv_stats/')
    except:
        return ((None, None, None, None))
    with request.urlopen(file_addr + 'csv_stats/') as file:
        _file = file.read().decode('utf-8')
        _file = _file.split('\n')
        _file.pop(0)
        _file.pop(len(_file) - 1)
        players = [[]] * 11
        players = [list() for x in players]
        for line in _file:
            each_player = line.split(',')
            i = -1
            for each in each_player:
                if i == -1:
                    rounds = int(each)
                else:
                    players[i].append(int(each) / rounds)
                    if h_score < int(each) and rounds == 5:
                        h_score = int(each)
                    if l_score > int(each) and rounds == 5:
                        l_score = int(each)
                i += 1
    stdevs, averages = [], []
    for player in players:
        if len(player) == 0:
            stdevs.append(None)
            averages.append(None)
        else:
            fx, fx2, n = 0, 0, 0
            for each in player:
                fx += each
                fx2 += each ** 2
                n += 1
            stdev = (fx2 / n - (fx / n) ** 2) ** 0.5
            averages.append(fx / n)
            stdevs.append(stdev)
    return ((stdevs, averages, h_score, l_score))

class OptionsScreen():
    def __init__(self,main_class):
        self.main_class = main_class

        self.players,self.rounds = None,None

        #main_class.name_font = '-*-Microsoft Sans Serif-Normal-R-*--*-700-*-*-*-*-ISO8859-1'
        #main_class.sub_font = '-*-Microsoft Sans Serif-Normal-R-*--*-400-*-*-*-*-ISO8859-1'
        
        self.menu = tk.Tk()
        self.menu.wm_title("Shut The Box - Setup")
        self.options_menu_frame = tk.Frame(master=self.menu, height=750, width=500, bg='blue')
        self.options_menu_frame.pack()
        self.menu.resizable(False, False)
        self.name_text = tk.Label(master=self.menu, text='Shut the Box', bg='blue', fg='yellow',
                                  font=main_class.name_font)
        self.name_text.place(x=45, y=10)
        self.rules_button = tk.Label(master=self.menu, text='The Rules', bg='black', fg='yellow', relief='ridge',
                                     font=main_class.small_font, height=1, bd=3, width=9)
        self.rules_button.bind('<Button-1>', self.display_rules)
        self.rules_button.place(x=50, y=125)

        self.disable_dice_animation_button_var = False

        self.disable_dice_animation_button = tk.Label(master=self.menu, text='Disable Dice Roll Animation',
                                                       bg='black', fg='yellow', relief='ridge',
                                                       font=main_class.small_font, height=1, bd=3, width=23)
        self.disable_dice_animation_button.bind('<Button-1>', self.disable_roll_animation_clicked)
        self.disable_dice_animation_button.place(x=50, y=165)

        self.player_count_text = tk.Label(master=self.menu, text='Select Number of Players', bg='blue',
                                          fg='yellow', font=main_class.sub_font)
        self.player_count_text.place(x=27, y=250)
        # Player Count Boxes
        self.player_count_button = []
        self.player_box = tk.Frame(master=self.menu, height=150, width=700, bd=5, bg='blue',
                                   relief='ridge')
        self.player_box.place(x=250, y=400, anchor=tk.CENTER)
        row = 0
        drop_column = 1
        for i in range(1, 12):
            column = i
            if i == 7:
                row = 1
            if i >= 7:
                column = drop_column
                drop_column = drop_column + 1
            self.player_count_button.append(
                tk.Label(master=self.player_box, width=2, height=1, bd=5, relief='ridge', text=i, font=main_class.font,
                         bg='black', fg='yellow'))
            self.player_count_button[len(self.player_count_button) - 1].grid(row=row, column=column)
            self.player_count_button[len(self.player_count_button) - 1].bind('<Button-1>',
                                                                             self.player_button_clicked, i)
        # Round Boxes
        self.round_button = []
        self.round_box = tk.Frame(master=self.menu, height=150, width=700, bd=5, bg='blue',
                                  relief='ridge')
        self.round_box.place(x=250, y=600, anchor=tk.CENTER)
        for i in range(1, 6):
            self.round_button.append(
                tk.Label(master=self.round_box, width=2, height=1, bd=5, relief='ridge', text=i, font=main_class.font,
                         bg='black', fg='yellow'))
            self.round_button[len(self.round_button) - 1].grid(row=0, column=i)
            self.round_button[len(self.round_button) - 1].bind('<Button-1>',
                                                               self.round_button_clicked, i)

        self.round_text = tk.Label(master=self.menu, text='Rounds', font=main_class.sub_font, bg='blue', fg='yellow')
        self.round_text.place(x=175, y=500)

        self.start_button = tk.Label(master=self.menu, text='Start Game', height=1, relief='ridge', bd=3, width=9,
                                     bg='black', fg='yellow', font=main_class.small_font)
        self.start_button.bind('<Button-1>', self.game_start_check)
        self.start_button.place(x=285, y=700)

        self.exit_button_2 = tk.Label(master=self.menu, text='Exit', height=1, relief='ridge', bd=3, width=4,
                                      bg='black', fg='yellow', font=main_class.small_font)
        self.exit_button_2.bind('<Button-1>', self.menu_quit)
        self.exit_button_2.place(x=425, y=700)

        self.options_complete = True

        self.menu.mainloop()

    def disable_roll_animation_clicked(self, *args):
        if self.disable_dice_animation_button_var == False:
            self.disable_dice_animation_button_var = True
            self.disable_dice_animation_button.config(fg='grey')
        else:
            self.disable_dice_animation_button_var = False
            self.disable_dice_animation_button.config(fg='yellow')

        print("Disable dice roll", self.disable_dice_animation_button_var)

    def menu_quit(self, *args):
        if tk.messagebox.askokcancel(title='Quit Confirm', message='Are you Sure you want to Quit?'):
            self.menu.destroy()

    def game_start_check(self, *args):
        issue = ''
        self.issues = False
        if self.players == None or self.players > 11 or self.players < 2:
            self.issues = True
            issue += 'You need to select between 2 and 11 players!\n'
        if self.rounds == None:
            self.issues = True
            issue += '\nYou need to select the amount of rounds you want to play!'

        if self.issues:
            tk.messagebox.askretrycancel('Oops!', message=issue)
        else:
            self.menu.destroy()
            self.main_class.absorb_settings(self.rounds,self.players,self.disable_dice_animation_button_var)

    def display_rules(self, *args):
        wbopen('https://shutthebox.club/the-game/')

    def player_button_clicked(self, n):
        if type(n) == tk.Event:
            num = int(self.player_count_button.index(n.widget) + 1)
        else:
            num = int(n)
        self.player_count_select(num)

    def round_button_clicked(self, n):
        if type(n) == tk.Event:
            num = int(self.round_button.index(n.widget) + 1)
        else:
            num = int(n)
        self.round_select(num)

    def round_select(self, num):
        if not self.rounds == None:
            self.round_button[self.rounds - 1].config(fg='yellow')
        self.round_button[num - 1].config(fg='grey')
        self.rounds = num

    def player_count_select(self, num):
        if not self.players == None:
            self.player_count_button[self.players - 1].config(fg='yellow')
        self.player_count_button[num - 1].config(fg='grey')
        self.players = num

class ShutTheBox():
    def __init__(self):
        # Set Constants
        self.colours = [
            ['red', 'white'],
            ['violet red', 'white'],
            ['yellow', 'black'],
            ['sea green', 'black'],
            ['orange', 'white'],
            ['brown', 'white'],
            ['white', 'black'],
            ['cyan', 'black'],
            ['orchid', 'white'],
            ['peru', 'black'],
            ['chartreuse', 'black']
        ]
        self.debug = False
        self.debug_nums = [6, 3, 6, 2, 6, 1, 6, 5, 4, 3, 2, 2, 6, 3, 6, 2, 6, 1, 6, 5, 4, 3, 2, 1]
        self.name_font = '-*-Microsoft Sans Serif-Normal-R-*--*-700-*-*-*-*-ISO8859-1'
        self.sub_font = '-*-Microsoft Sans Serif-Normal-R-*--*-400-*-*-*-*-ISO8859-1'
        self.font = '-*-Microsoft Sans Serif-Normal-R-*--*-480-*-*-*-*-ISO8859-1'
        self.small_font = '-*-Microsoft Sans Serif-Normal-R-*--*-240-*-*-*-*-ISO8859-1'
        self.log_address = 'http://188.166.170.12:5000/'
        # Initialise Some Variables
        self.single_dice_on = False
        self.player_turn = 0
        self.board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.round = 1
        self.awaiting_number = False
        self.acceptable_inputs = []

        self.players, self.rounds = None, None
        self.options_complete = False

        options_screen = OptionsScreen(self)

    def absorb_settings(self,rounds,players,disable_roll_animation):
        print(rounds,players)
        self.rounds = rounds
        self.players = players
        self.disable_roll_animation = disable_roll_animation
        self.start_game()
    
    def start_game(self, *args):
        ###
        # Build The Window
        self.window = tk.Tk()
        self.main_frame = tk.Frame(master=self.window, height=600, width=800, bg='blue')
        self.window.wm_title("Shut The Box - DEBUG" if self.debug else ("Shut The Box - " + version))
        self.selection_box = tk.Frame(master=self.main_frame, height=150, width=700, bd=10, bg='blue', relief='ridge')
        self.main_frame.pack()
        self.window.update()
        self.splash_photo = tk.PhotoImage(file='Splash.pgm')
        self.splash_label = tk.Label(master=self.main_frame, image=self.splash_photo, width=800, height=600)
        self.splash_label.place(x=0, y=0)
        self.window.update()
        self.single_dice_var = tk.IntVar()
        self.single_dice_var.set(0)
        self.window.bind("<Key>", self.key)
        ###
        # Destroy the splash screen
        time.sleep(2)
        self.splash_label. place_forget()
        # Render the content
        # Dice Labels
        self.dice1label = tk.Label(master=self.main_frame, width=2, height=1, bd=5, relief='ridge', text=' ',
                                   font=self.font, bg='red', fg='white')
        self.dice1label.place(x=10, y=50)
        self.dice2label = tk.Label(master=self.main_frame, width=2, height=1, bd=5, relief='ridge', text=' ',
                                   font=self.font, bg='red', fg='white')
        self.dice2label.place(x=82, y=50)
        # Player Score Labels
        self.score_labels = []
        self.player_scores = [0] * self.players
        for i in range(self.players):
            colour = self.colours[i][0]
            text_colour = self.colours[i][1]
            self.score_labels.append(tk.Label(master=self.main_frame, width=4, height=1, bd=5, relief='ridge', text='0',
                                              font=self.small_font, bg=colour, fg=text_colour))
            self.score_labels[len(self.score_labels) - 1].place(x=723, y=8 + 49 * i)
        # To Play Label
        self.to_play_label = tk.Label(master=self.main_frame, height=1, text='RED TO PLAY', font=self.font, bg='blue',
                                      fg='red')
        self.to_play_label.place(x=440, y=40, anchor=tk.CENTER)
        # Round Label
        self.round_label = tk.Label(master=self.main_frame, height=1, text='ROUND 1 OF 5', font=self.small_font,
                                    bg='blue', fg='red')
        self.round_label.place(x=440, y=140, anchor=tk.CENTER)
        # Exit Button
        self.exit_button = tk.Label(master=self.main_frame, height=1, width=6, bd=3, bg='black', fg='yellow',
                                    relief='ridge', text='Exit', font=self.small_font)
        self.exit_button.place(x=790, y=590, anchor=tk.SE)
        self.exit_button.bind("<Button-1>", self.close_window)
        # New Game Button
        self.new_game_button = tk.Label(master=self.main_frame, height=1, width=10, bd=3, bg='black', fg='yellow',
                                        relief='ridge', text='New Game', font=self.small_font)
        self.new_game_button.place(x=10, y=590, anchor=tk.SW)
        self.new_game_button.bind("<Button-1>", self.new_game)
        # End Turn Button
        self.end_turn_button = tk.Label(master=self.main_frame, height=1, width=8, bd=3, bg='black', fg='yellow',
                                        relief='ridge', text='End Turn', font=self.small_font)
        self.end_turn_button.place(x=165, y=590, anchor=tk.SW)
        self.end_turn_button.bind("<Button-1>", self.move_on_turn)
        # Throw Dice Button
        self.throw_dice_button = tk.Label(master=self.main_frame, height=1, width=10, bd=3, bg='black', fg='yellow',
                                          relief='ridge', text='Throw Dice', font=self.small_font)
        self.throw_dice_button.place(x=10, y=10, anchor=tk.NW)
        self.throw_dice_button.bind("<Button-1>", self.throw_dice_animation)
        # Show Stats Button
        self.show_stats_button = tk.Label(master=self.main_frame, height=1, width=10, bd=3, bg='black', fg='yellow',
                                          relief='ridge', text='Show Stats', font=self.small_font)
        self.show_stats_button.place(x=680, y=590, anchor=tk.SE)
        self.show_stats_button.bind("<Button-1>", self.show_stats)
        # Single Dice Mode Checkbox
        self.toggle_single_dice_checkbox = tk.Checkbutton(master=self.main_frame, text='Enable Single Dice Mode',
                                                          bg='blue', fg='white', variable=self.single_dice_var,
                                                          command=self.on_single_dice_change)
        # Number Boxes
        self.number_labels = []
        self.selection_buttons = []
        self.selection_box = tk.Frame(master=self.main_frame, height=150, width=700, bd=10, bg='blue', relief='ridge')
        self.selection_box.place(x=400, y=350, anchor=tk.CENTER)
        for i in range(1, 10):
            self.number_labels.append(
                tk.Label(master=self.selection_box, width=2, height=1, bd=5, relief='ridge', text=i, font=self.font,
                         bg='black', fg='red'))
            self.number_labels[len(self.number_labels) - 1].grid(row=0, column=i)
            self.number_labels[len(self.number_labels) - 1].bind('<Button-1>', self.number_clicked_function, i)
            self.selection_buttons.append(
                tk.Label(master=self.selection_box, width=2, height=1, bd=3, relief='ridge', text='', font=self.font,
                         bg='blue', fg='red'))
            self.selection_buttons[len(self.selection_buttons) - 1].grid(row=1, column=i)
        # Begin the Game
        self.round_label.config(text=self.gen_round_text())
        self.next_turn()
        # Main Loop
        self.window.mainloop()

    def close_window(self, x):
        if tk.messagebox.askokcancel('Exit Game', 'Are you sure you wish to exit?'):
            self.window.destroy()

    def new_game(self, x):
        if tk.messagebox.askokcancel('Start New Game', 'Are you sure you wish to start a new game?'):
            self.window.destroy()
            self.__init__()

    def move_on_turn(self, x):
        if tk.messagebox.askokcancel('End Turn', 'Are you sure you wish to end this turn?'):
            self.next_turn()

    def gen_round_text(self):
        return ('ROUND ' + str(self.round) + ' OF ' + str(self.rounds))

    def single_dice_option(self, val):
        if val:
            self.toggle_single_dice_checkbox.place(x=10, y=120)
        else:
            self.toggle_single_dice_checkbox.place_forget()

    def number_clicked_function(self, n):
        if type(n) == tk.Event:
            num = int(self.number_labels.index(n.widget) + 1)
        else:
            num = int(n)
        if self.awaiting_number:
            print(num, 'was clicked')
            if num in self.acceptable_inputs[0]:
                self.acceptable_inputs[0].remove(num)
                self.acceptable_inputs = [[None, None], self.acceptable_inputs[0][0]]
                self.selection_buttons[num - 1].config(text='X')
                self.number_labels[num - 1].config(text='', bg='grey')
                self.player_scores[self.player_turn - 1] += num
                self.board.remove(num)
                if not False in [False for x in self.board if x > 6]:
                    self.single_dice_option(True)
            elif num in self.acceptable_inputs:
                self.acceptable_inputs = []
                self.awaiting_number = False
                self.throw_dice_button.bind("<Button-1>", self.throw_dice_animation)
                self.throw_dice_button.config(fg='yellow')
                self.selection_buttons[num - 1].config(text='X')
                self.number_labels[num - 1].config(text='', bg='grey')
                self.player_scores[self.player_turn - 1] += num
                self.board.remove(num)
                if not False in [False for x in self.board if x > 6]:
                    self.single_dice_option(True)
            else:
                return (0)
            self.update_scores()
            if len(self.board) == 0:
                self.board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                self.reset_board()
                self.single_dice_var.set(0)
                self.on_single_dice_change()
                self.single_dice_option(False)
            print(self.acceptable_inputs)
        else:
            print(num, 'was clicked unwantingly')

    def throw_dice_animation(self, x, y=0):
        #self.disable_roll_animation
        if (type(x) is tk.Event) or (x is None):
            self.throw_dice_button.bind("<Button-1>", self.do_nothing)
            self.throw_dice_button.config(fg='grey')
            if self.single_dice_on:
                print('Single dice throw called')
                if self.disable_roll_animation:
                    self.throw_dice_button.after(40, self.throw_dice_animation, 0, 1)
                else:
                    self.dice1label.config(text=random.randint(1, 6))
                    self.window.update()
                    self.throw_dice_button.after(40, self.throw_dice_animation, 10, 1)
            else:
                print('Double dice throw called')
                if self.disable_roll_animation:
                    self.throw_dice_button.after(40, self.throw_dice_animation, 0, 0)
                else:
                    self.dice1label.config(text=random.randint(1, 6))
                    self.dice2label.config(text=random.randint(1, 6))
                    self.window.update()

                    self.throw_dice_button.after(40, self.throw_dice_animation, 10, 0)
        else:
            if y == 0:
                # Double throw
                if x > 0:
                    # Randomise and reduce x
                    self.dice1label.config(text=random.randint(1, 6))
                    self.dice2label.config(text=random.randint(1, 6))
                    self.window.update()
                    self.throw_dice_button.after(40, self.throw_dice_animation, x - 1, 0)
                else:
                    if self.debug and len(self.debug_nums) > 1:
                        r1, r2 = self.debug_nums.pop(0), self.debug_nums.pop(0)
                    else:
                        r1, r2 = random.randint(1, 6), random.randint(1, 6)
                    self.dice1label.config(text=r1)
                    self.dice2label.config(text=r2)
            elif y == 1:
                # Single throw
                if x > 0:
                    # Randomise and reduce x
                    self.dice1label.config(text=random.randint(1, 6))
                    self.window.update()
                    self.throw_dice_button.after(40, self.throw_dice_animation, x - 1, 1)
                else:
                    if self.debug and len(self.debug_nums) > 0:
                        r1, r2 = self.debug_nums.pop(0), 0
                    else:
                        r1, r2 = random.randint(1, 6), 0
                    self.dice1label.config(text=r1)
            if not x > 0:
                self.awaiting_number = True
                self.set_available(r1, r2)

    def set_available(self, r1, r2):
        self.acceptable_inputs = []
        if (r1 in self.board) and (r2 in self.board) and (r1 != r2):
            self.acceptable_inputs.append([r1, r2])
        else:
            self.acceptable_inputs.append([None, None])
        if r1 + r2 in self.board:
            self.acceptable_inputs.append(r1 + r2)
        else:
            self.acceptable_inputs.append(None)
        if self.acceptable_inputs == [[None, None], None]:
            # End turn
            self.to_play_label.config(text='TURN OVER')
            self.window.update()
            self.awaiting_number = False
            self.window.after(1200, self.next_turn)
        print(self.acceptable_inputs)

    def update_scores(self):
        for i in range(0, len(self.score_labels)):
            self.score_labels[i].config(text=self.player_scores[i])
        self.window.update()

    def next_turn(self):
        self.acceptable_inputs = []
        self.awaiting_number = False
        self.player_turn += 1
        if self.player_turn > self.players:
            self.player_turn = 1
            self.round += 1
            print('--- SCORES AT END OF PREVIOUS ROUND ---')
            print(self.player_scores)
            if not self.round > self.rounds:
                self.round_label.config(text=self.gen_round_text())
            else:
                print('GAME COMPLETE')
                win_index = self.player_scores.index(max(self.player_scores))
                win_colour = self.colours[win_index][0]
                self.to_play_label.config(text=win_colour.upper() + ' WINS', fg=win_colour)
                self.round_label.config(fg=win_colour)
                self.throw_dice_button.bind("<Button-1>", self.do_nothing)
                self.throw_dice_button.config(fg='grey')
                self.window.update()
                os.system('say ' + win_colour + ' has won the game')
                if internet_connected and has_internet(self.log_address):
                    request.urlopen(self.log_address + 'upload_stats/' + '/'.join(
                        [str(self.rounds)] + [str(x) for x in self.player_scores]))
                return (0)
        main_colour, secondary_colour = self.colours[self.player_turn - 1][0], self.colours[self.player_turn - 1][1]
        self.to_play_label.config(text=main_colour.upper() + ' TO PLAY', fg=main_colour)
        self.round_label.config(fg=main_colour)
        self.reset_board()
        self.single_dice_var.set(0)
        self.on_single_dice_change()
        self.single_dice_option(False)
        self.throw_dice_button.bind("<Button-1>", self.throw_dice_animation)
        self.dice1label.config(bg=main_colour)
        self.dice2label.config(bg=main_colour)
        self.dice1label.config(fg=secondary_colour, text=' ')
        self.dice2label.config(fg=secondary_colour, text=' ')
        self.board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.throw_dice_button.config(fg=main_colour)
        self.window.update()

    def reset_board(self):
        main_colour, secondary_colour = self.colours[self.player_turn - 1][0], self.colours[self.player_turn - 1][1]
        for i in self.selection_buttons:
            i.config(fg=main_colour)
        for i in self.number_labels:
            i.config(fg=main_colour)
        self.reset_selector_buttons()

    def on_single_dice_change(self):
        if self.single_dice_var.get() == 1:
            print('Toggling single dice mode on')
            self.dice2label.place_forget()
            self.single_dice_on = True
        else:
            print('Toggling single dice mode off')
            self.dice2label.place(x=82, y=50)
            self.single_dice_on = False

    def reset_selector_buttons(self):
        for i in self.selection_buttons:
            i.config(text=' ')
        for i in range(1, 10):
            self.number_labels[i - 1].config(text=i, bg='black')

    def do_nothing(*args):
        pass

    def show_stats(self, x):
        self.sub_window = tk.Tk()
        self.sub_window_frame = tk.Frame(master=self.sub_window, height=540, width=295, bg='blue')
        self.sub_window_frame.pack()
        self.sub_window.wm_title("Shut The Box - Statistics")
        i = 0
        boxes = []
        stdevs, averages, h_score, l_score = std_dev(self.log_address)
        if ((stdevs is None) and (averages is None)) and ((h_score is None) and (l_score is None)):
            box = tk.Label(master=self.sub_window_frame, height=1, width=20, font=self.small_font,
                           text='No stats available.', fg='black', bg='white', relief='ridge')
            boxes.append(box)
        else:
            for colour in self.colours:
                stdev, mean = stdevs[i], averages[i]
                _text = 'μ: ' + str(round(mean, 2) if mean is not None else 'N/A') + '   -   σ: ' + str(
                    round(stdev, 2) if stdev is not None else 'N/A')
                box = tk.Label(master=self.sub_window_frame, height=1, width=20, font=self.small_font, text=_text,
                               fg=colour[0], bg='black', relief='ridge')
                boxes.append(box)
                i += 1
            _text = 'High Score: ' + str(h_score)
            box = tk.Label(master=self.sub_window_frame, height=1, width=20, font=self.small_font, text=_text,
                           fg='black', bg='white', relief='ridge')
            boxes.append(box)
            _text = 'Low Score: ' + str(l_score)
            box = tk.Label(master=self.sub_window_frame, height=1, width=20, font=self.small_font, text=_text,
                           fg='black', bg='white', relief='ridge')
            boxes.append(box)
        i = 0
        for box in boxes:
            box.place(y=i * 40 + 15, x=15, anchor=tk.NW)
            i += 1

    def key(self, event):
        if event.char == ' ' or event.char == '\r':
            # Space Pressed, Roll Dice
            if (not self.awaiting_number) and (self.throw_dice_button.cget('fg') != 'grey'):
                self.throw_dice_animation(None)
        elif event.char.isnumeric():
            # Number Pressed, Press Number
            self.number_clicked_function(event.char)
        else:
            print("pressed", repr(event.char))


test = ShutTheBox()
