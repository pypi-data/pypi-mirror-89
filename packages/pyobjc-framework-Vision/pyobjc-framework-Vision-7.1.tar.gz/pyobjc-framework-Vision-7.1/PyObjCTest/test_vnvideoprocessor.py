from PyObjCTools.TestSupport import TestCase, min_os_level
import Vision


class TestVNVideoProcessor(TestCase):
    @min_os_level("10.16")
    def test_constants(self):
        self.assertIsInstance(Vision.VNVideoProcessingOptionFrameCadence, str)
        self.assertIsInstance(Vision.VNVideoProcessingOptionTimeInterval, str)

    @min_os_level("10.16")
    def test_methods10_16(self):
        self.assertResultIsBOOL(
            Vision.VNVideoProcessor.addRequest_withProcessingOptions_error_
        )
        self.assertArgIsOut(
            Vision.VNVideoProcessor.addRequest_withProcessingOptions_error_, 2
        )
        self.assertResultIsBOOL(
            Vision.VNVideoProcessor.addRequest_processingOptions_error_
        )
        self.assertArgIsOut(
            Vision.VNVideoProcessor.addRequest_processingOptions_error_, 2
        )

        self.assertResultIsBOOL(Vision.VNVideoProcessor.removeRequest_error_)
        self.assertArgIsOut(Vision.VNVideoProcessor.removeRequest_error_, 1)

        self.assertResultIsBOOL(Vision.VNVideoProcessor.analyzeWithTimeRange_error_)
        self.assertArgIsOut(Vision.VNVideoProcessor.analyzeWithTimeRange_error_, 1)

        self.assertResultIsBOOL(Vision.VNVideoProcessor.analyzeTimeRange_error_)
        self.assertArgIsOut(Vision.VNVideoProcessor.analyzeTimeRange_error_, 1)
