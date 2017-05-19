import tkinter as tk
import random, os, time, re, json, subprocess, sys, math
from tkinter import messagebox
from urllib import request, parse
from webbrowser import open as wbopen
from hashlib import sha256
from urllib import error as url_error
from tkinter import simpledialog

# Move Working Directory
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


# Declare Top Level Functions
def has_internet(site='http://google.co.uk'):
    try:
        _request = request.Request(site, headers={'User-Agent': 'python'})
        request.urlopen(_request, timeout=1)
        return (True)
    except:
        return (False)


def has_updates_enabled():
    return not os.path.isfile(".disableupdates")


def cause_update():
    dir_name = os.getcwd()
    addr = dname + '/updater.pyw'
    subprocess.Popen(['', addr], executable=sys.executable)
    os._exit(1)


def post_request(address, dictionary, headers=None):
    if headers is None:
        headers = {'user-agent': 'python'}
    data = parse.urlencode(dictionary).encode()
    _request = request.Request(address, data=data, headers=headers)
    response = request.urlopen(_request, timeout=5).read().decode()
    return (response)


def get_request(address, headers=None):
    if headers is None:
        headers = {'user-agent': 'python'}
    _request = request.Request(address, headers=headers)
    response = request.urlopen(_request, timeout=5).read().decode()
    return (response)


def pagerise(x, per=10):
    pages = int(math.ceil(len(x) / per))
    output = []
    for i in range(pages):
        output.append(x[per * i:per * (i + 1)])
    return (output)


# Grab Current Version
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


