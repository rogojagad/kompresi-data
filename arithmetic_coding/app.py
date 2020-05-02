from encoder import Encoder
from decoder import Decoder

class App:
    def __init__(self):
        self.encoder = Encoder()
        self.decoder = Decoder()

    def run(self):
        self.encoder.run()

        self.decoder.run()

if __name__ == "__main__":
    app = App()

    app.run()