from collections import namedtuple

from Vintageous.tests import ViewTest
from Vintageous.vi.utils import modes

test_data = namedtuple('test_data', 'text startRegion findChar expectedRegion msg')

TEST_MULTI_CHAR_CASES = (
	test_data('0ab3x5', (1, 3), 'x', (1, 5), 'Forward'),
	test_data('0a23x5', (1, 5), 'x', (1, 5), 'Forward find b'),
	test_data('0b2xa5', (5, 1), 'x', (5, 3), 'Reverse no crossover'),
	test_data('0ba3x5', (3, 1), 'x', (2, 5), 'Reverse crossover'),
	test_data('0b2x45', (4, 1), 'x', (4, 3), 'Reverse find a'),
	test_data('0x2a45', (4, 1), 'x', (4, 1), 'Reverse find b'),
)

TEST_ONE_CHAR_CASES = (
	test_data('ax', (0, 2), 'x', (0, 2), 'Forward find b'),
	test_data('bx', (2, 0), 'x', (2, 1), 'Reverse find a'),
	test_data('fx', (0, 1), 'x', (0, 2), 'Forward find next'),
	test_data('rx', (1, 0), 'x', (0, 2), 'Reverse find next'),
	test_data('f',  (0, 1), 'f', (0, 1), 'Forward find self'),
	test_data('r',  (1, 0), 'r', (1, 0), 'Reverse find self'),
)

TEST_MULTI_MATCHES_CASES = (
	test_data('0abxx5', (1, 3), 'x', (1, 4), 'Forward find first'),
	test_data('0axx45', (1, 3), 'x', (1, 4), 'Forward find b'),
	test_data('0bxx45', (3, 1), 'x', (3, 2), 'Reverse find a'),
	test_data('0bxx45', (4, 1), 'x', (4, 2), 'Reverse find a'),
	test_data('0xax45', (3, 1), 'x', (2, 4), 'Reverse find b'),
)

class Test_f_visual_mode(ViewTest):
	def runTests(self, data):
		for (i, data) in enumerate(data):
			self.write(data.text)
			self.clear_sel()
			self.add_sel(self.R(*data.startRegion))
			self.view.run_command('_vi_find_in_line',
				{'mode': modes.VISUAL, 'count': 1, 'char': data.findChar, 'inclusive': True})
			self.assertEqualRegions(self.R(*data.expectedRegion), self.first_sel(),
				"Failed on index {} {} : Text:\"{}\" Region:{} Find:'{}'"
					.format(i, data.msg, data.text, data.startRegion, data.findChar))

	def testMultipleCharacterCases(self):
		self.runTests(TEST_MULTI_CHAR_CASES)

	def testSingleCharacterCases(self):
		self.runTests(TEST_ONE_CHAR_CASES)

	def testMultipleMatchesCase(self):
		self.runTests(TEST_MULTI_MATCHES_CASES)
