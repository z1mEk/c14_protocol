######################################################################################
# Descirption: C14 Protocol python class
# author: Gabriel Zima (z1mEk)
# e-mail: gabriel.zima@wp.pl
# github: https://github.com/z1mEk/c14_protocol.git
# create date: 2018-08-09
# update date: 2018-08-09
######################################################################################

class C14:

    def CalcCSum(self, bFrame):
        cSum = 0
        return cSum

    def CheckCSum(self, bFrame, CompCSum):
        cSum = self.CalcCSum(bFrame)
        if cSUM == CompCSum:
            return 1
	else:
            return 0

    def ReadTemps(self, SendFrame):
        RecFrame = SendFrame
        return RecFrame

    def ReadParams(self, SendFrame):
        RecFrame = SendFrame
        return RecFrame

    def WriteParams(self, SendFrame):
        RecFrame = SendFrame
        return RecFrame
