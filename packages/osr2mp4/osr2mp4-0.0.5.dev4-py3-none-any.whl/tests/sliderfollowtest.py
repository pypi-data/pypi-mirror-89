import unittest
from osr2mp4.CheckSystem.checkmain import checkmain
from osr2mp4.global_var import Settings
from utils import getinfos


class TestSliderfollow(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.real = []
		cls.tests = []
		cls.custom = []
		cls.custom_expect100 = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0]
		cls.custom_expect50 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		cls.settings = Settings()
		cls.settings.timeframe = 1000
		cls.settings.fps = 60
		cls.tests.append(getinfos("yomi"))
		cls.tests.append(getinfos("tool"))
		cls.tests.append(getinfos("2tool"))
		cls.tests.append(getinfos("2yomi"))
		cls.tests.append(getinfos("4yomi"))

		cls.custom.append(getinfos("69tool"))
		cls.custom.append(getinfos("69yomi", True))
		cls.custom.append(getinfos("70tool"))
		cls.custom.append(getinfos("71tool"))
		cls.custom.append(getinfos("69kikoku"))
		cls.custom.append(getinfos("70kikoku"))
		cls.custom.append(getinfos("71kikoku"))
		cls.custom.append(getinfos("72yomi", True))
		cls.custom.append(getinfos("73yomi", True))
		cls.custom.append(getinfos("74yomi", True))
		cls.custom.append(getinfos("75yomi", True))
		cls.custom.append(getinfos("76yomi", True))
		cls.custom.append(getinfos("77yomi", True))
		cls.custom.append(getinfos("72tool"))
		cls.custom.append(getinfos("73tool"))
		cls.custom.append(getinfos("74tool"))
		cls.custom.append(getinfos("75tool"))
		cls.custom.append(getinfos("76tool"))
		cls.custom.append(getinfos("72kikoku"))
		cls.custom.append(getinfos("blends"))
		cls.custom.append(getinfos("date"))
		cls.custom.append(getinfos("69reimei"))
		cls.custom.append(getinfos("73kikoku"))
		cls.custom.append(getinfos("74kikoku"))

		cls.real.append(getinfos("realtool"))
		cls.real.append(getinfos("realyomi", True))
		cls.real.append(getinfos("realkikoku"))
		cls.real.append(getinfos("realmagnolia"))
		cls.real.append(getinfos("realkaede"))
		cls.real.append(getinfos("realexit"))
		cls.real.append(getinfos("realfallen"))

	def test_sliderfollow(self):
		for i in range(len(self.tests)):
			case = self.tests[i]
			print(f"Checking {case[0].path}")

			for x in range(len(case[1])):
				name = x
				if x == 0:
					name = ""
				print(f"Replay {case[2]}{name}.osr")

				resultinfo = checkmain(case[0], case[1][x], self.settings, True)
				self.assertEqual(case[1][x].number_300s, resultinfo[-1].accuracy[300], msg=f"Replay {case[2]}{name}.osr")
				self.assertEqual(case[1][x].number_100s, resultinfo[-1].accuracy[100], msg=f"Replay {case[2]}{name}.osr")
				self.assertEqual(case[1][x].number_50s, resultinfo[-1].accuracy[50], msg=f"Replay {case[2]}{name}.osr")

	def test_sliderfollowcustom(self):
		for i in range(len(self.custom)):
			case = self.custom[i]
			print(f"Checking {case[0].path}")

			for x in range(len(case[1])):
				name = x
				if x == 0:
					name = ""
				print(f"Replay {case[2]}{name}.osr")

				resultinfo = checkmain(case[0], case[1][x], self.settings, True)
				self.assertEqual(self.custom_expect100[i], resultinfo[-1].accuracy[100], msg=f"Replay {case[2]}{name}.osr")
				self.assertEqual(self.custom_expect50[i], resultinfo[-1].accuracy[50], msg=f"Replay {case[2]}{name}.osr")

	def test_real(self):
		for i in range(len(self.real)):
			case = self.real[i]
			for x in range(len(case[1])):
				name = x
				if x == 0:
					name = ""
				print(f"Replay {case[2]}{name}.osr")

				resultinfo = checkmain(case[0], case[1][x], self.settings, True)
				self.assertEqual(case[1][x].number_300s, resultinfo[-1].accuracy[300], msg=f"Replay {case[2]}{name}.osr")
				self.assertEqual(case[1][x].number_100s, resultinfo[-1].accuracy[100], msg=f"Replay {case[2]}{name}.osr")
				self.assertEqual(case[1][x].number_50s, resultinfo[-1].accuracy[50], msg=f"Replay {case[2]}{name}.osr")



if __name__ == '__main__':
	unittest.main()
