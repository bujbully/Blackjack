import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)

# Load card images
card_folder = "cards/"  # Set this to the folder where your card images are stored

def load_card_image(card_name):
    """Loads card image from folder"""
    return pygame.image.load(os.path.join(card_folder, f"{card_name}.png"))

# Deck of cards (formatted for image file names)
card_values = [ 2, 3, 4, 5, 6, 7, 8, 9, 10]
suits = ["hearts", "diamonds", "clubs", "spades"]
deck = [f"{value}_of_{suit}" for value in card_values for suit in suits]
game_deck= 4* deck

# Player and Dealer Hands
player_hand = []
dealer_hand = []
player_score = 0
dealer_score = 0
game_over = False
message = ""
tally = 0
player_wins = 0
dealer_wins = 0

# Button Class
class Button:
    def __init__(self, text, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, BLACK, self.rect, border_radius=5)
        label = font.render(self.text, True, WHITE)
        screen.blit(label, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Buttons
hit_button = Button("Hit", 100, 500, 100, 50)
stand_button = Button("Stand", 250, 500, 100, 50)
restart_button = Button("Restart", 400, 500, 100, 50)

def calculate_score(hand):
    """Calculates the score based on current hand"""
    values = [card.split("_")[0] for card in hand]
    score = sum(card_values[int(v)-1] for v in values)

    # Handling Ace (if score goes above 21)
    if "1" in values and score > 21:
        score -= 10

    return score

def check_winner():
    """Determines game winner"""
    global game_over, message, tally, player_wins, dealer_wins
    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)

    if dealer_score == 21 and len(dealer_hand) == 2:
        message = "Dealer has Blackjack! HOUSE WINS!"
        game_over = True
        dealer_wins += 1
    elif player_score == 21 and len(player_hand) == 2:
        message = "BLACKJACK! YOU WIN!"
        game_over = True
        player_wins += 1
    elif player_score > 21:
        message = "BUST! HOUSE WINS!"
        game_over = True
        dealer_wins += 1
    elif dealer_score > 21:
        message = "House busts! YOU WIN!"
        game_over = True
        player_wins += 1
    elif not game_over and dealer_score >= 17:
        if player_score > dealer_score:
            message = "YOU WIN!"
            player_wins += 1
        else:
            message = "HOUSE WINS!"
            dealer_wins += 1
        game_over = True

    if game_over:
        tally += 1

    # Display scores & messages
    player_text = font.render(f"Player Score: {calculate_score(player_hand)}", True, BLACK)
    dealer_text = font.render(f"Dealer Score: {calculate_score(dealer_hand)}", True, BLACK)
    game_text = font.render(message, True, WHITE)
    tally_text = font.render(f"Games Played: {tally}, Player Wins: {player_wins}, Dealer Wins: {dealer_wins}", True, WHITE)

    screen.blit(player_text, (50, 450))
    screen.blit(dealer_text, (50, 20))
    screen.blit(game_text, (WIDTH // 2 - 100, HEIGHT // 2))
    screen.blit(tally_text, (50, 550))

def deal_card(hand):
    """Deals a random card and adds it to the given hand"""
    card = random.choice(game_deck)
    hand.append(card)

def draw_cards():
    """Draws player and dealer cards on screen"""
    screen.fill(GREEN)

    # Draw dealer's cards
    for i, card in enumerate(dealer_hand):
        card_img = load_card_image(card)
        screen.blit(pygame.transform.scale(card_img, (125, 180)), (50 + i * 100, 30))

    # Draw player's cards
    for i, card in enumerate(player_hand):
        card_img = load_card_image(card)
        screen.blit(pygame.transform.scale(card_img, (125, 180)), (50 + i * 100, 300))

    # Draw buttons
    hit_button.draw()
    stand_button.draw()
    restart_button.draw()

def game_loop():
    """Main game loop handling events"""
    global game_over, player_hand, dealer_hand, message

    running = True

    # Start by dealing two cards to player and dealer
    player_hand.clear()
    dealer_hand.clear()
    for _ in range(2):
        deal_card(player_hand)
        deal_card(dealer_hand)

    while running:
        draw_cards()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not game_over:
                    if hit_button.is_clicked(pos):
                        deal_card(player_hand)
                        check_winner()
                    elif stand_button.is_clicked(pos):
                        while calculate_score(dealer_hand) < 17:
                            deal_card(dealer_hand)
                        check_winner()
                if restart_button.is_clicked(pos):
                    game_over = False
                    message = ""
                    player_hand.clear()
                    dealer_hand.clear()
                    for _ in range(2):
                        deal_card(player_hand)
                        deal_card(dealer_hand)
    pygame.quit()

# Run the game
game_loop()