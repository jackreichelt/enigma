from random import shuffle
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
greek = -4
l = -3
m = -2
r = -1

class Rotor:

    def __init__(self, wiring: str, turnovers: list[str] = []) -> None:
        self.encoding_string = wiring
        self.wiring = [alphabet.index(c)-i for i, c in enumerate(wiring)]
        self.reverse = [0] * 26
        for i, delta in enumerate(self.wiring):
            self.reverse[(i+delta)%26] = i
        self.position = 0
        self.ring_setting = 0
        self.turnovers = []
        for t in turnovers:
            self.add_turnover_letter(t)
    
    def add_turnover_letter(self, letter: str) -> None:
        self.turnovers.append((alphabet.index(letter)+1)%26)
    
    def set_ring_setting(self, new_setting: str | int) -> None:
        if isinstance(new_setting, int):
            self.ring_setting = new_setting
        else:
            self.ring_setting = alphabet.index(new_setting)

    def set_position(self, pos: int):
        while self.position != pos:
            self.rotate()
    
    def reset(self):
        self.set_position(0)
        self.set_ring_setting("A")

    def rotate(self) -> bool:
        # self.wiring = self.wiring[1:] + [self.wiring[0]]
        self.position += 1
        self.position %= 26
        return self.position in self.turnovers

    def encode_in(self, val: int) -> int:
        in_wire = (val - self.ring_setting + self.position) % 26
        out_wire = val + self.wiring[in_wire]
        out_wire %= 26
        return out_wire

    def encode_out(self, val: int) -> int:
        in_wire = (val - self.ring_setting + self.position) % 26
        out_wire = self.reverse[in_wire]
        out_wire += self.ring_setting
        out_wire -= self.position
        out_wire %= 26
        return out_wire

class Reflector:
    def __init__(self, wiring: list[int]) -> None:
        self.wiring = [alphabet.index(c) for c in wiring]
    
    def __getitem__(self, item) -> int:
        return self.wiring[item]

def make_rotor() -> Rotor:
    subs = list(alphabet)
    shuffle(subs)
    subs = ''.join(subs)
    return Rotor(subs)

class Enigma:

    def __init__(self, reflector: Reflector, rotors: list[Rotor]) -> None:
        self.rotor_count = len(rotors)
        self.rotors = rotors
        self.reflector = reflector
        self.swaps = {}
        self.double_step = False
    
    def print_state(self) -> None:
        # print(self.swaps)
        # for i in range(3):
        #     print(alphabet)
        #     print(self.rotors[i].subs)
        #     print()
        # print(self.reflector)
        pass
    
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

    def reset_rotors(self) -> None:
        for r in self.rotors:
            r.reset()
    
    def set_ring_settings(self, settings: str | list[int]) -> None:
        for i in range(self.rotor_count):
            self.rotors[i].set_ring_setting(settings[i])
    
    def set_start_positions(self, positions: str) -> None:
        for i in range(self.rotor_count):
            pos = alphabet.index(positions[i])
            self.rotors[i].set_position(pos)
        
    def ring_positions(self) -> str:
        l_pos = alphabet[self.rotors[l].position]
        m_pos = alphabet[self.rotors[m].position]
        r_pos = alphabet[self.rotors[r].position]
        return f"{l_pos}{m_pos}{r_pos}"
    
    def letter_to_wire_index(self, letter: str) -> int:
        if letter in self.swaps:
            letter = self.swaps[letter]
        return alphabet.index(letter)

    def wire_index_to_letter(self, index: int) -> str:
        letter = alphabet[index]
        if letter in self.swaps:
            return self.swaps[letter]
        return letter
    
    def add_swap(self, a: str, b: str) -> None:
        self.swaps[a] = b
        self.swaps[b] = a
    
    def add_swaps(self, swaps: str) -> None:
        for pair in swaps.split(" "):
            self.add_swap(pair[0], pair[1])

    def rotor_step(self) -> None:
        middle_turnover = self.rotors[r].rotate()
        if middle_turnover or self.double_step:
            left_turnover = self.rotors[m].rotate()
            self.double_step = False
            if (self.rotors[m].position + 1) % 26 in self.rotors[m].turnovers:
                self.double_step = True
            if left_turnover:
                self.rotors[l].rotate()
    
    def encode_letter(self, l: str) -> str:
        l = l.upper()

        l = self.letter_to_wire_index(l)

        for r in self.rotors[::-1]:
            l = r.encode_in(l)
        
        l = self.reflector[l]

        for r in self.rotors:
            l = r.encode_out(l)
            
        l = self.wire_index_to_letter(l)

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

rotor_I = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", ["Q"])
rotor_II = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", ["E"])
rotor_III = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", ["V"])
rotor_IV = Rotor("ESOVPZJAYQUIRHXLNFTGKDCMWB", ["J"])
rotor_V = Rotor("VZBRGITYUPSDNHLXAWMJQOFECK", ["Z"])
rotor_VI = Rotor("JPGVOUMFYQBENHZRDKASXLICTW", ["M", "Z"])
rotor_VII = Rotor("NZJHGRCXMYSWBOUFAIVLPEKQDT", ["M", "Z"])
rotor_VIII = Rotor("FKQHTLXOCBJSPDZRAMEWNIUYGV", ["M", "Z"])
rotor_beta = Rotor("LEYJVCNIXWPBQMDRTAKZGFUHOS")
rotor_gamma = Rotor("FSOKANUERHMBTIYCWLQPZXVGJD")

ref_a = Reflector("EJMZALYXVBWFCRQUONTSPIKHGD")
ref_b = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
ref_c = Reflector("FVPJIAOYEDRZXWGCTKUQSBNMHL")
ref_b_thin = Reflector("ENKQAUYWJICOPBLMDXZVFTHRGS")
ref_c_thin = Reflector("RDOBJNTKVEHMLFCWZAXGYIPSUQ")
