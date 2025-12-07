import random
from enum import Enum

#Class representing a given game
class Game:
    def __init__(self,players,num_days,game_phase,bluffs):
        self.players = players
        self.num_days = num_days
        self.game_phase = game_phase
        self.bluffs = bluffs

    #Returns the demon
    def demon(self):
        return self.players[CharacterType.DEMON][0]
    
    #Prints all the info there is about each player -- for debugging
    def printgameinfo(self):
        print("Days: ",self.num_days,"Game phase: ",self.game_phase)
        for role in self.players:
            for p in self.players[role]:
                print(p.role,p.alignment,p.alive,p.canvote,p.badinfo,p.seat,p.tokens,p.history,"\n")

    #Get a list of all players -- helpful since Game.players is a dict
    def getplayers(self):
        all_players = []
        for type in self.players:
            for p in self.players[type]: all_players.append(p)
        all_players = sorted(all_players, key=lambda player: player.seat)
        return all_players
    
    def incrementtime(self):
        #print("It is currently "+self.game_phase.name+ ". Time to change that!")
        if self.game_phase == GamePhase.NIGHT:
            self.game_phase = GamePhase.DAY
            for player in self.getplayers(): player.tell("It is now DAY")
        elif self.game_phase == GamePhase.DAY:
            self.game_phase = GamePhase.EVENING
            for player in self.getplayers(): player.tell("It is now EVENING")
        elif self.game_phase == GamePhase.EVENING:
            self.num_days = self.num_days+1
            self.game_phase = GamePhase.NIGHT
            for player in self.getplayers():
                player.tell("It is now Round "+str(self.num_days))
                player.tell("It is now NIGHT")


#Class representing a player
class Player:
    def __init__(self,role,alignment,alive,canvote,badinfo,seat,tokens,history):
        self.role = role
        self.alignment = alignment
        self.alive = alive
        self.canvote = canvote
        self.badinfo = badinfo
        self.seat = seat
        self.tokens = tokens
        self.history = history
    
    #Adds a message to player's message history
    def tell(self,msg):
        self.history.append(msg)

    #Use this function to allow a player to choose X players for their ability.
    #This is probably one of the function we'll edit the most for our project
    def choose_players_for_ability(self,g,num):
        choices = random.sample(g.getplayers(),num)
        for choice in choices:
            self.tell("I chose Seat "+str(choice.seat)+" for my ability")
        return choices
    
    # function to allow player to choose a player to talk to
    def choose_player_to_talk_to(self, g):
        players = g.getplayers()
        possible_choices = [player for player in players if player.seat != self.seat]
        choice = random.choice(possible_choices)
        return choice

    def say_publicly(self):
        msg = "Seat "+str(self.seat)+" says publicly: Hi! I am the "+self.role.name
        if random.random()<0.2: return msg
        else: return ""
        #TODO

    def say_privately(self, player_to_tell):
        msg = f"Seat {self.seat} tells you: Hi! I am the {self.role.name}"
        return msg


class GamePhase(Enum):
    NIGHT = 1
    DAY = 2
    EVENING = 3

class Role(Enum):
    WASHERWOMAN = 1
    LIBRARIAN = 2
    INVESTIGATOR = 3
    CHEF = 4
    EMPATH = 5
    FORTUNE_TELLER = 6
    UNDERTAKER = 7
    MONK = 8
    RAVENKEEPER = 9
    VIRGIN = 10
    SLAYER = 11
    SOLDIER = 12
    MAYOR = 13
    BUTLER = 14
    SAINT = 15
    RECLUSE = 16
    DRUNK = 17
    POISONER = 18
    SPY = 19
    BARON = 20
    SCARLET_WOMAN = 21
    IMP = 22

class CharacterType(Enum):
    TOWNSFOLK = 1
    OUTSIDER = 2
    MINION = 3
    DEMON = 4

class Alignment(Enum):
    GOOD = 1
    EVIL = 2

