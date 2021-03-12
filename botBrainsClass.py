#botBrainsClass.py
#imports
import random, re

class bot_brains():
    rand_num_top = 1
    adj_list = []
    is_sleeping = False

    ##commands (command_dict_switch is near the bottom)
    #!QB ----> keyword
    re_keyword = re.compile(r"\b!QB\b")
    #"QB add <word> --->adds a word to the adj list
    #"QB remove <word>" ---> removes a word to the adj list
    #"!QB sleep" --->sleeps the bot.
    #"!QB awake" --->awakens the bot.
    #"!QB calm" ---> reduces the number of times the bot checks messages
    re_command_check = re.compile(r"\b!QB\s(add|remove|calm|sleep|awake)\s([a-z][A-Z]*)\b")
    #"Kill QuirtisBot!" --->kills the bot..
    re_kill_check = re.compile(r"\bKill QuirtisBot!\b")



    def refresh_adj_list(self):
        print("-----------Looking for adj file------------")
        try:
            with open (r"adjectives.txt") as adj_file:
                print("Found adj file.")
                self.adj_list = adj_file.readlines()
        except IOError:
            print("'adjectives.txt' not found.")
            exit()

    def adj_replacer(self, message_content):
        print(f"starting replacer on message '{message_content}'")
        adjrep_output = ""
        for adj in self.adj_list:
            regex_adj = adj.rstrip("\n")
            regex_adj = regex_adj
            adj_check = re.compile(r"\b" + regex_adj + r"\b", re.IGNORECASE)
            if(adj_check.search(message_content)):
                adjrep_output = f"You're {regex_adj}."
                break
        return adjrep_output

    def bot_awaker(self, first_param, orignal_message):
        self.is_sleeping = False
        print("I'm awake.")
        return "Whaaat?"

    def bot_sleeper(self, first_param, orignal_message):
        self.is_sleeping = True
        print("I'm asleep.")
        return "Oh yeah, I was going to tell you something."

    def bot_calmer(self, first_param, orignal_message):
        if self.is_sleeping:
            return
        self.rand_num_top = 3
        print("I'm calm.")
        return "No you."

    def word_adder(self, word_to_add, orignal_message):
        if self.is_sleeping:
            return
        wordadd = word_to_add
        self.adj_list.append(wordadd)
        with open (r"adjectives.txt", "w") as adj_file:
            adj_file.writelines(self.adj_list)
        print(f"'{wordadd}' added")
        return f"Sure, I guess {word_to_add} is a word."

    def word_remover(self, word_to_remove, orignal_message):
        if self.is_sleeping:
            return
        wordrem = word_to_remove
        temp_list = []
        if wordrem in self.adj_list:
            for adj in self.adj_list:
                if adj != wordrem:
                    temp_list.append(adj)
            with open (r"adjectives.txt", "w") as adj_file:
                adj_file.writelines(temp_list)
                self.adj_list = temp_list
            print(f"'{word_to_remove}' removed")
            return f"Wow, I guess {word_to_remove} isn't a word."
        print(f"'{word_to_remove}' is not in the list")
        return

    command_dict_switch = {
    "add": word_adder,
    "remove": word_remover,
    "calm": bot_calmer,
    "sleep": bot_sleeper,
    "awake": bot_awaker
    }

    def message_checker(self, message):
        print(f"checking message: {message.content}")
        if re.search(self.re_keyword, message.content):
            command = re.search(self.re_command_check, message.content)
            output = self.command_dict_switch[command.group(1)](message, command.group(2))
            return output
        if self.is_sleeping:
            return
        if(random.randint(1, self.rand_num_top) == 1):
            print("I'm looking at the message!")
            new_message = self.adj_replacer(message.content)
            if(new_message == ""):
                return ""
            else:
                return new_message
        return ""
