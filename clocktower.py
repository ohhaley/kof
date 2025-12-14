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
    def __init__(self,role,alignment,alive,canvote,badinfo,seat,tokens,history, name):
        self.role = role
        self.alignment = alignment
        self.alive = alive
        self.canvote = canvote
        self.badinfo = badinfo
        self.seat = seat
        self.tokens = tokens
        self.history = history
        self.name = name
    
    #Adds a message to player's message history
    def tell(self,msg):
        self.history.append(msg)

    #Use this function to allow a player to choose X players for their ability.
    #This is probably one of the function we'll edit the most for our project
    def choose_players_for_ability(self,g,num):
        choices = random.sample(g.getplayers(),num)
        for choice in choices:
            self.tell(f"I chose {choice.name} for my ability")
        return choices
    
    # function to allow player to choose a player to talk to
    def choose_player_to_talk_to(self, g):
        players = g.getplayers()
        possible_choices = [player for player in players if player.seat != self.seat]
        choice = random.choice(possible_choices)
        return choice

    def say_publicly(self):
        msg = f"{self.name} says publicly: Hi! I am the "+self.role.name
        if random.random()<0.2: return msg
        else: return ""
        #TODO

    def say_privately(self, player_to_tell):
        msg = f"{self.name} tells you: Hi! I am the {self.role.name}"
        return msg
    
    def nominate_someone_or_not(self,can_be_nominated):
        #maybe you don't want to nom
        if random.random() > 0.5:
            self.tell("I did not nominate anyone")
            return None
        choice = random.choice(can_be_nominated)
        self.tell(f"I nominated {choice.name}")
        return choice
    
    def getvote(self,nominee,butler_master_voted=False):
        if self.role == Role.BUTLER and butler_master_voted == False:
            self.tell("I could not vote because I am the BUTLER")
            return False
        #if self.role == Role.BUTLER: print("\n\n\n\n\n\n\n\n********HOLD THE PHONE I GOT TO VOTE EVEN THOUGH I'M THE BUTLER**********\n\n\n\n\n\n\n")
        if random.random() > 0.5:
            #vote
            self.tell(f"I voted for {nominee.name}")
            if not self.alive: self.canvote = False
            return True
        else:
            #no vote
            self.tell("I did not vote")
            return False


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

names = ["Red", "Orange", "Yellow", "Purple", "Green", "Blue", "Pink", "Black", "White", "Brown", "Gray", "Indigo", "Violet", "Cyan", "Lime",]