class ReminderToken(Enum):
    WASHERWOMAN_REAL = 1
    WASHERWOMAN_FAKE = 2
    LIBRARIAN_REAL = 3
    LIBRARIAN_FAKE = 4
    INVESTIGATOR_REAL = 5
    INVESTIGATOR_FAKE = 6
    FORTUNE_TELLER_RED_HERRING = 7
    UNDERTAKER_EXECUTED_TODAY = 8
    MONK_SAFE_TONIGHT = 9
    RAVENKEEPER_DIED_TONIGHT = 10
    VIRGIN_HAS_ABILITY = 11
    SLAYER_HAS_ABILITY = 12
    SOLDIER_SAFE = 13
    MAYOR_CAN_REDIRECT = 14
    BUTLER_MASTER = 15
    BUTLER_CAN_VOTE = 16
    RECLUSE_MAY_REGISTER_EVIL = 17
    DRUNK_IS_THE_DRUNK = 18
    POISONER_IS_POISONED = 19
    SPY_MAY_REGISTER_GOOD = 20
    IMP_WILL_DIE_TONIGHT = 21
    MINION_IS_THE_DEMON = 22



role_to_character_type = {
    Role.WASHERWOMAN: CharacterType.TOWNSFOLK,
    Role.LIBRARIAN: CharacterType.TOWNSFOLK,
    Role.INVESTIGATOR: CharacterType.TOWNSFOLK,
    Role.CHEF: CharacterType.TOWNSFOLK,
    Role.EMPATH: CharacterType.TOWNSFOLK,
    Role.FORTUNE_TELLER: CharacterType.TOWNSFOLK,
    Role.UNDERTAKER: CharacterType.TOWNSFOLK,
    Role.MONK: CharacterType.TOWNSFOLK,
    Role.RAVENKEEPER: CharacterType.TOWNSFOLK,
    Role.VIRGIN: CharacterType.TOWNSFOLK,
    Role.SLAYER: CharacterType.TOWNSFOLK,
    Role.SOLDIER: CharacterType.TOWNSFOLK,
    Role.MAYOR: CharacterType.TOWNSFOLK,
    Role.BUTLER: CharacterType.OUTSIDER,
    Role.SAINT: CharacterType.OUTSIDER,
    Role.RECLUSE: CharacterType.OUTSIDER,
    Role.DRUNK: CharacterType.OUTSIDER,
    Role.POISONER: CharacterType.MINION,
    Role.SPY: CharacterType.MINION,
    Role.BARON: CharacterType.MINION,
    Role.SCARLET_WOMAN: CharacterType.MINION,
    Role.IMP: CharacterType.DEMON
}

character_type_to_alignment = {
    CharacterType.TOWNSFOLK: Alignment.GOOD,
    CharacterType.OUTSIDER: Alignment.GOOD,
    CharacterType.MINION: Alignment.EVIL,
    CharacterType.DEMON: Alignment.EVIL,
}

num_players_to_num_roles = {
    7: {
        CharacterType.TOWNSFOLK: 5,
        CharacterType.OUTSIDER: 0,
        CharacterType.MINION: 1,
        CharacterType.DEMON: 1,
        },
    }







#Set up grimoire for 7 players
num_players = 7

players = {
    CharacterType.TOWNSFOLK: [],
    CharacterType.OUTSIDER: [],
    CharacterType.MINION: [],
    CharacterType.DEMON: []
}

seats = list(range(0,num_players))
random.shuffle(seats)
seat = 0


#Assign roles and seats to players
for type in num_players_to_num_roles[num_players]:
    roles_of_this_type = []
    for role in Role:
        if role_to_character_type[role] == type: roles_of_this_type.append(role)
    random_roles = random.sample(roles_of_this_type,num_players_to_num_roles[num_players][type])
    #if type == CharacterType.TOWNSFOLK: random_roles = [Role.WASHERWOMAN, Role.LIBRARIAN, Role.INVESTIGATOR, Role.MAYOR, Role.MONK]
    #if type == CharacterType.MINION: random_roles = [Role.BARON]
    for role in random_roles:
        players[role_to_character_type[role]].append(Player(role,character_type_to_alignment[role_to_character_type[role]],True,True,False,seats[seat],[],[]))
        seat = seat + 1

# Create list of not in play good characters
all_roles = []
for role in Role:
    if role_to_character_type[role]==CharacterType.TOWNSFOLK or role_to_character_type[role]==CharacterType.OUTSIDER: all_roles.append(role)
