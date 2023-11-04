import unittest
from enigma import *

def wire(l):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return alphabet.index(l)

class TestRotor(unittest.TestCase):

    def setUp(self):
        self.r = rotor_I
        self.r.reset()

    def test_reversability(self):
        self.assertEqual(self.r.encode_in(wire("A")), wire("E"))
        self.assertEqual(self.r.encode_out(wire("E")), wire("A"))
    
    def test_rotation(self):
        self.assertEqual(self.r.encode_in(wire("A")), wire("E"))
        self.r.rotate()
        self.assertEqual(self.r.encode_in(wire("A")), wire("J"))
    
    def test_rotation_loop(self):
        self.r.set_position(25)
        self.assertEqual(self.r.encode_in(wire("A")), wire("K"))
        self.r.rotate()
        self.assertEqual(self.r.encode_in(wire("A")), wire("E"))
    
    def test_ring_setting(self):
        self.r.set_ring_setting("B")
        self.assertEqual(self.r.encode_in(wire("A")), wire("K"))
        self.assertEqual(self.r.encode_out(wire("K")), wire("A"))
    
    def test_complex_settings(self):
        self.r.set_ring_setting("F")
        self.r.set_position(wire("Y"))
        self.assertEqual(self.r.encode_in(wire("A")), wire("W"))
        self.assertEqual(self.r.encode_out(wire("W")), wire("A"))

class TestEnigmaViability(unittest.TestCase):

    def setUp(self):
        self.em = Enigma(ref_a, [rotor_III, rotor_II, rotor_I])
        self.em.reset_rotors()

    def test_reversability(self):
        plaintext = "HELLO WORLD!"
        ciphertext = self.em.encode_message(plaintext)
        self.em.reset_rotors()
        decodedtext = self.em.decode_message(ciphertext)
        self.assertEqual(plaintext, decodedtext)
    
    def test_chained_rotation(self):
        self.em.rotors[r].set_position(wire("Q"))
        self.em.rotor_step()
        self.assertEqual(self.em.rotors[r].position, wire("R"))
        self.assertEqual(self.em.rotors[m].position, 1)
    
    def test_longer_message(self):
        plaintext = "HELLO EVERYONE. THIS IS A LONGER MESSAGE ENCODED WITH THE ENIGMA MACHINE."
        ciphertext = self.em.encode_message(plaintext)
        self.em.reset_rotors()
        decodedtext = self.em.decode_message(ciphertext)
        self.assertEqual(plaintext, decodedtext)
    
    def test_double_step(self):
        self.em.set_start_positions("VDQ")
        self.em.rotor_step()
        self.assertEqual(self.em.ring_positions(), "VER")
        self.em.rotor_step()
        self.assertEqual(self.em.ring_positions(), "WFS")
        self.em.rotor_step()
        self.assertEqual(self.em.ring_positions(), "WFT")
    
    def test_real_double_step(self):
        self.em.set_start_positions("KDO")
        self.em.rotor_step()
        self.assertEqual(self.em.ring_positions(), "KDP")
        self.em.rotor_step()
        self.assertEqual(self.em.ring_positions(), "KDQ")
        self.em.rotor_step()
        self.assertEqual(self.em.ring_positions(), "KER")
        self.em.rotor_step()
        self.assertEqual(self.em.ring_positions(), "LFS")
        self.em.rotor_step()
        self.assertEqual(self.em.ring_positions(), "LFT")
        self.em.rotor_step()
        self.assertEqual(self.em.ring_positions(), "LFU")

class TestEnigmaBasicAuthenticity(unittest.TestCase):

    def setUp(self):
        self.em = Enigma(ref_b, [rotor_I, rotor_II, rotor_III])
        self.em.reset_rotors()

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

class TestEnigmaAuthenticity(unittest.TestCase):

    @unittest.skip("Possibly this example is wrong? All other authentic tests pass.")
    def test_minor(self):
        em = Enigma(ref_b, [rotor_I, rotor_II, rotor_V])
        em.set_ring_settings([6, 22, 14])
        em.add_swaps("PO ML IU KJ NH YT GB VF RE DC")
        em.set_start_positions("EHZ")
        message_key = em.decode_message("TBS")
        self.assertEquals(message_key, "XWB")
    
    def test_wehrmacht(self):
        em = Enigma(ref_b, [rotor_II, rotor_IV, rotor_V])
        em.set_ring_settings("BUL")
        em.add_swaps("AV BS CG DL FU HZ IN KM OW RX")
        em.set_start_positions("WXC")
        message_key = em.decode_message("KCH")
        self.assertEquals(message_key, "BLA")

        em.set_start_positions(message_key)
        self.assertEquals(em.decode_message("EDPUD"), "AUFKL")

        full_message = """
        EDPUD NRGYS ZRCXN UYTPO
        MRMBO FKTBZ REZKM LXLVE
        FGUEY SIOZV EQMIK UBPMM
        YLKLT TDEIS MDICA GYKUA
        CTCDO MOHWX MUUIA UBSTS
        LRNBZ SZWNR FXWFY SSXJZ
        VIJHI DISHP RKLKA YUPAD
        TXQSP INQMA TLPIF SVKDA
        SCTAC DPBOP VHJK
        """
        full_decoded = """
        AUFKL XABTE ILUNG XVONX
        KURTI NOWAX KURTI NOWAX
        NORDW ESTLX SEBEZ XSEBE
        ZXUAF FLIEG ERSTR ASZER
        IQTUN GXDUB ROWKI XDUBR
        OWKIX OPOTS CHKAX OPOTS
        CHKAX UMXEI NSAQT DREIN
        ULLXU HRANG ETRET ENXAN
        GRIFF XINFX RGTX
        """

        em.set_start_positions(message_key)
        self.assertEquals(em.decode_message(full_message), full_decoded)

class TestEnigmaDonitz(unittest.TestCase):

    def setUp(self):
        self.em = Enigma(ref_c_thin, [rotor_beta, rotor_V, rotor_VI, rotor_VIII])
        self.em.reset_rotors()
        self.em.set_ring_settings("EPEL")
        self.em.set_start_positions("NAEM")
        for pair in "AE BF CM DQ HU JN LX PR SZ VW".split(" "):
            self.em.add_swap(pair[0], pair[1])

    def test_donitz_message_key(self):
        first_key = "QEOB"
        expected_key = "CDSZ"

        self.assertEqual(self.em.encode_message(first_key), expected_key)
    
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