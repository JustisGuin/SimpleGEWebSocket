import pygame
import asyncio
import websockets
import threading
from queue import Queue

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FONT_SIZE = 30

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WebSocket Chat")

# Set up font
font = pygame.font.Font(None, FONT_SIZE)

# Message storage
messages = []
username = ""
message_queue = Queue()  # Queue for messages to be sent

# WebSocket client
async def send_message(websocket):
    while True:
        message = await asyncio.get_event_loop().run_in_executor(None, message_queue.get)
        await websocket.send(message)

async def websocket_client(username):
    print(f"{username} is trying to connect...")
    async with websockets.connect("ws://localhost:8001") as websocket:

        print(f"{username} connected to the server.")

        #Send the username 
        await websocket.send(f"username|{username}")

        # Start the send_message task
        asyncio.create_task(send_message(websocket))
        while True:
            message = await websocket.recv()
            print(f"Received message: {message}")  # Log received message
            messages.append(message)

# Start the WebSocket client in a separate thread
def start_websocket_client(username):
    asyncio.run(websocket_client(username))

# Main loop
running = True
input_box = pygame.Rect(50, HEIGHT // 2 - 20, WIDTH - 100, 40)  # Initial position for username input
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
text = ''
input_state = 'username'  # State to track if we are in username input or chat

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    if input_state == 'username':
                        username = text.strip()  # Get the username
                        if username:  # Ensure username is not empty
                            # Start the WebSocket client thread
                            threading.Thread(target=start_websocket_client, args=(username,), daemon=True).start()
                            input_state = 'chat'  # Switch to chat state
                            text = ''  # Clear the input box
                            # Move the input box to the bottom of the screen
                            input_box.y = HEIGHT - 50  # Set the input box position to the bottom
                    elif input_state == 'chat':
                        # Send message to the server
                        if text:
                            full_message = f"{username}|{text}"  # Use '|' instead of ':'
                            message_queue.put(full_message)  # Put the message in the queue
                            messages.append(full_message)  # Display the sent message
                            print(f"Sent message: {full_message}")  # Log sent message
                            text = ''  # Clear the input box after sending
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]  # Remove the last character
                else:
                    text += event.unicode  # Add the typed character to the text
    # Fill the screen with white
    screen.fill((255, 255, 255))

    if input_state == 'username':
        # Render username input screen
        title_surface = font.render("Enter your username:", True, (0, 0, 0))
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, HEIGHT // 2 - 100))
    else:
        # Render chat messages
        for i, message in enumerate(messages[-10:]):  # Show last 10 messages
            text_surface = font.render(message, True, (0, 0, 0))
            screen.blit(text_surface, (50, 50 + i * FONT_SIZE))

    # Render input box
    pygame.draw.rect(screen, color, input_box, 2)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

    pygame.display.flip()  # Update the display

pygame.quit()  # Quit Pygame when the loop ends