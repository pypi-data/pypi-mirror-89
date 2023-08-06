import GameKit
from PyObjCTools.TestSupport import TestCase, min_os_level


class TestGKPlayerHelper(GameKit.GKPlayer):
    def isFriend(self):
        return 1


class TestGKPlayer(TestCase):
    def testConstants(self):
        self.assertEqual(GameKit.GKPhotoSizeSmall, 0)
        self.assertEqual(GameKit.GKPhotoSizeNormal, 1)

    @min_os_level("10.16")
    def testConstants10_16(self):
        self.assertIsInstance(GameKit.GKPlayerIDNoLongerAvailable, str)

    def testMethods(self):
        self.assertArgIsBlock(
            GameKit.GKPlayer.loadPlayersForIdentifiers_withCompletionHandler_, 1, b"v@@"
        )

    @min_os_level("10.8")
    def testMethods10_8(self):
        self.assertArgIsBlock(
            GameKit.GKPlayer.loadPhotoForSize_withCompletionHandler_, 1, b"v@@"
        )

        self.assertResultIsBOOL(TestGKPlayerHelper.isFriend)

    @min_os_level("10.15")
    def testMethods10_15(self):
        self.assertResultIsBOOL(GameKit.GKPlayer.scopedIDsArePersistent)

    @min_os_level("10.16")
    def testMethods10_16(self):
        self.assertResultIsBOOL(GameKit.GKPlayer.isInvitable)
