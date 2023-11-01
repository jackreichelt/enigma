from random import shuffle
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class Rotor:
    def __init__(self, subs: str, turnovers: list[int] = [0]) -> None:
        self.subs = subs.upper()
        self.position = 0
        self.turnovers = turnovers
        self.ring_setting = 0
    
    def add_turnover_letter(self, letter: str) -> None:
        current_pos = self.position
        self.set_position(0)
        self.turnovers.append((self.subs.index(letter)+1)%26)
        self.set_position(current_pos)
    
    def set_ring_setting(self, new_setting: str) -> None:
        new_ring_setting = alphabet.index(new_setting)
        while self.ring_setting != new_ring_setting:
            self.subs = self.subs[1:] + self.subs[0]
            self.ring_setting += 1
            self.ring_setting %= 26

    def set_position(self, pos: int):
        while self.position != pos:
            self.rotate()

    def rotate(self) -> bool:
        self.subs = self.subs[1:] + self.subs[0]
        self.position += 1
        self.position %= 26

        return self.position in self.turnovers

    def encode_in(self, l: str) -> str:
        i = alphabet.index(l.upper())
        return self.subs[i]
    
    def encode_out(self, l: str) -> str:
        i = self.subs.index(l.upper())
        return alphabet[i]

def make_rotor() -> Rotor:
    subs = list(alphabet)
    shuffle(subs)
    subs = ''.join(subs)
    return Rotor(subs)

class Enigma:

    def __init__(self, rotor_count: int) -> None:
        self.rotor_count = rotor_count
        self.rotors: list[Rotor] = [None] * rotor_count
        self.reflector = {}
        self.swaps = {}
    
    def print_state(self) -> None:
        print(self.swaps)
        for i in range(3):
            print(alphabet)
            print(self.rotors[i].subs)
            print()
        print(self.reflector)
    
    def generate_reflector(self) -> str:
        subs = list(alphabet)
        shuffle(subs)
        subs = ''.join(subs)
        for i in range(13):
            a = subs[i]
            b = subs[-i-1]
            self.reflector[a] = b
            self.reflector[b] = a

    def set_random_rotors(self) -> None:
        for i in range(self.rotor_count):
            self.set_rotor(make_rotor(), i)
        self.generate_reflector()

    def set_rotor(self, rotor: Rotor, pos: int) -> None:
        if 0 <= pos < self.rotor_count:
            self.rotors[pos] = rotor
    
    def set_reflector(self, reflector) -> None:
        self.reflector = reflector
    
    def reset_rotors(self) -> None:
        for r in self.rotors:
            r.set_ring_setting("A")
            r.set_position(0)
    
    def set_ring_settings(self, settings: str) -> None:
        settings = settings[::-1] # settings come left-to-right, but rotors are indexed right-to-left
        for i in range(self.rotor_count):
            self.rotors[i].set_ring_setting(settings[i])
    
    def set_start_positions(self, positions: str) -> None:
        positions = positions[::-1] # positions come left-to-right, but rotors are indexed right-to-left
        for i in range(self.rotor_count):
            pos = alphabet.index(positions[i])
            self.rotors[i].set_position(pos)
    
    def add_swap(self, a: str, b: str) -> None:
        self.swaps[a] = b
        self.swaps[b] = a

    def rotor_step(self) -> None:
        for i in range(self.rotor_count):
            if self.rotors[i].rotate():
                continue
            break
    
    def encode_letter(self, l: str) -> str:
        l = l.upper()

        if l in self.swaps:
            l = self.swaps[l]

        for r in self.rotors:
            l = r.encode_in(l)
        
        l = self.reflector[l]

        for r in self.rotors[::-1]:
            l = r.encode_out(l)
            
        if l in self.swaps:
            l = self.swaps[l]

        return l
    
    def decode_letter(self, l: str) -> str:
        return self.encode_letter(l)
    
    def encode_message(self, m: str) -> str:
        out = ""
        for l in m:
            if l.upper() in alphabet:
                self.rotor_step()
                out += self.encode_letter(l.upper())
            else:
                out += l
        
        return out
    
    def decode_message(self, m: str) -> str:
        return self.encode_message(m)

rotor_I = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", [])
rotor_I.add_turnover_letter("Q")
rotor_II = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", [])
rotor_II.add_turnover_letter("E")
rotor_III = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", [])
rotor_III.add_turnover_letter("V")
rotor_IV = Rotor("ESOVPZJAYQUIRHXLNFTGKDCMWB", [])
rotor_IV.add_turnover_letter("J")
rotor_V = Rotor("VZBRGITYUPSDNHLXAWMJQOFECK", [])
rotor_V.add_turnover_letter("Z")
rotor_VI = Rotor("JPGVOUMFYQBENHZRDKASXLICTW", [])
rotor_VI.add_turnover_letter("M")
rotor_VI.add_turnover_letter("Z")
rotor_VII = Rotor("NZJHGRCXMYSWBOUFAIVLPEKQDT", [])
rotor_VII.add_turnover_letter("M")
rotor_VII.add_turnover_letter("Z")
rotor_VIII = Rotor("FKQHTLXOCBJSPDZRAMEWNIUYGV", [])
rotor_VIII.add_turnover_letter("M")
rotor_VIII.add_turnover_letter("Z")
rotor_beta = Rotor("LEYJVCNIXWPBQMDRTAKZGFUHOS", [])
rotor_gamma = Rotor("FSOKANUERHMBTIYCWLQPZXVGJD", [])

ref_a = {a: b for a, b in zip(alphabet, "EJMZALYXVBWFCRQUONTSPIKHGD")}
ref_b = {a: b for a, b in zip(alphabet, "YRUHQSLDPXNGOKMIEBFZCWVJAT")}
ref_c = {a: b for a, b in zip(alphabet, "FVPJIAOYEDRZXWGCTKUQSBNMHL")}
ref_b_thin = {a: b for a, b in zip(alphabet, "ENKQAUYWJICOPBLMDXZVFTHRGS")}
ref_c_thin = {a: b for a, b in zip(alphabet, "RDOBJNTKVEHMLFCWZAXGYIPSUQ")}