for type in players:
    for p in players[type]:
        if p.role in all_roles: all_roles.remove(p.role)


# handle for the baron
in_play_minions = players[CharacterType.MINION]
for minion in in_play_minions:
    if minion.role == Role.BARON:
        # find two outsiders to add to the game
        out_of_play_outsiders = [role for role in all_roles if role_to_character_type[role]==CharacterType.OUTSIDER]
        added_outsiders = random.sample(out_of_play_outsiders, 2)
        # randomly pick two townsfolk to remove
        in_play_townsfolk = players[CharacterType.TOWNSFOLK]
        townsfolk_removed = random.sample(in_play_townsfolk, 2)
        # find the role and seat of the removed townsfolk 
        removed_townsfolk_role_1 = townsfolk_removed[0].role
        removed_townsfolk_seat_1 = townsfolk_removed[0].seat
        removed_townsfolk_role_2 = townsfolk_removed[1].role
        removed_townsfolk_seat_2 = townsfolk_removed[1].seat
        # create new outsider players
        new_outsider_1 = Player(added_outsiders[0],character_type_to_alignment[CharacterType.OUTSIDER], True, True, False, removed_townsfolk_seat_1, [], [])
        new_outsider_2 = Player(added_outsiders[1], character_type_to_alignment[CharacterType.OUTSIDER], True, True, False, removed_townsfolk_seat_2, [], [])
        # add the outsiders 
        players[CharacterType.OUTSIDER].append(new_outsider_1)
        players[CharacterType.OUTSIDER].append(new_outsider_2)
        # remove the townsfolk
        for p in players[CharacterType.TOWNSFOLK]:
            if p==townsfolk_removed[0] or p==townsfolk_removed[1]: players[CharacterType.TOWNSFOLK].remove(p)
        #for i in range(len(players[CharacterType.TOWNSFOLK])):
            #if players[CharacterType.TOWNSFOLK][i].role == removed_townsfolk_role_1 or players[CharacterType.TOWNSFOLK][i].role == removed_townsfolk_role_2:
                #players[CharacterType.TOWNSFOLK].pop(i)

        # add the no longer in play townsfolk to all_roles
        all_roles.append(removed_townsfolk_role_1)
        all_roles.append(removed_townsfolk_role_2)
        # remove the newly added outsiders from all_roles
        for role in all_roles:
            if role == added_outsiders[0] or role == added_outsiders[1]: all_roles.remove(role)
        #print(added_outsiders)
        #for i in range(len(all_roles)):
            #if all_roles[i] == added_outsiders[0] or all_roles[i] == added_outsiders[1]:
                #all_roles.pop(i)


# townsfolk that aren't in play
available_townsfolk = [role for role in all_roles if role_to_character_type[role]==CharacterType.TOWNSFOLK]
# list of outsiders
outsiders = players[CharacterType.OUTSIDER]
# find if there is a drunk, remove it and add a not in play townsfolk in the same seat
for i in range(len(outsiders)):
    if outsiders[i].role == Role.DRUNK:
        seat = outsiders[i].seat
        players[CharacterType.OUTSIDER].pop(i)
        new_townsfolk = random.choice(available_townsfolk)
        players[CharacterType.TOWNSFOLK].append(Player(new_townsfolk, character_type_to_alignment[CharacterType.TOWNSFOLK], True, True, False, seat, [], []))

        # randomly assign a townsfolk to be the drunk
        random_player = random.randint(0, len(players[CharacterType.TOWNSFOLK]) - 1)
        players[CharacterType.TOWNSFOLK][random_player].badinfo = True
        players[CharacterType.TOWNSFOLK][random_player].tokens.append(ReminderToken.DRUNK_IS_THE_DRUNK)
        
       
        # remove the added townsfolk from all_roles
        for role in all_roles:
            if role == new_townsfolk: all_roles.remove(role)
        #for i in range(len(all_roles)):
            #if all_roles[i] == new_townsfolk:
                #all_roles.pop(i)
                
        break


# generate random bluffs  
bluffs = random.sample(all_roles,3)


#make the Game object
g = Game(players,0,GamePhase.EVENING,bluffs)