#Assign roles and seats to players
for type in num_players_to_num_roles[num_players]:
    roles_of_this_type = []
    for role in Role:
        if role_to_character_type[role] == type: roles_of_this_type.append(role)
    random_roles = random.sample(roles_of_this_type,num_players_to_num_roles[num_players][type])
    #if type == CharacterType.TOWNSFOLK: random_roles = [Role.WASHERWOMAN, Role.LIBRARIAN, Role.INVESTIGATOR, Role.MAYOR, Role.MONK]
    #if type == CharacterType.MINION: random_roles = [Role.BARON]
    for role in random_roles:
        name = random.choice(names)
        players[role_to_character_type[role]].append(Player(role,character_type_to_alignment[role_to_character_type[role]],True,True,False,seats[seat],[],[], name))
        seat = seat + 1
        names.remove(name)

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
        new_outsider_1 = Player(added_outsiders[0],character_type_to_alignment[CharacterType.OUTSIDER], True, True, False, removed_townsfolk_seat_1, [], [], townsfolk_removed[0].name)
        new_outsider_2 = Player(added_outsiders[1], character_type_to_alignment[CharacterType.OUTSIDER], True, True, False, removed_townsfolk_seat_2, [], []townsfolk_removed[1].name)
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
        players[CharacterType.TOWNSFOLK].append(Player(new_townsfolk, character_type_to_alignment[CharacterType.TOWNSFOLK], True, True, False, seat, [], [], outsiders[i].name))

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
            p.tell(f"{dead_player.name} died in the night.")
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
    can_nominate = g.getplayers()
    for player in can_nominate:
            if not player.alive:
                can_nominate.remove(player) 
    can_be_nominated = []
    for player in can_nominate:
        can_be_nominated.append(player)

    votes_to_die = round(len(can_nominate)/2)-1
    on_the_block = None
    for player in can_nominate:
        player.tell("Would you like to nominate someone? If so, who?")
        nominee = player.nominate_someone_or_not(can_be_nominated)
        if not nominee == None:
            can_be_nominated.remove(nominee)
            total_votes = 0
            players = g.getplayers()
            players_in_order = []
            players_counterclockwise = []
            for i in range(nominee.seat + 1, len(players)):
                players_in_order.append(players[i])
            for i in range(nominee.seat + 1):
                players_counterclockwise.append(players[i])
            players_in_order.extend(players_counterclockwise)
            butler_master_voted = False
            for p in players_in_order:
                if p.canvote:
                    #print(p.seat,p.role.name,p.alive,p.canvote)
                    p.tell("Seat "+str(player.seat)+" has nominated Seat "+str(nominee.seat))
                    p.tell("Total votes right now: "+str(total_votes)+", total needed: "+str(votes_to_die))
                    didvote = p.getvote(nominee,butler_master_voted=butler_master_voted)
                    if didvote:
                        total_votes = total_votes+1
                        if ReminderToken.BUTLER_MASTER in p.tokens: butler_master_voted = True
                        for q in g.getplayers():
                            if p.alive:
                                q.tell("Total votes: "+str(total_votes)+", as Seat "+str(p.seat)+" has voted")
                            else:
                                q.tell("Total votes: "+str(total_votes)+", as Seat "+str(p.seat)+" has voted, using a deadvote")
                    #print("Butler master voted: "+str(butler_master_voted))
            print(total_votes,votes_to_die)
            if total_votes > votes_to_die:
                on_the_block = nominee
                votes_to_die = total_votes
                for p in g.getplayers():
                    p.tell("There were "+str(total_votes)+", with "+str(votes_to_die)+" needed")
                    p.tell("Seat "+str(nominee.seat)+" is on the block")
            elif total_votes == votes_to_die:
                on_the_block = None
                for p in g.getplayers():
                    p.tell("There were "+str(total_votes)+", with "+str(votes_to_die)+" needed")
                    p.tell("No one is on the block")

    if not on_the_block == None:
        print("Seat "+str(on_the_block.seat)+" was executed")
        for p in g.getplayers(): p.tell("Seat "+str(on_the_block.seat)+" was executed and dies")
        on_the_block.alive = False
        if on_the_block.role == Role.IMP:
            for p in g.getplayers():
                if p.role == Role.SCARLET_WOMAN and p.alive:
                    p.tokens.append(ReminderToken.MINION_IS_THE_DEMON)
                    scarlet_woman(g)
    else:
        print("No one was executed")
        for p in g.getplayers(): p.tell("No one was executed")
                    

    


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
        if p.role == Role.IMP and p.alive:
            #print("Imp acting on other night")
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


#game loop
def start_game(g):
    print(g.printgameinfo())
    alive_players = g.getplayers()
    game_over = False

    # do the first night
    first_night(g)


    g.incrementtime()
    # loop for rest of the game
    while not game_over:
        print(g.num_days,g.game_phase.name,len(alive_players)," players")
        #daytime happens, each player can tell something to three other players
        do_day(g, 3)
        g.incrementtime()
        #print(g.game_phase)
        # do evening
        do_evening(g)
        # update alive players list
        for player in alive_players:
            if not player.alive:
                alive_players.remove(player)

        if g.num_days > 100:
            break

        game_over = True
        # check if there is no alive imp, if so, stop game loop
        for player in alive_players:
            if player.role == Role.IMP and p.alive:
                game_over = False
                break
        if game_over:
            break
        
        # if less than three alive players, stop game loop
        if len(alive_players) < 3:
            # game is over
            break
        
        g.incrementtime()
        #print(g.game_phase)
        # do next night
        other_nights(g)
        # update alive players list
        for player in alive_players:
            if not player.alive:
                alive_players.remove(player)
        
        game_over = True
        # check if there is no alive imp, if so, stop game loop
        for player in alive_players:
            if player.role == Role.IMP and p.alive:
                game_over = False
                break
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
            if ReminderToken.POISONER_IS_POISONED not in p.tokens and ReminderToken.DRUNK_IS_THE_DRUNK not in p.tokens:
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
            else:
                possible_pings = g.getplayers()
                possible_pings.remove(p)
                possible_characters = [role for role in Role if role_to_character_type[role] == CharacterType.TOWNSFOLK]
                possible_characters.remove(Role.WASHERWOMAN)
                pings = random.sample(possible_pings, 2)
                character_learned = random.choice(possible_characters)
                p.tell(f"From your ability you learn either seat {pings[0].seat} or seat {pings[1].seat} is the {character_learned.name}")



