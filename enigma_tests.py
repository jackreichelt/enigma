import unittest
from enigma import *

class TestRotor(unittest.TestCase):

    def setUp(self):
        self.r = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ")

    def test_reversability(self):
        self.assertEqual(self.r.encode_in("A"), "E")
        self.assertEqual(self.r.encode_out("E"), "A")
    
    def test_rotation(self):
        self.assertEqual(self.r.encode_in("A"), "E")
        self.r.rotate()
        self.assertEqual(self.r.encode_in("A"), "K")
    
    def test_rotation_loop(self):
        self.r.set_position(25)
        self.assertEqual(self.r.encode_in("A"), "J")
        self.r.rotate()
        self.assertEqual(self.r.encode_in("A"), "E")
    
    def test_ring_setting(self):
        self.assertEqual(self.r.encode_in("A"), "E")
        self.r.set_ring_setting("B")
        self.assertEqual(self.r.encode_in("A"), "K")

class TestEnigmaViability(unittest.TestCase):

    def setUp(self):
        self.em = Enigma(3)
        self.em.set_random_rotors()

    def test_reversability(self):
        plaintext = "HELLO WORLD!"
        ciphertext = self.em.encode_message(plaintext)
        self.em.reset_rotors()
        decodedtext = self.em.decode_message(ciphertext)
        self.assertEqual(plaintext, decodedtext)
    
    def test_chained_rotation(self):
        self.em.rotors[0].set_position(25)
        self.em.rotor_step()
        self.assertEqual(self.em.rotors[0].position, 0)
        self.assertEqual(self.em.rotors[1].position, 1)
    
    def test_longer_message(self):
        plaintext = "HELLO EVERYONE. THIS IS A LONGER MESSAGE ENCODED WITH THE ENIGMA MACHINE."
        ciphertext = self.em.encode_message(plaintext)
        self.em.reset_rotors()
        decodedtext = self.em.decode_message(ciphertext)
        self.assertEqual(plaintext, decodedtext)

class TestEnigmaAuthenticity(unittest.TestCase):

    def setUp(self):
        self.em = Enigma(3)
        self.em.set_reflector(ref_b)
        self.em.set_rotor(rotor_I, 2)
        self.em.set_rotor(rotor_II, 1)
        self.em.set_rotor(rotor_III, 0)
        self.em.reset_rotors()
        self.em.set_start_positions("AAA")

    # @unittest.skip("Not sure why not authentic yet")
    def test_aaaaa(self):
        plaintext = "AAAAA"
        ciphertext = self.em.encode_message(plaintext)
        expected = "BDZGO"
        self.assertEqual(ciphertext, expected)
    
    def test_aaaaa_offset(self):
        self.em.set_ring_settings("BBB")
        plaintext = "AAAAA"
        ciphertext = self.em.encode_message(plaintext)
        expected = "EWTYX"
        self.assertEqual(ciphertext, expected)
    


class TestEnigmaDonitz(unittest.TestCase):

    def setUp(self):
        self.em = Enigma(4)
        self.em.set_reflector(ref_c_thin)
        self.em.set_rotor(rotor_beta, 3)
        self.em.set_rotor(rotor_V, 2)
        self.em.set_rotor(rotor_VI, 1)
        self.em.set_rotor(rotor_VIII, 0)
        self.em.reset_rotors()
        self.em.set_ring_settings("EPEL")
        self.em.set_start_positions("NAEM")
        for pair in "AE BF CM DQ HU JN LX PR SZ VW".split(" "):
            self.em.add_swap(pair[0], pair[1])

    @unittest.skip("Not sure why not authentic yet")
    def test_donitz_message_key(self):
        first_key = "QEOB"
        expected_key = "CDSZ"

        self.assertEqual(self.em.encode_message(first_key), expected_key)
    
    @unittest.skip("Not sure why not authentic yet")
    def test_donitz_message(self):
        self.em.set_start_positions("CDSZ")
        cipher_text = self.em.encode_message("KRKR ALLE XX")
        expected_text = "LANO TCTO UA"
        self.assertEqual(cipher_text, expected_text)




if __name__ == '__main__':
    unittest.main()

# def test_AAAAA():
#     em = Enigma(3)
#     em.set_rotor(rotor_III, 0)
#     em.set_rotor(rotor_II, 1)
#     em.set_rotor(rotor_I, 2)
#     em.set_reflector(ref_b)

#     em.print_state()

#     result = em.encode_message("AAAAA")
#     print(f"{result = }")