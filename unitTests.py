import unittest
from unittest.mock import patch
from JapTool import Settings, Game

class TestJapTool(unittest.TestCase):

    def setUp(self):
        self.settings = Settings()
        self.game = Game()
        self.settings.changeSettings('default')
        self.settings.mode = 'test'
        self.game.settings.mode = 'test'

    def test_mode(self):
        self.assertEqual(self.settings.mode, 'test')
        self.assertEqual(self.game.settings.mode, 'test')

    def test_gameSetUp(self):
        self.assertEqual(self.game.romaji, "x")
        self.assertEqual(self.game.prompt, "")

    def test_startUp(self):
        self.assertEqual(self.settings.startUp(), "Settings imported!")
        self.assertEqual(self.settings.minInd, 0)
        self.assertEqual(self.settings.maxInd, 70)
        self.assertEqual(self.settings.symbAmt, 10)
        self.assertEqual(self.settings.currDict, 'hiragana')

    def test_changeDict(self):
        with patch('builtins.input', return_value='K'):
            self.settings.changeSettings('dict')
        self.assertEqual(self.settings.currDict, 'katakana')

    def test_changeSymbAmt(self):
        with patch('builtins.input', return_value='20'):
            self.settings.changeSettings('amt')
        self.assertEqual(self.settings.symbAmt, 20)

    def test_changeSymbAmtInvalid(self):
        with patch('builtins.input', side_effect=['0', '20']):
            self.assertEqual(self.settings.changeSettings('amt'), "Invalid input!")
            self.assertEqual(self.settings.symbAmt, 20)

    def test_changeIndRange(self):
        with patch('builtins.input', side_effect=['10', '20']):
            self.settings.changeSettings('ind')
        self.assertEqual(self.settings.minInd, 10)
        self.assertEqual(self.settings.maxInd, 20)

    def test_changeIndRangeInvalid(self):
        with patch('builtins.input', side_effect=['10', '5', '10', '70']):
            self.assertEqual(self.settings.changeSettings('ind'), "Invalid input!")
            self.assertEqual(self.settings.minInd, 10)
            self.assertEqual(self.settings.maxInd, 70)

    def test_readSettings(self):
        self.assertEqual(self.settings.changeSettings('read'), "Settings read!")

    def test_OWFile(self):
        self.settings.OWFile('symbAmt', 'symbAmt = 3')
        with open ('settings.txt', 'r') as file:
            data = file.read()
            self.assertTrue('symbAmt = 3' in data)

    def test_defaultSettings(self):
        self.settings.changeSettings('default')
        self.assertEqual(self.settings.minInd, 0)
        self.assertEqual(self.settings.maxInd, 70)
        self.assertEqual(self.settings.symbAmt, 10)
        self.assertEqual(self.settings.currDict, 'hiragana')

    def test_invalidCommand(self):
        self.assertEqual(self.settings.changeSettings('Invalid'), "Invalid command!")

    def test_readFile(self):
        self.game.readFile()
        self.assertEqual(self.game.hana[1], 'か')
        self.assertEqual(self.game.kata[1], 'カ')
        self.assertEqual(self.game.roma[1], 'ka')

    def test_getCommand(self):
        with patch('builtins.input', return_value='test'):
            self.assertEqual(self.game.getCommand(), 'test')

    def test_getSymb(self):
        self.assertEqual(self.game.getSymb(1, self.settings), 'か')

    def test_givePrompt(self):
        with patch('builtins.input', return_value='1'):
            self.settings.changeSettings('amt')
        with patch('builtins.input', side_effect=['1', '2']):
            self.settings.changeSettings('ind')
        self.assertEqual(self.game.givePrompt(self.settings), 'か')

    def test_getRomaji(self):
        self.assertEqual(self.game.getRomaji(1), 'ka')

    def test_checkAnswer(self):
        self.game.romaji = 'ka'
        self.assertEqual(self.game.checkAnswer('ka'), True)
        self.assertEqual(self.game.checkAnswer('a'), False)

    def test_checkInARow(self):
        self.assertEqual(self.game.inARow, 0)
        self.game.romaji = 'ka'
        self.game.checkAnswer('ka')
        self.assertEqual(self.game.inARow, 1)

    def test_startGame(self):
        with patch('builtins.input', return_value='x'):
            self.assertEqual(self.game.start(), 'Game over!')

if __name__ == '__main__':
    unittest.main()