#Librarian gets info
def librarian(g):
    for p in g.getplayers():
        if p.role == Role.LIBRARIAN:
            if ReminderToken.DRUNK_IS_THE_DRUNK not in p.tokens and ReminderToken.POISONER_IS_POISONED not in p.tokens:
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
            else:
                if random.random() < 0.20:
                    p.tell("From your ability you learn there are 0 outsiders in play")
                else:
                    possible_pings = g.getplayers()
                    possible_pings.remove(p)
                    possible_characters = [role for role in Role if role_to_character_type[role] == CharacterType.OUTSIDER]
                    pings = random.sample(possible_pings, 2)
                    character_learned = random.choice(possible_characters)
                    p.tell(f"From your ability you learn either seat {pings[0].seat} or {pings[1].seat} is the {character_learned.name}")


#Investigator gets info
def investigator(g):
    for p in g.getplayers():
        if p.role == Role.INVESTIGATOR:
            if ReminderToken.DRUNK_IS_THE_DRUNK not in p.tokens and ReminderToken.POISONER_IS_POISONED not in p.tokens:
                recluse_in_play = False
                for q in g.getplayers():
                    if q.role == Role.RECLUSE:
                        recluse_in_play = True
                if recluse_in_play and random.random() < 0.4:
                    for pl in g.getplayers():
                        if pl.role == Role.RECLUSE:
                            possible_roles = [role for role in Role if role_to_character_type[role] == CharacterType.MINION]
                            character_learned = random.choice(possible_roles)
                            possible_pings = g.getplayers()
                            possible_pings.remove(p)
                            possible_pings.remove(pl)
                            other_ping = random.choice(possible_pings)
                            pings = [pl, other_ping]
                            random.shuffle(pings)
                            p.tell(f"From your ability you learn either seat {pings[0].seat} or seat {pings[1].seat} is the {character_learned.name}.")

                else:
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
            else:
                possible_pings = g.getplayers()
                possible_pings.remove(p)
                possible_characters = [role for role in Role if role_to_character_type[role] == CharacterType.MINION]
                pings = random.sample(possible_pings, 2)
                random.shuffle(pings)
                character_learned = random.choice(possible_characters)
                p.tell(f"From your ability, you learn either seat {pings[0].seat} or seat {pings[1].seat} is the {character_learned.name}")


#Chef gets info
def chef(g):
    player_list = g.getplayers()
    evil_pairs = 0
    for i in range(len(player_list)):
        if i != len(player_list) - 1:
            if player_list[i].alignment == Alignment.EVIL and player_list[i+1].alignment == Alignment.EVIL:
                evil_pairs += 1
            elif player_list[i].alignment == Alignment.EVIL and player_list[i+1].role == Role.RECLUSE:
                if random.random() < 0.5:
                    evil_pairs += 1
            elif player_list[i].role == Role.RECLUSE and player_list[i+1].alignment == Alignment.EVIL:
                if random.random() < 0.5:
                    evil_pairs += 1
        else:
            if player_list[i].alignment == Alignment.EVIL and player_list[0].alignment == Alignment.EVIL:
                evil_pairs += 1
            elif player_list[i].alignment == Alignment.EVIL and player_list[0].role == Role.RECLUSE:
                if random.random() < 0.5:
                    evil_pairs += 1
            elif player_list[i].role == Role.RECLUSE and player_list[0].alignment == Alignment.EVIL:
                if random.random() < 0.5:
                    evil_pairs += 1

    for p in g.getplayers():
        if p.role == Role.CHEF:
            if ReminderToken.DRUNK_IS_THE_DRUNK not in p.tokens and ReminderToken.POISONER_IS_POISONED not in p.tokens:
                p.tell("There are " + str(evil_pairs) + "pairs of evil players")
            else:
                if len(g.getplayers()) < 10:
                    max_pairs = 1
                elif len(g.getplayers()) < 13:
                    max_pairs = 2
                else:
                    max_pairs = 3

                pairs = random.randint(0, max_pairs)
                p.tell(f"There are {pairs} pairs of evil players.")



