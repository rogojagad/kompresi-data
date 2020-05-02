from encoder import Encoder
from decoder import Decoder

class ShannonFano:
    def __init__(self):
        self.encoder = Encoder()
        self.decoder = Decoder()

    def run(self):
        self.encoder.runEncode()

        self.decoder.runDecode()

if __name__ == "__main__":
    sf = ShannonFano()

    sf.run()