def do_day(g, num_conversations):
    players = g.getplayers()
    # tell everyone who died in the night
    dead_player = None
    for p in players:
        if ReminderToken.IMP_WILL_DIE_TONIGHT in p.tokens: 
            dead_player = p
    if dead_player:
        for p in players:
            p.tell(f"Seat {dead_player.seat} died in the night.")
        dead_player.tokens.remove(ReminderToken.IMP_WILL_DIE_TONIGHT)
    else:
        for p in players:
            p.tell("Nobody died in the night")
    
    # start private discussion
    for p in players:
        p.tell("Private discussion starts")
    for i in range(num_conversations):
        for p in g.getplayers():
            p.tell("Choose a player to talk to")
            choice = p.choose_player_to_talk_to(g)
            msg = p.say_privately(choice)
            choice.tell(msg)
            



def do_evening(g):
    #public discussion
    num_speech_turns = 2
    players = g.getplayers()
    random.shuffle(players)
    for p in players:
        p.tell("Public discussion starts")
    for i in range(0,num_speech_turns):
        for p in players:
            msg = p.say_publicly()
            if msg!="":
                for q in players: q.tell(msg)
    
    #noms


def first_night(g):
    #Players need to know what their role is
    for type in g.players:
        for p in g.players[type]:
            p.tell("Your role is "+p.role.name)
            p.tell("Your type is "+role_to_character_type[p.role].name)
            p.tell("Your alignment is "+character_type_to_alignment[role_to_character_type[p.role]].name)

    g.incrementtime()
    #Do first night

    #The Drunk
    #TODO: Does the Drunk work?

   
    # decide red herring if ft in play
    for p in g.getplayers():
        if p.role == Role.FORTUNE_TELLER and ReminderToken.DRUNK_IS_THE_DRUNK not in p.tokens:
            red_herring(g)

    #Minion info
    for p in g.players[CharacterType.MINION]:
        p.tell("Seat "+str(g.demon().seat)+" is the Demon")

    #Demon info
    for p in g.players[CharacterType.DEMON]:
        for q in g.players[CharacterType.MINION]:
            p.tell("Seat "+str(q.seat)+" is a Minion")
        for bluff in g.bluffs:
            p.tell(bluff.name+" is not in play")


    # first night abilities
    # minions
    poisoner(g)
    spy(g)

    #townsfolk 
    washerwoman(g)
    librarian(g)
    investigator(g)
    chef(g)
    empath(g)
    fortune_teller(g)
    butler(g)


def other_nights(g):
    players = g.getplayers()
    # poisoner goes first 
    for p in players:
        if p.role == Role.POISONER and p.alive:
            poisoner(g)
    
    # monk goes
    for p in players:
        if p.role == Role.MONK and p.alive:
            monk(g)
    
    # spy goes
    for p in players:
        if p.role == Role.SPY and p.alive:
            spy(g)

    # scarlet woman goes
    for p in players:
        if p.role == Role.SCARLET_WOMAN and p.alive:
            scarlet_woman(g)
    
    # imp goes
    for p in players:
        if p.role == Role.IMP and role.alive:
            imp(g)
    
    # ravenkeeper goes
    for p in players:
        if p.role == Role.RAVENKEEPER:
            ravenkeeper(g)

    # undertaker goes
    for p in players:
        if p.role == Role.UNDERTAKER and p.alive:
            undertaker(g)
    
    # empath goes
    for p in players:
        if p.role == Role.EMPATH and p.alive:
            empath(g)
    
    # fortune teller goes
    for p in players:
        if p.role == Role.FORTUNE_TELLER and p.alive:
            fortune_teller(g)
    
    # butler goes 
    for p in players:
        if p.role == Role.BUTLER and p.alive:
            butler(g)


