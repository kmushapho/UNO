import random
import tkinter as tk
from functions import *
import time

# create the deck of cards
cards = build_deck()

# shuffle the cards
shuffled_cards = get_shuffled_deck(cards)

# setting up main game window
window = tk.Tk()
window.title("UNO")

# setting up the size of the window
canvas = tk.Canvas(window, width=1200, height=900, bg='black')
canvas.pack()

# print(cards)
# deal cards to the players
shuffled_cards, players_dict = deal_shuffled_cards(shuffled_cards, players_dict)

turn_idx = 0
action_played = False
card_changed = False
len_pile_after_action = len(discard_pile)
resume_program = False
hand_before_play = len(players_dict['Human'])

# check if first card picked is not a wild card
discard_pile, shuffled_cards, human_played = first_card_not_wild(shuffled_cards)


while True:
    current_player = players_names[turn_idx]
    draw_pile_image_path = f'cards/back.png'
    draw_pile_img = str_to_image(draw_pile_image_path)
    draw_pile_img_ref = ImageTk.PhotoImage(draw_pile_img)
    draw_pile_id = canvas.create_image(250, 450, image = draw_pile_img_ref)
    
     # add cards to player hand when you click on the draw pile
    canvas.tag_bind(draw_pile_id, '<Button-1>', lambda event: click_on_draw_pile(event,players_dict, shuffled_cards, draw_pile_id, canvas, human_hand, last_card_discarded))
            
    # create and show discard pile
    last_card_discarded = discard_pile[-1]
    card_color, card_action = get_card_color_and_action(last_card_discarded)
    if card_action != None:
        last_card_discarded_path = f'cards/{card_color} {card_action}.png'
    else:
        last_card_discarded_path = f'cards/{card_color}.png'
    last_card_discarded_img = str_to_image(last_card_discarded_path)
    last_card_discarded_img_ref = ImageTk.PhotoImage(last_card_discarded_img)
    canvas.create_image(900, 450, image = last_card_discarded_img_ref)

    # computer cards will be displayed at the top of the screen
    computer_hand, computer_hand_images, computer_offset_x, computer_offset_y = computer_hand_and_offsets()
    display_hand(canvas, computer_hand_images, computer_offset_x, computer_offset_y, True, 'computer_hand_tag', computer_hand, '')

    # human cards will be displayed at the bottom of the screen
    human_hand, human_hand_images, human_offset_x, human_offset_y = human_hand_and_offsets()
    card_id_list = display_hand(canvas, human_hand_images, human_offset_x, human_offset_y, False, 'human_hand_tag', human_hand, last_card_discarded)
    print(human_hand)

    if len(players_dict['Computer']) == 0:
        pop_ip_winner(True)
        break
    elif len(players_dict['Human']) == 0:
        pop_ip_winner(False)
        break


    if len(last_card_discarded.split()) == 1 and 'draw4' in discard_pile[-2] and not action_played:
        last_card_discarded = 'draw4'
        action_played = True
        resume_program = True
    
    if ('reverse' in last_card_discarded or 'skip' in last_card_discarded or 'draw2' in last_card_discarded or 'draw4' in last_card_discarded) and not action_played:
        len_pile_after_action = len(discard_pile)

        if 'reverse' in last_card_discarded or 'skip' in last_card_discarded:
            turn_idx = (turn_idx + 2) % 2

        elif 'draw2' in last_card_discarded:
            add_card_to_hand(players_dict, shuffled_cards, 2, current_player)
        
        elif 'draw4' in last_card_discarded:
            add_card_to_hand(players_dict, shuffled_cards, 4, current_player)
        
        action_played = True
        resume_program = True

        display_hand(canvas, computer_hand_images, computer_offset_x, computer_offset_y, True, 'computer_hand_tag', computer_hand, '')
        display_hand(canvas, human_hand_images, human_offset_x, human_offset_y, False, 'human_hand_tag', human_hand, last_card_discarded)


    else:
        time.sleep(1)
        action_played = False
        if 'Computer' in current_player and human_played:
            computer_play(computer_hand,current_player, players_dict, last_card_discarded, shuffled_cards, canvas)
            human_played = False
            card_picked = False
            resume_program = True
            display_hand(canvas, computer_hand_images, computer_offset_x, computer_offset_y, True, 'computer_hand_tag', computer_hand, '')

        
        elif 'Human' in current_player:
            if len(players_dict['Human']) > hand_before_play:
                resume_program = True
                human_played = True
            
            else:
                for idx, card_id in enumerate(card_id_list):
                    card = human_hand[idx]
                    canvas.tag_bind(card_id, '<Button-1>', lambda event, card = card : card_clicked_is_playable(event, card, last_card_discarded, human_hand, players_dict, canvas, human_offset_x, human_offset_y,))

                    if hand_before_play > len(human_hand):
                        resume_program = True
                        human_played = True
                    

    
    if resume_program:
        hand_before_play = len(players_dict['Human'])
        if turn_idx < 1:
            turn_idx += 1
        else:
            turn_idx =0
        resume_program = False


window.mainloop()