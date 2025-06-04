import pygame
import random
import os
import copy

pygame.init()

card_values = ['2', '3', '4', '5', '6', '7', '8', '9', 'J', 'Q', 'K', 'A']
suits = ["hearts", "diamonds", "clubs", "spades"]
deck = [f"{value}_of_{suit}" for value in card_values for suit in suits]
one_deck= 4 * deck
deck_no = 1
game_deck=copy.deepcopy(one_deck * deck_no)
active= False
record = [0, 0, 0]
initial_deal= False
revealed= False
hand_active = False
add_game=False
my_hand=[]
dealers_hand=[]
player_score = 0
dealer_score = 0
outcome=0
results = ["", "GAME DRAW!", "DEALER HAS A BLACKJACK!", "THAT'S A BLACKJACK!",
           "OH SHOOT! IT'S A BUST!", "DEALER WENT OVER!", "YOU BEAT THE DEALER!",
           "LOST TO THE DEALER!"]


WIDTH, HEIGHT = 600,760
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack")
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)


# Load card images
card_folder = "cards/"  # Set this to the folder where your card images are stored

def load_card_image(card_name):
    """Loads card image from folder"""
    return pygame.image.load(os.path.join(card_folder, f"{card_name}.png"))

def deal_cards(hand, our_deck):
    card = random.randint(0, len(our_deck))
    hand.append(our_deck[card-1])
    our_deck.pop(card-1)
    return hand, our_deck

def draw_cards(reveal):
    """Draws player and dealer cards on screen"""
    global my_hand, dealers_hand

    # Draw dealer's cards
    for a, card in enumerate(dealers_hand):
        if a!=0 or reveal:
            card_img = load_card_image(card)
            screen.blit(pygame.transform.scale(card_img, (125, 180)), (50 + a * 100, 100 + (a * 15)))
        else:
            pic = pygame.image.load(os.path.join(card_folder, "card_back.png"))
            screen.blit(pygame.transform.scale(pic, (125, 180)), (50 + a * 100, 100 + (a * 15)))

    # Draw player's cards
    for a, card in enumerate(my_hand):
        card_img = load_card_image(card)
        screen.blit(pygame.transform.scale(card_img, (125, 180)), (50 + a * 100, 400 + (a*15)))

def calculate_score(hand):
    """Calculate hand score fresh each turn and check for aces"""
    hand_score = 0
    values = [card.split("_")[0] for card in hand]
    ace_count = values.count("A")
    for x in range(len(values)):
        for j in range(8):
            if values[x] == card_values[j]:
                hand_score += int(values[x])
        if values[x] in ['10', 'J', 'Q', 'K']:
            hand_score += 10
        elif values[x] == "A":
            hand_score += 11
    if hand_score > 21 and ace_count > 0:
        for x in range(ace_count):
            if hand_score > 21:
                hand_score -= 10
    return hand_score

def draw_game(act, result):
    """Draws the game buttons and conditions"""
    button_list =[]
    #when game not active only option is to deal a new hand
    if not act:
        deal = pygame.draw.rect(screen, "white", [150, 30, 300, 80], 0, 5)
        pygame.draw.rect(screen,"green", [150, 30, 300, 80], 3, 5)
        deal_text = font.render("DEAL HAND", True, "black")
        screen.blit(deal_text, (195, 50))
        button_list.append(deal)
    # once game is active display the hit and stand buttons
    else:
        hit = pygame.draw.rect(screen, "white", [50, 630, 220, 60], 0, 5)
        pygame.draw.rect(screen, "green", [50, 630, 220, 60], 3, 5)
        hit_text = font.render("HIT ME", True, "black")
        screen.blit(hit_text, (100, 645))
        button_list.append(hit)
        stand = pygame.draw.rect(screen, "white", [340, 630, 220, 60], 0, 5)
        pygame.draw.rect(screen, "green", [340, 630, 220, 60], 3, 5)
        stand_text = font.render("STAND", True, "black")
        screen.blit(stand_text, (400, 645))
        button_list.append(stand)
        score_text = font.render(f"Wins:{record[0]}   Losses:{record[1]}   Draws:{record[2]}", True, "black")
        screen.blit(score_text, (90, 710))
    if result != 0:
        screen.blit(font.render(results[result], True, "white"), (120,25))
        deal = pygame.draw.rect(screen, "white", [160, 320, 270, 70], 0, 5)
        pygame.draw.rect(screen, "black", [160, 320, 270, 70], 3, 5)
        deal_text = font.render("DEAL AGAIN", True, "black")
        screen.blit(deal_text, (190, 335))
        button_list.append(deal)
    return button_list

def display_cards(player, dealer):
    screen.blit(font.render(f"Score:{player}", True, "white"), (420,550))
    if revealed:
        screen.blit(font.render(f"Score:{dealer}", True, "white"), (420, 250))

def check_win(hand_act, player, dealer, result, records, add):
    """Compares the score between the user and dealer"""
    global  my_hand, dealers_hand
    if not hand_act and dealer>= 17:
        if player == dealer:
            result= 1
        elif dealer == 21 and len(dealers_hand) == 2:
            result= 2
        elif player == 21 and len(my_hand) == 2:
            result=3
        elif player > 21:
            result=4
        elif dealer > 21:
            result = 5
        elif player > dealer :
            result = 6
        else:
            result = 7
        if add:
            if result==1:
                records[2]+=1
            elif result==2 or result==4 or result==7:
                records[1]+=1
            elif result==3 or result==5 or result==6:
                records[0]+=1
            add=False
    return  result,records, add


run = True
while run:
    timer.tick(fps)
    screen.fill((0, 128, 0))
    buttons = draw_game(active, outcome)
    #initial card deal to the player and dealer
    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards (my_hand, game_deck)
            dealers_hand, game_deck = deal_cards(dealers_hand, game_deck)
        initial_deal = False
    if active:
        draw_cards(revealed)
        player_score = calculate_score(my_hand)
        if revealed:
            dealer_score =  calculate_score(dealers_hand)
            if dealer_score < 17:
                dealers_hand, game_deck = deal_cards(dealers_hand, game_deck)
        display_cards(player_score, dealer_score)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if not active:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    initial_deal =  True
                    game_deck = copy.deepcopy(one_deck * deck_no)
                    my_hand = []
                    dealers_hand = []
                    outcome=0
                    hand_active = True
                    add_game=True
                    player_score=0
                    dealer_score=0

            else:
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                    my_hand, game_deck = deal_cards(my_hand, game_deck)
                elif buttons[1].collidepoint(event.pos) and not revealed:
                    hand_active=False
                    revealed=True
                elif len(buttons) == 3:
                    if buttons[2].collidepoint(event.pos):
                        revealed= False
                        active = True
                        initial_deal = True
                        game_deck = copy.deepcopy(one_deck * deck_no)
                        my_hand = []
                        dealers_hand = []
                        outcome = 0
                        hand_active = True
                        add_game = True
                        player_score = 0
                        dealer_score = 0

    if hand_active and player_score >= 21:
        hand_active = False
        revealed = True
    outcome, record, add_game = check_win(hand_active, player_score, dealer_score, outcome, record, add_game)


    pygame.display.flip()
pygame.quit()