def start_game(g):
    alive_players = g.getplayers()
    game_over = False

    # do the first night
    first_night(g)


    g.incrementtime()
    # loop for rest of the game
    while not game_over:
        #daytime happens, each player can tell something to three other players
        do_day(g, 3)
        g.incrementtime()
        # do evening
        do_evening(g)
        # update alive players list
        for player in alive_players:
            if not player.alive:
                alive_players.remove(player)

        # check if there is no alive imp, if so, stop game loop
        for player in alive_players:
            if player.role == Role.IMP and p.alive:
                game_over = False
                break
            if player.role == Role.IMP and p.dead:
                game_over = True
        if game_over:
            break
        
        # if less than three alive players, stop game loop
        if len(alive_players) < 3:
            # game is over
            break
        
        g.incrementtime()
        # do next night
        other_nights(g)
        # update alive players list
        for player in alive_players:
            if not player.alive:
                alive_players.remove(player)
        
        # check if there is no alive imp, if so, stop game loop
        for player in alive_players:
            if player.role == Role.IMP and p.alive:
                game_over = False
                break
            if player.role == Role.IMP and p.dead:
                game_over = True
        if game_over:
            break
        
        # if there are less than three alive players, stop game loop
        if len(alive_players) < 3:
            # game is over
            break

        g.incrementtime()
        



    
#Poisoner poisons someone
def poisoner(g):
    for p in g.getplayers():
        if ReminderToken.POISONER_IS_POISONED in p.tokens: p.tokens.remove(ReminderToken.POISONER_IS_POISONED)
    for p in g.getplayers():
        if p.role == Role.POISONER:
            p.tell("Pick 1 player for your ability")
            choice = p.choose_players_for_ability(g,1)
            choice[0].tokens.append(ReminderToken.POISONER_IS_POISONED)
            if choice[0].badinfo == False: choice[0].badinfo = True


# spy sees grim
def spy(g):
    players = g.getplayers()
    for p in players:
        if p.role == Role.SPY:
            for player in players:
                p.tell(f"Seat {player.seat} is {player.role.name}")
                for token in player.tokens:
                    p.tell(f"Seat {player.seat} has the {token} token") 

#Washerwoman gets info
def washerwoman(g):
    for p in g.getplayers():
        if p.role == Role.WASHERWOMAN:
            possible_pings = g.players[CharacterType.TOWNSFOLK].copy()
            possible_pings.remove(p)
            # remove the drunk from the possible pings
            for ping in possible_pings:
                if ReminderToken.DRUNK_IS_THE_DRUNK in ping.tokens:
                    possible_pings.remove(ping)
            real_person = random.sample(possible_pings,1)[0]
            possible_pings.remove(real_person)
            possible_pings = possible_pings+g.players[CharacterType.OUTSIDER]+g.players[CharacterType.MINION]+g.players[CharacterType.DEMON]
            fake_person = random.sample(possible_pings,1)[0]
            real_person.tokens.append(ReminderToken.WASHERWOMAN_REAL)
            fake_person.tokens.append(ReminderToken.WASHERWOMAN_FAKE)
            pings = [real_person,fake_person]
            random.shuffle(pings)
            p.tell("From your ability you learn either Seat "+str(pings[0].seat)+" or Seat "+str(pings[1].seat)+" is the "+real_person.role.name)


#Librarian gets info
def librarian(g):
    for p in g.getplayers():
        if p.role == Role.LIBRARIAN:
            if not g.players[CharacterType.OUTSIDER]: p.tell("From your ability you learn there are 0 outsiders.")
            else:
                possible_pings = g.players[CharacterType.OUTSIDER].copy()
                # add the drunk to possible pings if there is a drunk in play
                for townsfolk in g.players[CharacterType.TOWNSFOLK]:
                    if townsfolk.role != Role.LIBRARIAN and ReminderToken.DRUNK_IS_THE_DRUNK in townsfolk.tokens:
                        possible_pings.append(townsfolk)
                real_person = random.sample(possible_pings,1)[0]
                possible_pings.remove(real_person)
                possible_pings = possible_pings+g.players[CharacterType.TOWNSFOLK]+g.players[CharacterType.MINION]+g.players[CharacterType.DEMON]
                possible_pings.remove(p)
                fake_person = random.sample(possible_pings,1)[0]
                real_person.tokens.append(ReminderToken.LIBRARIAN_REAL)
                fake_person.tokens.append(ReminderToken.LIBRARIAN_FAKE)
                pings = [real_person,fake_person]
                # make sure the librarian learns the Drunk and not a townsfolk if librarian is learning the drunk
                outsider_to_learn = Role.DRUNK.name if ReminderToken.DRUNK_IS_THE_DRUNK in real_person.tokens else real_person.role.name
                random.shuffle(pings)
                p.tell("From your ability you learn either Seat "+str(pings[0].seat)+" or Seat "+str(pings[1].seat)+" is the "+ outsider_to_learn)


