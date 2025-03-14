import random
import hmac
import hashlib

class FairRandomGenerator:
    def __init__(self, range_max):
        self.range_max = range_max
        self.key = random.randbytes(32)  # 256-bit key
        self.computer_number = random.randint(0, range_max)
        self.hmac = self._calculate_hmac()

    def _calculate_hmac(self):
        return hmac.new(self.key, str(self.computer_number).encode(), hashlib.sha3_256).hexdigest()

    def get_hmac(self):
        return self.hmac

    def get_result(self, user_number):
        result = (self.computer_number + user_number) % (self.range_max + 1)
        return result, self.key.hex()