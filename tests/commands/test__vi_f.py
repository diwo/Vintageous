from collections import namedtuple

from Vintageous.tests import ViewTest
from Vintageous.vi.utils import modes

test_data = namedtuple('test_data', 'text startRegion findChar mode expectedRegion msg')

VISUAL_MULTI_CHAR_CASES = (
	test_data('0ab3x5', (1, 3), 'x', modes.VISUAL, (1, 5), 'Forward'),
	test_data('0a23x5', (1, 5), 'x', modes.VISUAL, (1, 5), 'Forward find b'),
	test_data('0b2xa5', (5, 1), 'x', modes.VISUAL, (5, 3), 'Reverse no crossover'),
	test_data('0ba3x5', (3, 1), 'x', modes.VISUAL, (2, 5), 'Reverse crossover'),
	test_data('0b2x45', (4, 1), 'x', modes.VISUAL, (4, 3), 'Reverse find a'),
	test_data('0x2a45', (4, 1), 'x', modes.VISUAL, (4, 1), 'Reverse find b'),
)

VISUAL_ONE_CHAR_CASES = (
	test_data('ax', (0, 2), 'x', modes.VISUAL, (0, 2), 'Forward find b'),
	test_data('bx', (2, 0), 'x', modes.VISUAL, (2, 1), 'Reverse find a'),
	test_data('fx', (0, 1), 'x', modes.VISUAL, (0, 2), 'Forward find next'),
	test_data('rx', (1, 0), 'x', modes.VISUAL, (0, 2), 'Reverse find next'),
	test_data('f',  (0, 1), 'f', modes.VISUAL, (0, 1), 'Forward find self'),
	test_data('r',  (1, 0), 'r', modes.VISUAL, (1, 0), 'Reverse find self'),
)

VISUAL_MULTI_MATCHES_CASES = (
	test_data('0abxx5', (1, 3), 'x', modes.VISUAL, (1, 4), 'Forward find first'),
	test_data('0axx45', (1, 3), 'x', modes.VISUAL, (1, 4), 'Forward find b'),
	test_data('0bxx45', (3, 1), 'x', modes.VISUAL, (3, 2), 'Reverse find a'),
	test_data('0bxx45', (4, 1), 'x', modes.VISUAL, (4, 2), 'Reverse find a'),
	test_data('0xax45', (3, 1), 'x', modes.VISUAL, (2, 4), 'Reverse find b'),
)

class Test_vi_f(ViewTest):
	def runTests(self, data):
		for (i, data) in enumerate(data):
			self.write(data.text)
			self.clear_sel()
			self.add_sel(self.R(*data.startRegion))
			self.view.run_command('_vi_find_in_line',
				{'mode': data.mode, 'count': 1, 'char': data.findChar, 'inclusive': True})
			self.assertEqualRegions(self.R(*data.expectedRegion), self.first_sel(),
				"Failed on index {} {} : Text:\"{}\" Region:{} Find:'{}'"
					.format(i, data.msg, data.text, data.startRegion, data.findChar))

	def testVisualMultipleCharacterCases(self):
		self.runTests(VISUAL_MULTI_CHAR_CASES)

	def testVisualSingleCharacterCases(self):
		self.runTests(VISUAL_ONE_CHAR_CASES)

	def testVisualMultipleMatchesCase(self):
		self.runTests(VISUAL_MULTI_MATCHES_CASES)