#Investigator gets info
def investigator(g):
    for p in g.getplayers():
        if p.role == Role.INVESTIGATOR:
            possible_pings = g.players[CharacterType.MINION].copy()
            real_person = random.sample(possible_pings,1)[0]
            possible_pings.remove(real_person)
            possible_pings = possible_pings+g.players[CharacterType.TOWNSFOLK]+g.players[CharacterType.OUTSIDER]+g.players[CharacterType.DEMON]
            possible_pings.remove(p)
            fake_person = random.sample(possible_pings,1)[0]
            real_person.tokens.append(ReminderToken.INVESTIGATOR_REAL)
            fake_person.tokens.append(ReminderToken.INVESTIGATOR_FAKE)
            pings = [real_person,fake_person]
            random.shuffle(pings)
            p.tell("From your ability you learn either Seat "+str(pings[0].seat)+" or Seat "+str(pings[1].seat)+" is the "+real_person.role.name)


#Chef gets info
def chef(g):
    player_list = g.getplayers()
    evil_pairs = 0
    for i in range(len(player_list)):
        if i != len(player_list) - 1:
            if player_list[i].alignment == Alignment.EVIL and player_list[i+1].alignment == Alignment.EVIL:
                evil_pairs += 1
        else:
            if player_list[i].alignment == Alignment.EVIL and player_list[0].alignment == Alignment.EVIL:
                evil_pairs += 1

    for p in g.getplayers():
        if p.role == Role.CHEF:
            p.tell("There are " + str(evil_pairs) + "pairs of evil players")



#Empath gets info
def empath(g):
    player_list = g.getplayers()
    for p in player_list:
        if not p.alive:
            player_list.remove(p)
    evil_empath_neighbors = 0
    empath_neighbor_seats = []
    for i in range(len(player_list)):
        if player_list[i].role == Role.EMPATH:
            if i == len(player_list) - 1:
                empath_neighbor_seats.append(player_list[0].seat)
                empath_neighbor_seats.append(player_list[i-1].seat)
                if player_list[0].alignment == Alignment.EVIL:
                    evil_empath_neighbors += 1
                if player_list[i-1].alignment == Alignment.EVIL:
                    evil_empath_neighbors += 1
            elif i == 0:
                empath_neighbor_seats.append(player_list[i+1].seat)
                empath_neighbor_seats.append(player_list[len(player_list)-1].seat)
                if player_list[i+1].alignment == Alignment.EVIL:
                    evil_empath_neighbors += 1
                if player_list[len(player_list)-1].alignment == Alignment.EVIL:
                    evil_empath_neighbors += 1
            else:
                empath_neighbor_seats.append(player_list[i+1].seat)
                empath_neighbor_seats.append(player_list[i-1].seat)
                if player_list[i+1].alignment == Alignment.EVIL:
                    evil_empath_neighbors += 1
                if player_list[i-1].alignment == Alignment.EVIL:
                    evil_empath_neighbors += 1
    for p in g.getplayers():
        if p.role == Role.EMPATH:
            p.tell(str(evil_empath_neighbors) + " of seats " + str(empath_neighbor_seats[0]) + " and " + str(empath_neighbor_seats[1]) + " are evil")

                

# randomly assign fortune teller red herring to a good player if there is a non-drunk ft in play
def red_herring(g):
    good_players = [player for player in g.getplayers() if player.alignment == Alignment.GOOD]
    red_herring = random.choice(good_players)
    red_herring.tokens.append(ReminderToken.FORTUNE_TELLER_RED_HERRING)