# Utility Classes
class ChatWindow():
    def __init__(self, master, callback_function):
        self.callback_function = callback_function

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

        self.window = tk.Toplevel(master)
        self.window.wm_title('Chat')
        self.main_frame = tk.Frame(master=self.window, width=300, height=600, bg='blue')
        self.main_frame.pack()

        self.message_var = tk.StringVar()
        self.text_entry = tk.Entry(master=self.window,textvar=self.message_var)
        self.text_entry.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_entry.bind('<Return>', self.send_message)

        self.scrollbar = tk.Scrollbar(self.main_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text = tk.Text(self.main_frame, bg='blue', fg='black', width=30, height=30, state='disabled', wrap=tk.WORD,
                            yscrollcommand=self.scrollbar.set)
        self.text.pack(side=tk.LEFT)

        self.scrollbar.config(command=self.text.yview)

        for each in self.colours:
            self.text.tag_config(each[0].replace(" ", "") + '1', foreground=each[1], background=each[0])
            self.text.tag_config(each[0].replace(" ", "") + '2', foreground=each[1])

        self.window.withdraw()
        self.window.protocol("WM_DELETE_WINDOW", self.hide_window)

        #self.window.mainloop()

    def add_message(self, sender, message):
        self.text.config(state='normal')
        self.text.insert(tk.END, sender + ':', (sender.replace(" ", "") + '1'))
        self.text.insert(tk.END, '  ' + message + '\n', (sender.replace(" ", "") + '2'))
        self.text.see(tk.END)
        self.text.config(state='disabled')

    def add_fc_message(self,message,tag):
        self.text.config(state='normal')
        self.text.insert(tk.END, message, tag.replace(" ", "") + '1')
        self.text.see(tk.END)
        self.text.config(state='disabled')

    def send_message(self, x):
        message = self.message_var.get()
        self.message_var.set('')
        self.callback_function(message)

    def hide_window(self, x=None):
        self.window.withdraw()

    def show_window(self, x=None):
        self.window.deiconify()


# Main Window Classes
class OpeningScreen():
    def __init__(self):
        self.window = tk.Tk()
        self.window.wm_title("Shut The Box - Setup")
        self.decider_frame = tk.Frame(master=self.window, height=200, width=500, bg='blue')
        self.decider_frame.pack()
        self.window.resizable(False, False)

        # change these later
        self.name_font = '-*-Microsoft Sans Serif-Normal-R-*--*-700-*-*-*-*-ISO8859-1'
        self.sub_font = '-*-Microsoft Sans Serif-Normal-R-*--*-400-*-*-*-*-ISO8859-1'
        self.font = '-*-Microsoft Sans Serif-Normal-R-*--*-480-*-*-*-*-ISO8859-1'
        self.small_font = '-*-Microsoft Sans Serif-Normal-R-*--*-240-*-*-*-*-ISO8859-1'
        self.italic_font = '-*-Microsoft Sans Serif-Normal-I-*--*-240-*-*-*-*-ISO8859-1'

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

        self.online_button = tk.Label(master=self.window, text='Online', bg='black', fg='yellow', relief='ridge',
                                      font=self.font, height=1, bd=3, width=7)
        self.online_button.bind('<Button-1>', self.do_online)
        self.online_button.place(x=25, y=50)

        self.local_button = tk.Label(master=self.window, text='Local', bg='black', fg='yellow', relief='ridge',
                                     font=self.font, height=1, bd=3, width=7)
        self.local_button.bind('<Button-1>', self.do_local)
        self.local_button.place(x=270, y=50)

        self.stage2 = None

        self.window.mainloop()

    def do_online(self, *args):
        self.stage2 = OnlineScreen(self)

    def do_local(self, *args):
        self.stage2 = OfflineScreen(self)


class OnlineScreen():
    def __init__(self, opening_screen):
        self.base_url = 'https://mp.shutthebox.club/'
        self.uuid_location = 'uuid.txt'

        if os.access('/path/to/folder', os.W_OK):
            if os.path.isfile(os.getenv('LOCALAPPDATA') + '\\Shut The Box\\uuid.txt'):
                if not os.path.isdir(os.getenv('LOCALAPPDATA') + '\\Shut The Box'):
                    os.mkdir(os.getenv('LOCALAPPDATA') + '\\Shut The Box')
                self.uuid_location = os.getenv('LOCALAPPDATA') + '\\Shut The Box\\uuid.txt'
            else:
                self.uuid_location = 'uuid.txt'
        else:
            if not os.path.isdir(os.getenv('LOCALAPPDATA') + '\\Shut The Box'):
                os.mkdir(os.getenv('LOCALAPPDATA') + '\\Shut The Box')
            self.uuid_location = os.getenv('LOCALAPPDATA') + '\\Shut The Box\\uuid.txt'

        # grab a uuid
        if os.path.isfile(self.uuid_location):
            with open(self.uuid_location, 'r') as file:
                old_id = file.read()
        else:
            old_id = None
        new_id = None
        if old_id is not None:
            result = post_request(self.base_url + '/refresh_uuid/', {'uuid': old_id})
            new_id = old_id if json.loads(result)['success'] else None
            print('new_id =', new_id)
        if new_id is None:
            new_id = get_request(self.base_url + '/serve_uuid/')
            print('new_id =', new_id)
        with open(self.uuid_location, 'w') as file:
            file.write(new_id)
        self.new_id = new_id
        self.new_id_hash = sha256(self.new_id.encode('utf-8')).hexdigest()

        self.opening_screen = opening_screen
        self.window = opening_screen.window
        opening_screen.decider_frame.destroy()

        self.online_frame = tk.Frame(master=self.window, height=200, width=500, bg='blue')
        self.online_frame.pack()

        self.join_button = tk.Label(master=self.online_frame, text='Join', bg='black', fg='yellow', relief='ridge',
                                    font=opening_screen.font, height=1, bd=3, width=7)
        self.join_button.bind('<Button-1>', self.do_join)
        self.join_button.place(x=25, y=50)

        self.create_button = tk.Label(master=self.online_frame, text='Create', bg='black', fg='yellow', relief='ridge',
                                      font=opening_screen.font, height=1, bd=3, width=7)
        self.create_button.bind('<Button-1>', self.do_create)
        self.create_button.place(x=270, y=50)

        self.window.mainloop()

    def do_join(self, *args):
        self.online_frame.destroy()
        content = get_request(self.base_url + '/available_rooms/')
        self.available_rooms = json.loads(content)
        self.join_pages = pagerise(self.available_rooms)
        self.join_page = 0
        self.render_join_page()

    def render_join_page(self, *args):
        if len(self.join_pages) == 0:
            return (None)
        page = self.join_pages[self.join_page]
        self.in_room_frame = tk.Frame(master=self.window, height=800, width=500, bg='blue')
        self.in_room_frame.pack()
        page_labels = []
        i = 0
        for each in page:
            new = tk.Label(master=self.in_room_frame, text=each['identifier'], width=15, height=2,
                           font=self.opening_screen.small_font, bg='black', fg='yellow', relief='ridge', bd=3)
            new.bind('<Button-1>', self.click_join_button)
            new.place(x=20, y=50 + 75 * i)
            page_labels.append(new)
            i += 1

    def click_join_button(self, event):
        print(event.widget['text'])
        print(self.available_rooms)
        rooms_dict = {x['identifier']: x for x in self.available_rooms}
        if rooms_dict[event.widget['text']]['has_password']:
            room_pass = tk.simpledialog.askstring('Password', 'Please enter the room password:')
        else:
            room_pass = None
        nname = tk.simpledialog.askstring('Nickname', 'Please enter a nickname:')
        self.final_join(event.widget['text'], nname, room_pass)

    def do_create(self, *args):
        self.online_frame.destroy()
        self.create_room_frame = tk.Frame(master=self.window, height=400, width=500, bg='blue')
        self.create_room_frame.pack()

        self.room_name_entry = tk.Entry(self.create_room_frame)
        self.room_name_entry.place(x=10, y=20)
        self.room_pass_entry = tk.Entry(self.create_room_frame, show='*')
        self.room_pass_entry.place(x=10, y=50)
        self.nickname_entry = tk.Entry(self.create_room_frame)
        self.nickname_entry.place(x=10, y=80)

        create_button = tk.Label(master=self.create_room_frame, text='Create Room', bg='black', fg='yellow',
                                 font=self.opening_screen.font, relief='ridge', height=1, bd=3, width=11)
        create_button.bind('<Button-1>', self.final_create)
        create_button.place(x=10, y=350)

    def final_create(self, *args):
        reasons = {'RNE': 'The room name you entered has already been used!'}
        name_entry = self.room_name_entry.get()
        if ' ' in name_entry:
            tk.messagebox.showerror('Room Not Created', 'Spaces are not allowed in room names!')
            return (False)
        pass_entry = self.room_pass_entry.get()
        nname_entry = self.nickname_entry.get()
        pass_entry = None if pass_entry == '' else pass_entry
        data = {'uuid': self.new_id, 'room_data': json.dumps({'room_name': name_entry, 'room_pass': pass_entry})}
        print(data)
        val = post_request(self.base_url + 'create_room/', data)
        print(json.loads(val))
        success = json.loads(val)['success']
        if success:
            self.final_join(name_entry, nname_entry, pass_entry)
        else:
            print('not success')
            tk.messagebox.showerror('Room Not Created', reasons[json.loads(val)['reason']])

    def final_join(self, room_id, nickname, room_pass=None):
        print('joining room with id:', room_id)
        data = {'uuid': self.new_id, 'nickname': nickname,
                'room_data': json.dumps({'room_name': room_id, 'room_pass': room_pass})}
        result = post_request(self.base_url + '/join_room/', data)
        success = json.loads(result)['success']
        if not success:
            tk.messagebox.showerror('Room Not Joined', 'The room you wish to join is full.')
            return (False)
        self.joined_room = room_id
        self.room_screen()

    def room_screen(self):
        try:
            if not 'room_screen_frame' in list(self.__dict__.keys()):
                self.room_screen_frame = tk.Frame(master=self.window, height=600, width=300, bg='blue')
                self.room_screen_frame.pack()
                label1 = tk.Label(master=self.room_screen_frame, text='Leave Game', width=10, height=1,
                                  font=self.opening_screen.small_font, bg='black', fg='yellow', relief='ridge', bd=3)
                label1.place(x=160, y=560)
                label1.bind('<Button-1>', self.leave_room)
            if 'create_room_frame' in list(self.__dict__.keys()):
                self.create_room_frame.destroy()
            elif 'in_room_frame' in list(self.__dict__.keys()):
                self.in_room_frame.destroy()
            room_data = json.loads(get_request(self.base_url + '/view_room/' + self.joined_room))
            if room_data['started']:
                self.start_game()
            if room_data['host'] == self.new_id_hash:
                label2 = tk.Label(master=self.room_screen_frame, text='Start Game', width=10, height=1,
                                  font=self.opening_screen.small_font, bg='black', fg='yellow', relief='ridge', bd=3)
                label2.place(x=7, y=560)
                label2.bind('<Button-1>', self.send_start)
            if 'room_screen_labels' not in list(self.__dict__.keys()):
                self.room_screen_labels = []
                for i in range(room_data['capacity']):
                    new = tk.Label(master=self.room_screen_frame, bg='light slate gray', width=15, height=1,
                                   font=self.opening_screen.small_font, bd=3, relief='ridge')
                    new.place(x=10, y=10 + i * 42)
                    self.room_screen_labels.append(new)
            members = room_data['members']
            j = 0
            for member in members:
                if member[1] == self.new_id_hash:
                    text = ' ' + chr(0x00B7) + '  ' + member[0]
                    self.my_colour = j
                else:
                    text = '    ' + member[0]
                self.room_screen_labels[j].config(bg=self.opening_screen.colours[j][0], anchor=tk.W,
                                                  font=self.opening_screen.small_font,
                                                  text=text, fg=self.opening_screen.colours[j][1])
                j += 1
            self.room_screen_frame.after(1000, self.room_screen)
        except url_error.URLError as e:
            print('Excepted!')
            print(e)
            self.room_screen_frame.after(500, self.room_screen)

    def send_start(self, x):
        data = {'uuid': self.new_id, 'room_data': json.dumps({'room_name': self.joined_room})}
        post_request(self.base_url + '/start_game_room/', data)

    def leave_room(self, x):
        data = {'uuid': self.new_id, 'room_data': json.dumps({'room_name': self.joined_room})}
        post_request(self.base_url + '/leave_room/', data)
        self.room_screen_frame.destroy()
        self.opening_screen.__init__()

    def start_game(self):
        self.room_screen_frame.destroy()
        self.window.destroy()
        print('Starting game...')
        game = OnlineGame(self.joined_room, self.new_id, self.new_id_hash, self.opening_screen, self.my_colour)


class OnlineGame():
    def __init__(self, game_id, uuid, uuid_hash, opening_screen, my_colour):
        self.game_id = game_id
        self.uuid = uuid
        self.uuid_hash = uuid_hash
        self.opening_screen = opening_screen
        self.my_colour = my_colour

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
        self.stats_location = 'https://stats.shutthebox.club/'
        self.base_url = 'https://mp.shutthebox.club/'
        self.reactions = {
            'TextChat': self.react_to_text_chat,
            'ReportActivity': self.refresh_uuid,
            'PlayerLeft': self.player_left,
            'DiceRollBegins': self.throw_dice_animation,
            'DiceRollEnds': self.set_throw_dice_results,
            'LostConnection': self.lost_connection_handler,
            'NumberCleared': self.clear_number,
            'EnableThrowDice': self.enable_throw_dice,
            'TurnChange': self.react_to_turn_change,
            'RoundChange': self.react_to_round_change,
            'AnnounceWinner': self.react_to_game_finished,
            'ScoreUpdate': self.react_to_scores
        }

        # Initialise Some Variables
        self.single_dice_on = False
        self.player_turn = 0
        self.board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.round = 1
        self.awaiting_number = False
        self.acceptable_inputs = []
        self.last_score_gathered = 0.0
        self.time_offset = None
        self.r1, self.r2 = None, None
        self.my_turn = False

        room_data = json.loads(get_request(self.base_url + '/view_room/' + self.game_id))

        self.players, self.rounds = len(room_data['members']), 5
        self.show_roll_animation = True

        # Build The Window
        self.window = tk.Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)
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
        # Create Background Chat Window
        self.chat_window = ChatWindow(self.window, self.inform_server_of_chat)
        # Destroy the splash screen
        time.sleep(2)
        self.splash_label.place_forget()
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
        self.end_turn_button.bind("<Button-1>", self.cause_server_vote)
        # Throw Dice Button
        self.throw_dice_button = tk.Label(master=self.main_frame, height=1, width=10, bd=3, bg='black', fg='yellow',
                                          relief='ridge', text='Throw Dice', font=self.small_font)
        self.throw_dice_button.place(x=10, y=10, anchor=tk.NW)
        self.throw_dice_button.bind("<Button-1>", self.tell_server_dice_throw)
        # Show Stats Button
        self.show_stats_button = tk.Label(master=self.main_frame, height=1, width=10, bd=3, bg='black', fg='yellow',
                                          relief='ridge', text='Show Stats', font=self.small_font)
        self.show_stats_button.place(x=680, y=590, anchor=tk.SE)
        self.show_stats_button.bind("<Button-1>", self.show_stats)
        # Open Chat Button
        self.open_chat_button = tk.Label(master=self.main_frame, height=1, width=10, bd=3, bg='black', fg='yellow',
                                          relief='ridge', text='Open Chat', font=self.small_font)
        self.open_chat_button.place(x=530, y=590, anchor=tk.SE)
        self.open_chat_button.bind("<Button-1>", self.open_chat)
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
        self.window.after(1000, self.online_loop)
        # Main Loop
        self.window.mainloop()

    def online_loop(self):
        try:
            data = json.loads(get_request(self.base_url+'/view_events/' + self.game_id + '/' + str(self.last_score_gathered)))
            self.last_score_gathered = data['timecode']
            if self.time_offset is None:
                self.time_offset = round((data['timecode'] - time.time())/1800)*1800
                print(self.time_offset)
            self.events = data['events']
            if self.my_turn:
                self.window.after(500, self.online_loop)
            else:
                self.window.after(1000, self.online_loop)
            if len(self.events) > 0:
                self.window.after(2,self.offline_loop)
        except Exception as e:
            print(e)
            self.window.after(1000, self.online_loop)

    def offline_loop(self):
        keys_to_process = [x for x in self.events.keys() if float(x) < (time.time() + self.time_offset)]
        if len(keys_to_process) == 0:
            if len(self.events) > 0:
                self.window.after(10, self.offline_loop)
            return(None)
        keys_to_process = sorted(keys_to_process, key=float)
        process_key = keys_to_process[0]
        event = self.events.pop(process_key)
        event = json.loads(event)
        print('Handling',event)
        self.reactions[event['type']](event)
        if len(self.events) > 0:
            self.window.after(10,self.offline_loop)

    def send_server_event(self, event, details=None):
        if details is None:
            details = {}
        post_request(self.base_url + '/event_from_client/', {'event': event, 'uuid': self.uuid, 'details':json.dumps(details), 'room_id':self.game_id})

    def close_window(self, x=None):
        if tk.messagebox.askokcancel('Exit Game', 'Are you sure you wish to exit? You will not be able to reconnect to this game.'):
            try:
                self.disconnect()
            except:
                pass
            self.window.destroy()

    def disconnect(self):
        data = {'uuid': self.uuid, 'room_data': json.dumps({'room_name': self.game_id})}
        post_request(self.base_url + '/leave_room/', data)

    def open_chat(self,x):
        self.chat_window.show_window()

    # To Server Event Management
    def inform_server_of_chat(self, chat):
        self.send_server_event('NCM',{'message':chat})

    def cause_server_vote(self,x):
        self.send_server_event('TEV')

    def tell_server_dice_throw(self,x=None):
        self.send_server_event('DCT')

    def on_single_dice_change(self,x=None):
        if self.single_dice_var.get() == 1:
            print('Toggling single dice mode on')
            self.send_server_event('SDM',{'state': True})
        else:
            print('Toggling single dice mode off')
            self.send_server_event('SDM', {'state': False})

    def number_clicked_function(self, n):
        if type(n) == tk.Event:
            num = int(self.number_labels.index(n.widget) + 1)
        else:
            num = int(n)
        self.send_server_event('NUMC', {'number': num})

    # From Server Event Management
    def react_to_text_chat(self, data):
        self.chat_window.add_message(self.colours[data['contents']['sender']][0],data['contents']['message'])

    def refresh_uuid(self, data):
        result = post_request(self.base_url + '/refresh_uuid/', {'uuid': self.uuid})
        print('UUID Refreshed' if json.loads(result)['success'] else 'UUID Refresh Failed')

    def player_left(self, data):
        self.chat_window.add_fc_message(self.colours[data['contents']['colour']][0]+' has left the game.',self.colours[data['contents']['colour']][0])

    def set_throw_dice_results(self,data):
        self.r1, self.r2 = data['contents']['number1'], data['contents']['number2']

    def clear_number(self, data):
        num = data['contents']['number']
        self.selection_buttons[num - 1].config(text='X')
        self.number_labels[num - 1].config(text='', bg='grey')

    def enable_throw_dice(self, data):
        self.throw_dice_button.bind("<Button-1>", self.tell_server_dice_throw)
        self.throw_dice_button.config(fg='yellow')

    def react_to_turn_change(self, data):
        change_to = data['contents']['to_colour']
        if change_to == self.my_colour:
            self.my_turn = True
        else:
            self.my_turn = False
        print('Change to:',change_to)
        self.window.after(1200,self.next_turn,change_to)

    def react_to_round_change(self, data):
        change_to = data['contents']['to_round']+1
        self.next_round(change_to)
        self.next_turn(0)

    def react_to_game_finished(self, data):
        x = data['contents']['winner']
        self.game_finished(x)

    def react_to_scores(self, data):
        self.player_scores = data['contents']['scores']
        for i in range(0, len(self.score_labels)):
            self.score_labels[i].config(text=self.player_scores[i-1])
        self.window.update()

    # Base Functions
    def next_turn(self, x):
        self.player_turn = x
        main_colour, secondary_colour = self.colours[self.player_turn][0], self.colours[self.player_turn][1]
        self.to_play_label.config(text=main_colour.upper() + ' TO PLAY', fg=main_colour)
        self.round_label.config(fg=main_colour)
        self.reset_board()
        self.single_dice_var.set(0)
        self.on_single_dice_change()
        self.throw_dice_button.bind("<Button-1>", self.tell_server_dice_throw)
        self.dice1label.config(bg=main_colour)
        self.dice2label.config(bg=main_colour)
        self.dice1label.config(fg=secondary_colour, text=' ')
        self.dice2label.config(fg=secondary_colour, text=' ')
        self.board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.throw_dice_button.config(fg=main_colour)
        self.window.update()

    def game_finished(self,x):
        win_colour = self.colours[x][0]
        self.to_play_label.config(text=win_colour.upper() + ' WINS', fg=win_colour)
        self.round_label.config(fg=win_colour)
        self.throw_dice_button.bind("<Button-1>", self.do_nothing)
        self.throw_dice_button.config(fg='grey')
        self.window.update()
        os.system('say ' + win_colour + ' has won the game')

    def next_round(self, x):
        self.player_turn = 0
        self.round = x
        self.round_label.config(text=self.gen_round_text())

    def reset_board(self):
        main_colour, secondary_colour = self.colours[self.player_turn][0], self.colours[self.player_turn][1]
        for i in self.selection_buttons:
            i.config(fg=main_colour)
        for i in self.number_labels:
            i.config(fg=main_colour)
        for i in self.selection_buttons:
            i.config(text=' ')
        for i in range(1, 10):
            self.number_labels[i - 1].config(text=i, bg='black')

    def new_game(self,x):
        self.close_window(None)
        self.opening_screen.__init__()

    def gen_round_text(self):
        return ('ROUND ' + str(self.round) + ' OF ' + str(self.rounds))

    def throw_dice_animation(self, x, y=0):
        # self.disable_roll_animation
        if (type(x) is tk.Event) or (type(x) is dict) or (x is None):
            self.throw_dice_button.bind("<Button-1>", self.do_nothing)
            self.throw_dice_button.config(fg='grey')
            if self.single_dice_on:
                print('Single dice throw called')
                if self.show_roll_animation:
                    self.dice1label.config(text=random.randint(1, 6))
                    self.window.update()
                    self.throw_dice_button.after(40, self.throw_dice_animation, 10, 1)
                else:
                    self.throw_dice_button.after(40, self.throw_dice_animation, 0, 1)

            else:
                print('Double dice throw called')
                if self.show_roll_animation:
                    self.dice1label.config(text=random.randint(1, 6))
                    self.dice2label.config(text=random.randint(1, 6))
                    self.window.update()

                    self.throw_dice_button.after(40, self.throw_dice_animation, 10, 0)
                else:
                    self.throw_dice_button.after(40, self.throw_dice_animation, 0, 0)

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
                    self.dice1label.config(text=self.r1)
                    self.dice2label.config(text=self.r2)
            elif y == 1:
                # Single throw
                if x > 0:
                    # Randomise and reduce x
                    self.dice1label.config(text=random.randint(1, 6))
                    self.window.update()
                    self.throw_dice_button.after(40, self.throw_dice_animation, x - 1, 1)
                else:
                    self.dice1label.config(text=self.r1)

    def lost_connection_handler(self, x):
        print('LostConnection Event Received')

    def gather_stats(self):
        if not (internet_connected and has_internet(self.stats_location)):
            if not has_internet(self.stats_location):
                print('cannot connect to:', self.stats_location)
            return ((None, None, None, None))
        _request = request.Request(self.stats_location + 'abbrv_stats/', headers={'User-Agent': 'python'})
        data = json.loads(request.urlopen(_request).read().decode('utf-8'))
        return ((data['stdev'], data['averages'], data['h_score'], data['l_score']))

    def do_nothing(self, *args):
        pass

    def show_stats(self, x):
        self.sub_window = tk.Toplevel(master=self.window)
        self.sub_window_frame = tk.Frame(master=self.sub_window, height=540, width=295, bg='blue')
        self.sub_window_frame.pack()
        self.sub_window.wm_title("Shut The Box - Statistics")
        i = 0
        boxes = []
        stdevs, averages, h_score, l_score = self.gather_stats()
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
            self.tell_server_dice_throw()
        elif event.char.isnumeric():
            # Number Pressed, Press Number
            self.number_clicked_function(event.char)
        elif event.char == 's':
            print('s pressed')
            if self.single_dice_available:
                print('toggling single dice')
                to_set = 1 if self.single_dice_var.get() == 0 else 0
                self.single_dice_var.set(to_set)
                self.on_single_dice_change()
        else:
            print("pressed", repr(event.char))


