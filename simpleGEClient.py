import asyncio
import websocket
from simpleGE import Scene
import pygame, sys


class WebSocketClient(Scene):
    def __init__(self, size=(640, 480)):
        super().__init__(size)
        self.connected = False
        self.websocket = None
        self.messages = []


        #GUI/ UI elements 
        self.font = pygame.font.Font(None, 36)
        self.inputBox = pygame.Rect(50, 300, 540, 40)
        self.inputText = '...'
        self.active = False

    async def connect(self):
        url = 'ws://localhost:5000'
        self.websocket = await websocket.connect(url)
        self.connected = True
        if (self.connected == True):
            print("Connected to server")
        else:
            print("Failed connection please try again")
        
        #Reciving messages 
        asyncio.create_task(self.receiveMessages())

    async def receiveMessages(self):
        while self.connected:
            try: 
                message = await self.websocket.recv()
                self.messages.append(f"Recieved: {message}")
            except Exception as e:
                print(f"Error occured: {e}")
                self.connected = False

        
    def handleInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.connected = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        asyncio.run(self.sendMessage(self.inputText))
                        self.inputText = ''
                    elif event.key == pygame.K_BACKSPACE:
                        self.inputText = self.inputText[:-1]
                    else:
                        self.inputText += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.inputBox.collidepoint(event.pos):
                    self.active = not self.active
                else:
                    self.active = False
