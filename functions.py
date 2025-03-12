from PIL import Image, ImageTk
import os
import random
import tkinter as tk

colors = ['red', 'green', 'blue', 'yellow']
actions = ['reverse', 'draw2', 'skip']
numbers = list(range(10)) + list(range(1,10))
wild = ['wild card', 'wild draw4']
players_dict = {"Human" : [], 'Computer' : []}
players_names = list(players_dict.keys())
discard_pile = []
card_picked = False



def build_deck():
    """_build a deck of cards for the game_

    Returns:
        _list_: _list of all the uno cards_
    """

    deck = []
    for color in colors:
        for num in numbers:
            deck.append(f'{color} {num}')

        for action in actions:
            for i in range(2):
                deck.append(f'{color} {action}')

        for wild_card in wild:
            deck.append(f'{wild_card}')

    return deck


def get_shuffled_deck(deck:list):
    """_shuffle the deck of cards_

    Args:
        deck (_list_): _list of uno cards as strings_

    Returns:
        _list_: _randomly shuffled deck of cards_
    """

    return random.choices(deck, k=len(deck))


def get_card_color_and_action(card:str):
    """_get the card color and the action of the card_

    Args:
        card (str): _uno card_

    Returns:
        card_color (_str_): _card color_
        card_action (_str_): _card action_
    """
    if card != None:
        card = card.split()
        if len(card) == 1:
            card_color, card_action = card[0], None
        else:
            card_color, card_action = card[0], card[-1]
        return card_color, card_action


def player_hand_images(player_hand:list, is_computer:bool):
    """_creates list of images that corresponds to the shuffled deck_

    Args:
        player_hand (list): _players hand as strings_
        is_computer (bool): _checks if the player is computer or human_

    Returns:
        images_hand (_list_): _list of images of the player's hand_
    """
    images_hand = []
    if not is_computer:
        for card in player_hand:
            card_color, card_action = get_card_color_and_action(card)
            image_path = f'cards/{card_color} {card_action}.png'
            img = str_to_image(image_path)
            images_hand.append(ImageTk.PhotoImage(img))

    else:
        for card in player_hand:
            card_color, card_action = get_card_color_and_action(card)
            image_path = f'cards/back.png'
            img = str_to_image(image_path)
            images_hand.append(ImageTk.PhotoImage(img))

    return images_hand


def str_to_image(image_path):
    """_takes the image path and returns the photho_

    Args:
        image_path (_str_): _the path of the photho_

    Returns:
        _img_: _the photo corresponding to the path_
    """
    if os.path.exists(image_path):
        img = Image.open(image_path)
        img = img.resize((100, 150))

        return img


def deal_shuffled_cards(shuffled_deck:list, players_dict:dict):
    """_takes in the shuffled deck and gives players thier first hands_

    Args:
        shuffled_deck (list): _deck of shuffled cards_
        players_dict (dict): _a dictionary of players names and their hands_
        players_names (list): _a list of all the players names_
        images_deck (list): _a list of the uno cards images
    
    Returns:
        shuffled_deck (_list_): _list of the remaining shuffled cards after dealing_
        players_dict (_dict_): _list of the players names as keys and their hands as values_
        images_deck (_list_): _list of the remaining shuffled cards images after dealing_
    """
    players_names = list(players_dict.keys())
    for player in players_names:
        hand = []
        for i in range(7):
            hand.append(shuffled_deck[0])
            shuffled_deck.pop(0)
        players_dict[player] = hand

    return shuffled_deck, players_dict


def add_card_to_hand(players_dict:dict, shuffled_deck:list, no_cards_to_draw, player_name):
    """_adds a card to the player hand each time they draw from the draw pile_

    Args:
        players_dict (dict): _disctionary of the player's hands_
        shuffled_deck (list): _cards shuffled_

    Returns:
        shuffled_deck (_list_): _remaining shuffled cards_
        players_dict (_dict_): _players names and hands in a dictionary_
    """
    if no_cards_to_draw > len(shuffled_deck):
        cards = [i for i in discard_pile[-1] if len(i.split() > 1)]
        shuffled_deck = get_shuffled_deck(cards)
    
    player_hand = players_dict[player_name]
    for i in range(no_cards_to_draw):
        card = shuffled_deck[0]
        player_hand.append(card)
        shuffled_deck.pop(0)
    players_dict[player_name] = player_hand

    return shuffled_deck

def display_hand(canvas, hand_images, x_offset:int, y_offset:int, is_computer:bool, tag_name:str, player_hand:list, last_card_discarded):
    """_displays the player's hands 7 cards per row_

    Args:
        canvas (_type_): _description_
        hand_images (_img_): _images of the player's hand_
        x_offset (_int_): _x cordinate of where the cards will start_
        y_offset (_int_): _y cordinate of where the cards will start_
        is_computer (bool): _if the player is a computer or not_
    """
    max_cards_per_row = 7  
    row_cards = 0  
    card_id_list = []

    for idx, card_image in enumerate(hand_images):
        
        if row_cards >= max_cards_per_row:
            row_cards = 0 

            if not is_computer:
                y_offset += 50
            else:
                y_offset -= 50

        card_id = canvas.create_image(x_offset + (idx % max_cards_per_row) * 120, y_offset, image=card_image, tag = tag_name)
        card_id_list.append(card_id)
        row_cards += 1  
    
    canvas.update()
    return card_id_list