class OfflineScreen():
    def __init__(self, opening_screen):
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

        opening_screen.decider_frame.destroy()
        self.menu = opening_screen.window
        self.opening_screen = opening_screen

        self.players, self.rounds = None, None

        self.name_font = '-*-Microsoft Sans Serif-Normal-R-*--*-700-*-*-*-*-ISO8859-1'
        self.sub_font = '-*-Microsoft Sans Serif-Normal-R-*--*-400-*-*-*-*-ISO8859-1'
        self.small_font = '-*-Microsoft Sans Serif-Normal-R-*--*-240-*-*-*-*-ISO8859-1'
        self.font = '-*-Microsoft Sans Serif-Normal-R-*--*-480-*-*-*-*-ISO8859-1'

        self.menu.wm_title("Shut The Box - Setup")
        self.options_menu_frame = tk.Frame(master=self.menu, height=615, width=500, bg='blue')
        self.options_menu_frame.pack()
        self.menu.resizable(False, False)
        self.name_text = tk.Label(master=self.menu, text='Shut the Box', bg='blue', fg='yellow',
                                  font=self.name_font)
        self.name_text.place(x=45, y=10)
        self.rules_button = tk.Label(master=self.menu, text='The Rules', bg='black', fg='yellow', relief='ridge',
                                     font=self.small_font, height=1, bd=3, width=9)
        self.rules_button.bind('<Button-1>', self.display_rules)
        self.rules_button.place(x=50, y=125)

        self.show_dice_animation_button_var = True

        self.show_dice_animation_button = tk.Label(master=self.menu, text='Show Dice Roll Animation',
                                                   bg='black', fg='yellow', relief='ridge',
                                                   font=self.small_font, height=1, bd=3, width=23)
        self.show_dice_animation_button.bind('<Button-1>', self.toggle_roll_animation)
        self.show_dice_animation_button.place(x=50, y=165)

        self.player_count_text = tk.Label(master=self.menu, text='Select Number of Players', bg='blue',
                                          fg='yellow', font=self.sub_font)
        self.player_count_text.place(x=27, y=215)
        # Player Count Boxes
        self.player_count_button = []
        self.player_box = tk.Frame(master=self.menu, height=150, width=700, bd=5, bg='blue',
                                   relief='ridge')
        self.player_box.place(x=250, y=350, anchor=tk.CENTER)
        row = 0
        drop_column = 1
        for i in range(1, 12):
            column = i
            if i == 7:
                row = 1
            if i >= 7:
                column = drop_column
                drop_column = drop_column + 1
            main_colour, secondary_colour = self.colours[i - 1]
            self.player_count_button.append(
                tk.Label(master=self.player_box, width=2, height=1, bd=5, relief='ridge', text=i, font=self.font,
                         bg=main_colour, fg=secondary_colour))
            self.player_count_button[len(self.player_count_button) - 1].grid(row=row, column=column)
            self.player_count_button[len(self.player_count_button) - 1].bind('<Button-1>',
                                                                             self.player_button_clicked, i)
        # Round Boxes
        self.round_button = []
        self.round_box = tk.Frame(master=self.menu, height=150, width=700, bd=5, bg='blue',
                                  relief='ridge')
        self.round_box.place(x=250, y=525, anchor=tk.CENTER)
        for i in range(1, 6):
            self.round_button.append(
                tk.Label(master=self.round_box, width=2, height=1, bd=5, relief='ridge', text=i, font=self.font,
                         bg='black', fg='yellow'))
            self.round_button[len(self.round_button) - 1].grid(row=0, column=i)
            self.round_button[len(self.round_button) - 1].bind('<Button-1>',
                                                               self.round_button_clicked, i)

        self.round_text = tk.Label(master=self.menu, text='Rounds', font=self.sub_font, bg='blue', fg='yellow')
        self.round_text.place(x=175, y=425)

        self.start_button = tk.Label(master=self.menu, text='Start Game', height=1, relief='ridge', bd=3, width=9,
                                     bg='black', fg='yellow', font=self.small_font)
        self.start_button.bind('<Button-1>', self.game_start_check)
        self.start_button.place(x=285, y=570)

        self.exit_button_2 = tk.Label(master=self.menu, text='Exit', height=1, relief='ridge', bd=3, width=4,
                                      bg='black', fg='yellow', font=self.small_font)
        self.exit_button_2.bind('<Button-1>', self.menu_quit)
        self.exit_button_2.place(x=425, y=570)

        self.site_button = tk.Label(master=self.menu, text='shutthebox.club', height=1, relief='ridge', bd=4, width=13,
                                    bg='black', fg='yellow', font=self.small_font)
        self.site_button.place(x=10, y=570)
        self.site_button.bind('<Button-1>', self.display_site)

        self.options_complete = True

        self.menu.mainloop()

    def toggle_roll_animation(self, *args):
        if self.show_dice_animation_button_var:
            self.show_dice_animation_button_var = False
            self.show_dice_animation_button.config(fg='grey')
        else:
            self.show_dice_animation_button_var = True
            self.show_dice_animation_button.config(fg='yellow')

        print("Show dice roll", self.show_dice_animation_button_var)

    def menu_quit(self, *args):
        if tk.messagebox.askokcancel(title='Quit Confirm', message='Are you Sure you want to Quit?'):
            self.menu.destroy()

    def game_start_check(self, *args):
        issue = ''
        self.issues = False
        if self.players is None or self.players > 11 or self.players < 2:
            self.issues = True
            issue += 'You need to select between 2 and 11 players!\n'
        if self.rounds is None:
            self.issues = True
            issue += '\nYou need to select the amount of rounds you want to play!'

        if self.issues:
            tk.messagebox.askretrycancel('Oops!', message=issue)
        else:
            self.menu.destroy()
            self.game_instance = OfflineGame.static_build(self.rounds, self.players,
                                                          self.show_dice_animation_button_var, self.opening_screen)

    def display_rules(self, *args):
        wbopen('https://shutthebox.club/the-game/')

    def display_site(self, *args):
        wbopen('https://shutthebox.club/')

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
        self.reset_colours()
        self.player_count_button[num - 1].config(fg='grey')
        self.players = num

    def reset_colours(self):
        for i in range(11):
            main_colour, secondary_colour = self.colours[i]
            self.player_count_button[i].config(fg=secondary_colour)


