from PyObjCTools.TestSupport import TestCase, min_os_level
import Vision


class TestVNRecognizeTextRequest(TestCase):
    def test_constants(self):
        self.assertEqual(Vision.VNRequestTextRecognitionLevelAccurate, 0)
        self.assertEqual(Vision.VNRequestTextRecognitionLevelFast, 1)

        self.assertEqual(Vision.VNRecognizeTextRequestRevision1, 1)
        self.assertEqual(Vision.VNRecognizeTextRequestRevision2, 2)

    @min_os_level("10.15")
    def test_methods(self):
        self.assertArgIsOut(
            Vision.VNRecognizeTextRequest.supportedRecognitionLanguagesForTextRecognitionLevel_revision_error_,  # noqa: B950
            2,
        )

        self.assertResultIsBOOL(Vision.VNRecognizeTextRequest.usesLanguageCorrection)
        self.assertArgIsBOOL(
            Vision.VNRecognizeTextRequest.setUsesLanguageCorrection_, 0
        )
