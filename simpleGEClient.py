import asyncio
import websockets  # Use the correct websockets library
import simpleGE

class WebSocketClient(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.connected = False
        self.websocket = None
        self.messages = []

        # GUI/UI elements
        self.lblOut = simpleGE.Label()
        self.lblOut.center = (320, 50)
        self.lblOut.size = (300, 30)
        self.lblOut.text = "WebSocket Client 1:"

        self.txtInput = simpleGE.TxtInput()
        self.txtInput.center = (320, 80)
        self.txtInput.text = ""

        self.btnSend = simpleGE.Button()
        self.btnSend.center = (320, 120)
        self.btnSend.text = "Send"

        self.lblOut2 = simpleGE.Label()
        self.lblOut2.center = (320, 170)
        self.lblOut2.text = "WebSocket Client 2:"


        self.sprites = [self.lblOut2,self.lblOut, self.txtInput, self.btnSend]

    async def connect(self):
        url = 'ws://localhost:5000'
        self.websocket = await websockets.connect(url)  # Use websockets.connect
        self.connected = True
        print("Connected to server")
        
        # Receiving messages 
        asyncio.create_task(self.receiveMessages())

    async def receiveMessages(self):
        while self.connected:
            try: 
                message = await self.websocket.recv()
                self.messages.append(f"Received: {message}")
            except Exception as e:
                print(f"Error occurred: {e}")
                self.connected = False

    def processEvent(self, event):
        self.txtInput.readKeys(event)  # Handle text input

    def process(self):
        if self.btnSend.clicked:
            message = self.txtInput.text
            if message:
                asyncio.run(self.sendMessage(message))
                self.txtInput.text = ""  # Clear input after sending

        # Update label to show received messages
        if self.messages:
            self.lblOut.text = "\n".join(self.messages[-5:])  # Show last 5 messages

    async def sendMessage(self, message):
        if self.connected:
            await self.websocket.send(message)
            self.messages.append(f"You: {message}")

def main():
    client = WebSocketClient()
    asyncio.run(client.connect())  # Connect to the WebSocket server
    client.start()  # Start the simpleGE scene

if __name__ == "__main__":
    main()