class OfflineGame():
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
        self.stats_location = 'https://stats.shutthebox.club/'
        # Initialise Some Variables
        self.single_dice_on = False
        self.player_turn = 0
        self.board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.round = 1
        self.awaiting_number = False
        self.acceptable_inputs = []

        self.players, self.rounds = None, None
        self.options_complete = False
        self.show_roll_animation = True
        self.opening_screen = None

    @staticmethod
    def static_build(rounds, players, show_roll_animation, opening_screen):
        obj = OfflineGame.__call__()
        obj.__init__()
        obj.absorb_settings(rounds, players, show_roll_animation, opening_screen)
        return (obj)

    def absorb_settings(self, rounds, players, show_roll_animation, opening_screen):
        print(rounds, players)
        self.rounds = rounds
        self.players = players
        self.show_roll_animation = show_roll_animation
        self.opening_screen = opening_screen
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
        self.splash_label.place_forget()
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

    def gather_stats(self):
        if not (internet_connected and has_internet(self.stats_location)):
            if not has_internet(self.stats_location):
                print('cannot connect to:', self.stats_location)
            return ((None, None, None, None))
        _request = request.Request(self.stats_location + 'abbrv_stats/', headers={'User-Agent': 'python'})
        data = json.loads(request.urlopen(_request).read().decode('utf-8'))
        return ((data['stdev'], data['averages'], data['h_score'], data['l_score']))

    def close_window(self, x):
        if tk.messagebox.askokcancel('Exit Game', 'Are you sure you wish to exit?'):
            self.window.destroy()

    def new_game(self, x):
        if tk.messagebox.askokcancel('Start New Game', 'Are you sure you wish to start a new game?'):
            self.window.destroy()
            self.opening_screen.__init__()

    def move_on_turn(self, x):
        if tk.messagebox.askokcancel('End Turn', 'Are you sure you wish to end this turn?'):
            self.next_turn()

    def gen_round_text(self):
        return ('ROUND ' + str(self.round) + ' OF ' + str(self.rounds))

    def single_dice_option(self, val):
        self.single_dice_available = val
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
        # self.disable_roll_animation
        if (type(x) is tk.Event) or (x is None):
            self.throw_dice_button.bind("<Button-1>", self.do_nothing)
            self.throw_dice_button.config(fg='grey')
            if self.single_dice_on:
                print('Single dice throw called')
                if self.show_roll_animation:
                    self.dice1label.config(text=random.randint(1, 6))
                    self.window.update()
                    self.throw_dice_button.after(40, self.throw_dice_animation, 10, 1)
                else:
                    self.throw_dice_button.after(40, self.throw_dice_animation, 0, 1)

            else:
                print('Double dice throw called')
                if self.show_roll_animation:
                    self.dice1label.config(text=random.randint(1, 6))
                    self.dice2label.config(text=random.randint(1, 6))
                    self.window.update()

                    self.throw_dice_button.after(40, self.throw_dice_animation, 10, 0)
                else:
                    self.throw_dice_button.after(40, self.throw_dice_animation, 0, 0)

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
                if internet_connected and has_internet(self.stats_location):
                    self.submit_stats('/'.join([str(self.rounds)] + [str(x) for x in self.player_scores]))
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

    def submit_stats(self, web_args):
        success = False
        while not success:
            u_name, p_word = self.get_login()
            data = parse.urlencode({'username': u_name, 'password': p_word}).encode()
            url = self.stats_location + 'submit/' + web_args
            _request = request.Request(url, data=data, headers={'User-Agent': 'python'})
            response = request.urlopen(_request, timeout=1).read().decode()
            success = json.loads(response)['was_success']
            if success:
                tk.messagebox.showinfo('Success', 'Successfully posted stats.', master=self.window)
                return (1)
            else:
                retry = tk.messagebox.askretrycancel('Failure', 'Failed to post stats.', master=self.window)
                if not retry:
                    return (0)

    def get_login(self):
        sub_window = tk.Toplevel(master=self.window)

        u_var, p_var = tk.StringVar(), tk.StringVar()

        u_name_box = tk.Entry(sub_window, textvariable=u_var)
        p_word_box = tk.Entry(sub_window, textvariable=p_var, show='*')

        def on_entry(*args):
            sub_window.quit()
            sub_window.destroy()

        tk.Label(master=sub_window, text='Username:').pack(side='top')
        u_name_box.pack(side='top')
        tk.Label(master=sub_window, text='Password:').pack(side='top')
        p_word_box.pack(side='top')
        tk.Button(sub_window, command=on_entry, text='OK').pack(side='top')

        p_word_box.bind('<Return>', on_entry)
        u_name_box.bind('<Return>', on_entry)

        sub_window.lift()
        sub_window.grab_set()
        sub_window.mainloop()

        return ((u_var.get(), p_var.get()))

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
        if 'sub_window' in list(self.__dict__.keys()):
            self.sub_window.destroy()
        self.sub_window = tk.Toplevel(master=self.window)
        self.sub_window_frame = tk.Frame(master=self.sub_window, height=540, width=295, bg='blue')
        self.sub_window_frame.pack()
        self.sub_window.wm_title("Shut The Box - Statistics")
        i = 0
        boxes = []
        stdevs, averages, h_score, l_score = self.gather_stats()
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
        elif event.char == 's':
            print('s pressed')
            if self.single_dice_available:
                print('toggling single dice')
                to_set = 1 if self.single_dice_var.get() == 0 else 0
                self.single_dice_var.set(to_set)
                self.on_single_dice_change()
        else:
            print("pressed", repr(event.char))


Game_Instance = OpeningScreen()