#Empath gets info
def empath(g):
    player_list = g.getplayers()
    for p in player_list:
        if not p.alive:
            player_list.remove(p)

    empath_neighbor_seats = []
    for i in range(len(player_list)):
        if player_list[i].role == Role.EMPATH:
            if i == len(player_list) - 1:
                empath_neighbor_seats.append(player_list[0])
                empath_neighbor_seats.append(player_list[i-1])
            elif i == 0:
                empath_neighbor_seats.append(player_list[i+1])
                empath_neighbor_seats.append(player_list[len(player_list)-1])
            else:
                empath_neighbor_seats.append(player_list[i+1])
                empath_neighbor_seats.append(player_list[i-1])

    evil_empath_neighbors = 0
    for n in empath_neighbor_seats:
        if n.alignment == Alignment.EVIL:
            evil_empath_neighbors += 1
        elif n.role == Role.RECLUSE:
            if random.random() < 0.5:
                evil_empath_neighbors += 1
    
    for p in g.getplayers():
        if p.role == Role.EMPATH:
            if ReminderToken.DRUNK_IS_THE_DRUNK not in p.tokens and ReminderToken.POISONER_IS_POISONED not in p.tokens:
                p.tell(str(evil_empath_neighbors) + " of seats " + str(empath_neighbor_seats[0].seat) + " and " + str(empath_neighbor_seats[1].seat) + " are evil")
            else:
                nums = [0, 1, 2]
                nums.remove(evil_empath_neighbors)
                fake_number = random.choice(nums)
                if random.random() < 0.8:
                    p.tell(f"{fake_number} of seats {empath_neighbor_seats[0].seat} and {empath_neighbor_seats[1].seat} are evil")
                else:
                    p.tell(f"{evil_empath_neighbors} of seats {empath_neighbor_seats[0].seat} and {empath_neighbor_seats[1].seat} are evil")

                

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
                if ReminderToken.DRUNK_IS_THE_DRUNK not in p.tokens and ReminderToken.POISONER_IS_POISONED not in p.tokens:
                    p.tell("One of seat" + str(ft_choices[0].seat) + "or seat" + str(ft_choices[1].seat) + "is the demon.")
                else:
                    # 80% chance to get false info if droisoned
                    if random.random() > 0.8:
                        p.tell(f"Neither seat {ft_choices[0].seat} or seat {ft_choices[1].seat} is the demon.")
                    else:
                        p.tell("One of seat" + str(ft_choices[0].seat) + "or seat" + str(ft_choices[1].seat) + "is the demon.")
            else:
                if ReminderToken.DRUNK_IS_THE_DRUNK not in p.tokens and ReminderToken.POISONER_IS_POISONED not in p.tokens:
                    if ft_choices[0].role == Role.RECLUSE or ft_choices[1].role == Role.RECLUSE and random.random() < 0.8:
                        p.tell("One of seat" + str(ft_choices[0].seat) + "or seat" + str(ft_choices[1].seat) + "is the demon.")
                    else:
                        p.tell("Neither seat" + str(ft_choices[0].seat) + "or seat" + str(ft_choices[1].seat) + "is the demon.")
                else:
                    if random.random() < 0.8:
                        p.tell("One of seat" + str(ft_choices[0].seat) + "or seat" + str(ft_choices[1].seat) + "is the demon.")
                    else:
                        p.tell("Neither seat" + str(ft_choices[0].seat) + "or seat" + str(ft_choices[1].seat) + "is the demon.")