#Fortune teller gets info
def fortune_teller(g):
    for p in g.getplayers():
        if p.role == Role.FORTUNE_TELLER:
            p.tell("Pick two players for your ability")
            ft_choices = p.choose_players_for_ability(g,2)
            if ReminderToken.FORTUNE_TELLER_RED_HERRING in ft_choices[0].tokens or role_to_character_type[ft_choices[0].role] == CharacterType.DEMON or ReminderToken.FORTUNE_TELLER_RED_HERRING in ft_choices[1].tokens or role_to_character_type[ft_choices[1].role] == CharacterType.DEMON:
                p.tell("One of seat" + str(ft_choices[0].seat) + "or seat" + str(ft_choices[1].seat) + "is the demon")
            else:
                p.tell("Neither seat" + str(ft_choices[0].seat) + "or seat" + str(ft_choices[1].seat) + "is the demon")


def butler(g):
    #Butler gets info
    for p in g.getplayers():
        if p.role == Role.BUTLER:
            choice = p.choose_players_for_ability(g,1)[0]
            choice.tokens.append(ReminderToken.BUTLER_MASTER)
            #They CAN CHOOSE THEMSELVES! TODO fix.








# monk selects a player to protect
def monk(g):
    for p in g.getplayers():
        if p.role == Role.MONK and p.alive:
            p.tell("Pick one player for your ability")
            choice = p.choose_players_for_ability(g, 1)
            if ReminderToken.DRUNK_IS_THE_DRUNK not in p.tokens and ReminderToken.POISONER_IS_POISONED not in p.tokens:
                choice[0].tokens.append(ReminderToken.MONK_SAFE_TONIGHT)





# tell scarlet woman they become the demon, if they do
def scarlet_woman(g):
    for p in g.getplayers():
        if p.role == Role.SCARLET_WOMAN and ReminderToken.MINION_IS_THE_DEMON in p.tokens:
            p.tell("You are the " + Role.IMP.name)
            p.tell("You are a " + role_to_character_type[Role.IMP].name)
            p.tell("You are " + character_type_to_alignment[CharacterType.DEMON].name)
            p.tokens.remove(ReminderToken.MINION_IS_THE_DEMON)


# imp goes
def imp(g):
    for p in g.getplayers():
        if p.role == Role.IMP:
            p.tell("Pick one player for your ability")
            choice = p.choose_players_for_ability(g, 1)
            if ReminderToken.POISONER_IS_POISONED not in p.tokens:
                if ReminderToken.MONK_SAFE_TONIGHT not in choice[0].tokens:
                    if ReminderToken.SOLDIER_SAFE not in choice[0].tokens or ReminderToken.POISONER_IS_POISONED in choice[0].tokens:
                        choice[0].tokens.append(ReminderToken.IMP_WILL_DIE_TONIGHT)
                        choice[0].alive = False
                        if choice[0].seat == p.seat:
                            star_pass(g)


# ravenkeeper goes
def ravenkeeper(g):
    for p in g.getplayers():
        if p.role == Role.RAVENKEEPER and ReminderToken.RAVENKEEPER_DIED_TONIGHT in p.tokens:
            p.tell("Pick one player for your ability.")
            choice = p.choose_players_for_ability(g, 1)
            choice_seat = choice[0].seat
            choice_character = choice[0].role
            p.tell(f"Seat {choice_seat} is {choice_character}.")




# undertaker goes
def undertaker(g):
    for p in g.getplayers():
        if p.role == Role.UNDERTAKER and p.alive:
            for pl in g.getplayers():
                if ReminderToken.UNDERTAKER_EXECUTED_TODAY in pl.tokens:
                    executed_role = pl.role
                    executed_seat = pl.seat
                    p.tell(f"Seat {executed_seat} is {executed_role}.")
                    pl.tokens.remove(ReminderToken.UNDERTAKER_EXECUTED_TODAY)


def star_pass(g):
    minions = []
    for p in g.getplayers():
        if role_to_character_type[p.role] == CharacterType.MINION and p.alive:
            minions.append(p)
    if minions != []:
        for minion in minions:
            if minion.role == Role.SCARLET_WOMAN and minion.alive:
                minion.role = Role.IMP
                minion.tell("You are now the Imp. You are evil.")
                return
        
        minion_to_imp = random.choice(minions)
        minion_to_imp.tell("You are now the Imp. You are evil.")
        




start_game(g)









    

g.printgameinfo()