def click_on_draw_pile(event, players_dict:dict, shuffled_cards:list, draw_pile_id, canvas, player_hand, last_card_discarded):
    """_adds a card to the player's hand each time they click on the draw pile_

    Args:
        event (_type_): _description_
        players_dict (_dict_): _description_
        shuffled_cards (_list_): _description_

    Returns:
        _type_: _description_
    """
    
    x1, y1, x2, y2 = canvas.bbox(draw_pile_id)
    if x1 <= event.x <= x2 and y1 <= event.y <= y2:
        players_dict, shuffled_cards = add_card_to_hand(players_dict, shuffled_cards, 1, 'Human')

    human_hand, human_hand_images, human_offset_x, human_offset_y = human_hand_and_offsets()
    display_hand(canvas, human_hand_images, human_offset_x, human_offset_y, False, 'human_hand_tag', player_hand, last_card_discarded)

    return players_dict, shuffled_cards


# check if first card placed down is a wild card
def first_card_not_wild(shuffled_cards):
    first_card = shuffled_cards[0]
    human_played = False
    while True:
        if  'wild' in first_card:
            shuffled_cards = get_shuffled_deck(shuffled_cards)
            first_card = shuffled_cards[0]
        else:
            discard_pile.append(first_card)
            shuffled_cards.pop(0)
            break
    if 'reverse' in first_card or 'skip' in first_card:
        human_played = True
    
    return discard_pile, shuffled_cards, human_played


def is_card_valid(last_card_discarded, player_card):
    last_card_discarded_color, last_card_discarded_action = get_card_color_and_action(last_card_discarded)
    card_color, card_action = get_card_color_and_action(player_card)
    
    if 'wild' in player_card:
        return True
    
    elif last_card_discarded_color == card_color:
        return True
    
    elif last_card_discarded_action != None and card_action != None:
        if card_action.isdigit() and last_card_discarded_action.isdigit():
            if int(card_action) == int(last_card_discarded_action):
                return True
    
    elif card_action == last_card_discarded_action:
        return True
    
    return False


def card_clicked_is_playable(event, card, last_card_discarded, player_hand, players_dict, canvas, human_offset_x, human_offset_y):
    if is_card_valid(last_card_discarded, card): 
        print(card)
        card_idx = player_hand.index(card) 
        player_hand.pop(card_idx)
        players_dict['Human'] = player_hand
        human_hand_images = player_hand_images(player_hand, False)
        display_hand(canvas, human_hand_images, human_offset_x, human_offset_y, False, 'human_hand_tag', player_hand, last_card_discarded)
        discard_pile.append(card)
            

def pop_ip_winner(is_computer):
    popup = tk.Toplevel()
    popup.title("WINNER!!!!!")

    # size of popup
    popup.geometry('600x600')

    # label inside of popup
    if is_computer:
        label = tk.Label(popup, text= f'COMPUTER WON!!!!')
        label.pack(padx=20)

    else:
        label = tk.Label(popup, text= f'YOU WON!!!!')
        label.pack(padx=20)
    
    # button to close popup
    close_button = tk.Button(popup, text='Close', command=popup.destroy)
    close_button.pack()


def get_playable_cards(player_hand, last_card_discarded):
    playable_cards = []
    for card in player_hand:
        if is_card_valid(last_card_discarded, card):
            playable_cards.append(card)

    return playable_cards



def computer_play(computer_hand, player_name, players_dict, last_card_discarded, shuffled_deck, canvas, tag = 'computer_hand_tag'):
    playable_cards = get_playable_cards(computer_hand, last_card_discarded)
    if len(playable_cards) == 0:
        add_card_to_hand(players_dict, shuffled_deck, 1, player_name)
        

    else:
        
        card = random.choice(playable_cards)
        new_color = ''
        card_idx = computer_hand.index(card)
        computer_hand.pop(card_idx)
        if 'wild' in card:
            new_color = pick_new_color(computer_hand, True)
            discard_pile.extend([card, new_color])
        else:
            discard_pile.append(card)

        players_dict[player_name] = computer_hand
        computer_hand, computer_hand_images, computer_offset_x, computer_offset_y = computer_hand_and_offsets()
        display_hand(canvas, computer_hand_images, computer_offset_x, computer_offset_y, False, tag, computer_hand, '')



def human_hand_and_offsets():
    human_hand = players_dict['Human']
    human_hand_images = player_hand_images(human_hand, False)
    human_offset_x = 200
    human_offset_y = 700
    return human_hand, human_hand_images, human_offset_x, human_offset_y

def computer_hand_and_offsets():
    computer_hand = players_dict['Computer']
    computer_hand_images = player_hand_images(computer_hand, False)
    computer_offset_x = 200
    computer_offset_y = 100
    return computer_hand, computer_hand_images, computer_offset_x, computer_offset_y



def pick_new_color(players_hand, is_computer):
    if is_computer:
        hand_colors = []
        for card in players_hand:
            card_color, card_action = get_card_color_and_action(card)
            if card_color in colors:
                hand_colors.append(card_color)

        hand_colors = list(set(hand_colors))
        if len(hand_colors) > 0:
            new_color = random.choice(hand_colors)
        else:
            new_color = random.choice(colors)

    else:
        pass


    return new_color

def wild_card_popup(card, player_name, new_color):
    popup = tk.Tk()
    popup.title(f'{player_name} put down {card}')

    if 'draw4' in card:
        if 'Computer' in player_name:
            label = tk.Label(popup, text=f'You picked up 4 cards \nGame color changed to {new_color}')
            label.pack(padx=20, pady=20)
        else:
            label = tk.Label(popup, text=f'Computer picked up 4 cards \nGame color changed to {new_color}')
            label.pack(padx=20, pady=20)
    else:
        label = tk.Label(popup, text=f'You picked up 4 cards \nGame color changed to {new_color}')
        label.pack(padx=20, pady=20)

def is_action_done(len_pile_after_action, discard_pile):
    if len_pile_after_action == len(discard_pile):
        return True
    return False
