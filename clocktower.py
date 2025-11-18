import random
from enum import Enum

class Game:
    def __init__(self,players,num_days,game_phase,bluffs):
        self.players = players
        self.num_days = num_days
        self.game_phase = game_phase
        self.bluffs = bluffs

    def demon(self):
        return self.players[CharacterType.DEMON][0]
    
    def printgameinfo(self):
        for role in self.players:
            for p in self.players[role]:
                print(p.role,p.alignment,p.alive,p.canvote,p.badinfo,p.seat,p.tokens,p.history)

    def getplayers(self):
        all_players = []
        for type in self.players:
            for p in self.players[type]: all_players.append(p)
        print(all_players)
        return all_players


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
    
    def tell(self,msg):
        self.history.append(msg)

    def choose_players_for_ability(self,g,num):
        choices = random.sample(g.getplayers(),num)
        for choice in choices:
            self.tell("I chose Seat "+str(choice.seat)+" for my ability")
        return choices

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

#Assign roles
for type in num_players_to_num_roles[num_players]:
    roles_of_this_type = []
    for role in Role:
        if role_to_character_type[role] == type: roles_of_this_type.append(role)
    random_roles = random.sample(roles_of_this_type,num_players_to_num_roles[num_players][type])
    for role in random_roles:
        players[role_to_character_type[role]].append(Player(role,character_type_to_alignment[role_to_character_type[role]],True,True,False,seats[seat],[],[]))
        seat = seat + 1

#Generate random bluffs
all_roles = []
for role in Role:
    if role_to_character_type[role]==(CharacterType.TOWNSFOLK or CharacterType.OUTSIDER): all_roles.append(role)
for type in players:
    for p in players[type]:
        if p.role in all_roles: all_roles.remove(p.role)
bluffs = random.sample(all_roles,3)



g = Game(players,0,GamePhase.NIGHT,bluffs)

#Players need to know what their role is
for type in g.players:
    for p in g.players[type]:
        p.tell("You are the "+p.role.name)
        p.tell("You are a "+role_to_character_type[p.role].name)
        p.tell("You are a "+character_type_to_alignment[role_to_character_type[p.role]].name)

#Do first night

#The Drunk
#TODO: MAKE THIS WORK

#Minion info
for p in g.players[CharacterType.MINION]:
    p.tell("Seat "+str(g.demon().seat)+" is the Demon")

#Demon info
for p in g.players[CharacterType.DEMON]:
    for q in g.players[CharacterType.MINION]:
        p.tell("Seat "+str(q.seat)+" is a Minion")
    for bluff in g.bluffs:
        p.tell(bluff.name+" is not in play")
    
#Poisoner poisons someone
for p in g.getplayers():
    if p.role == Role.POISONER:
        choice = p.choose_players_for_ability(g,1)
        choice[0].tokens.append(ReminderToken.POISONER_IS_POISONED)


g.printgameinfo()