def butler(g):
    #Butler gets info
    for p in g.getplayers():
        if p.role == Role.BUTLER:
            choice = p.choose_players_for_ability(g,1)[0]
            while choice.role == Role.BUTLER:
                choice = p.choose_players_for_ability(g, 1)[0]
            choice.tokens.append(ReminderToken.BUTLER_MASTER)
            








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
            if ReminderToken.DRUNK_IS_THE_DRUNK not in p.tokens and ReminderToken.POISONER_IS_POISONED not in p.tokens:
                if choice.role == Role.RECLUSE and random.random() < 0.8:
                    possible_characters = [role for role in Role if role_to_character_type[role] == CharacterType.MINION or role_to_character_type[role] == CharacterType.DEMON]
                    character_learned = random.choice(possible_characters)
                    p.tell(f"Seat {choice_seat} is {character_learned.name}")
                else:
                    p.tell(f"Seat {choice_seat} is {choice_character.name}.")
            else:
                if random.random() < 0.2:
                    p.tell(f"Seat {choice_seat} is {choice_character.name}.")
                else:
                    possible_characters = [role for role in Role]
                    possible_characters.remove(Role.RAVENKEEPER)
                    possible_characters.remove(choice_character)
                    character_learned = random.choice(possible_characters)
                    p.tell(f"Seat {choice_seat} is {character_learned.name}.")
            p.tokens.remove(ReminderToken.RAVENKEEPER_DIED_TONIGHT)




# undertaker goes
def undertaker(g):
    for p in g.getplayers():
        if p.role == Role.UNDERTAKER and p.alive:
            for pl in g.getplayers():
                if ReminderToken.UNDERTAKER_EXECUTED_TODAY in pl.tokens:
                    executed_role = pl.role
                    executed_seat = pl.seat
                    if ReminderToken.DRUNK_IS_THE_DRUNK not in p.tokens and ReminderToken.POISONER_IS_POISONED not in p.tokens:
                        if executed_role == Role.RECLUSE and random.random() < 0.8:
                            possible_characters = [role for role in Role if role_to_character_type[role] == CharacterType.MINION or role_to_character_type[role] == CharacterType.DEMON]
                            character_learned = random.choice(possible_characters)
                            p.tell(f"Seat {executed_seat} is {character_learned.name}")
                        else:
                            p.tell(f"Seat {executed_seat} is {executed_role.name}.")
                    else:
                        if random.random() < 0.2:
                            p.tell(f"Seat {executed_seat} is {executed_role}.")
                        else:
                            possible_characters = [role for role in Role]
                            possible_characters.remove(Role.UNDERTAKER)
                            possible_characters.remove(executed_role)
                            character_learned = random.choice(possible_characters)
                            p.tell(f"Seat {executed_seat} is {character_learned.name}")
                    pl.tokens.remove(ReminderToken.UNDERTAKER_EXECUTED_TODAY)


def slayer(g, slayer, slayed):
    if slayer.role == Role.SLAYER and slayer.alive and ReminderToken.SLAYER_HAS_ABILITY in slayer.tokens:
        slayer.tokens.remove(ReminderToken.SLAYER_HAS_ABILITY)
        if ReminderToken.POISONER_IS_POISONED not in slayer.tokens and ReminderToken.DRUNK_IS_THE_DRUNK not in slayer.tokens:
            if slayed.role == Role.IMP:
                slayed.alive = False
                for p in g.getplayers():
                    p.tell(f"Seat {slayed.seat} dies.")
                    if p.role == Role.SCARLET_WOMAN and p.alive:
                        p.tokens.append(ReminderToken.MINION_IS_THE_DEMON)
                        scarlet_woman(g)
            elif slayed.role == Role.RECLUSE:
                if random.random() < 0.8:
                    slayed.alive = False
                    for p in g.getplayers():
                        p.tell(f"Seat {slayed.seat} dies.")
                
                


def star_pass(g):
    alive_minions = []
    for p in g.getplayers():
        if role_to_character_type[p.role] == CharacterType.MINION and p.alive:
            alive_minions.append(p)
    if alive_minions != []:
        for minion in alive_minions:
            if minion.role == Role.SCARLET_WOMAN:
                minion.role = Role.IMP
                minion.tell("You are the " + Role.IMP.name)
                minion.tell("You are a " + role_to_character_type[Role.IMP].name)
                minion.tell("You are " + character_type_to_alignment[CharacterType.DEMON].name)
                return
        
        minion_to_imp = random.choice(alive_minions)
        minion_to_imp.tell("You are the " + Role.IMP.name)
        minion_to_imp.tell("You are a " + role_to_character_type[Role.IMP].name)
        minion_to_imp.tell("You are " + character_type_to_alignment[CharacterType.DEMON].name)
        
        




start_game(g)









    

g.printgameinfo()