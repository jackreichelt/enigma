"""
General methodology:

Find a chunk of the message that you believe you know where it is in the code.
You can do this by ensuring no letters encoded to themselves.
We'll call these snippets our text_phrase and our code_phrase.
    eg: code_phrase: ATGBGGYWCRYBG
        text_phrase: WETTERBERICHT

Treat the total rotor settings as a single vector. Pick any starting point.
Assume any plugboard connection for the first letter.
    eg: (T, A) connected
Pick a letter from the code_phrase and what it decodes to from the text_phrase.
We'll call these the code_letter and the text_letter.
    eg: T -> E (index 1)
For the correct settings, this coding is true.
Find what now comes out of the rotors when the connected letter is input.
If the output is not correct (E in the example),
  then deduce another plugboard connection from the output to the text_letter.
Repeat for another pair of letters from the phrases.
If no contradictory connections are found:
    You have found your initial rotor settings.
Else:
    You can mark all deduced connections as bad.
    In future tests, if these are deduced again, you can fail that test.
    Pick a new initial connection, eg (T, B).
    Reset your rotors to the starting settings.

If all 26 connections for your first letter (25 other letters, as well as no connection) are invalid:
    your rotor starting settings are incorrect.
    Advance the rotor one tick, then try again.

This gives a problem space of:
    26 initial connections on the plugboard
    26 x 26 x 26 rotor positions
    26 x 26 x 26 ring settings
    26 ^ 7 in total
    8,031,810,176 possiblities to be checked

    If ring settings are ignored:
    26 ^ 4 possibilities
    456,976 possibilities
"""
from enigma import *

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

invalid_rotors = set()
invalid_settings = set()
invalid_swaps = set()
invalid_start_positions = set()

def find_next_swap():
    for a in alphabet:
        for b in alphabet:
            if a == b:
                continue
            a, b = sorted((a, b)) # ensure consistent order
            if a+b not in invalid_swaps and a+b not in current_swaps():
                return a+b
    


code_phrase = input("Enter the code phrase: ")
text_phrase = input("What do you think this means? ")

ring_settings = [0, 0, 0]
current_swaps = set()
start_positions = ""

em = Enigma(ref_a, [rotor_I, rotor_II, rotor_III])
em.set_ring_settings(ring_settings)
em.set_swaps(" ".join(current_swaps))
em.set_start_positions(start_positions)



