from PyObjCTools.TestSupport import TestCase

import MetalPerformanceShadersGraph


class TestMPSGraphCore(TestCase):
    def test_methods(self):
        self.assertResultIsBOOL(
            MetalPerformanceShadersGraph.MPSGraphShapedType.isEqualTo_
        )

    def test_constants(self):
        self.assertEqual(
            MetalPerformanceShadersGraph.MPSGraphTensorNamedDataLayoutNCHW, 0
        )
        self.assertEqual(
            MetalPerformanceShadersGraph.MPSGraphTensorNamedDataLayoutNHWC, 1
        )
        self.assertEqual(
            MetalPerformanceShadersGraph.MPSGraphTensorNamedDataLayoutOIHW, 2
        )
        self.assertEqual(
            MetalPerformanceShadersGraph.MPSGraphTensorNamedDataLayoutHWIO, 3
        )
        self.assertEqual(
            MetalPerformanceShadersGraph.MPSGraphTensorNamedDataLayoutCHW, 4
        )
        self.assertEqual(
            MetalPerformanceShadersGraph.MPSGraphTensorNamedDataLayoutHWC, 5
        )
        self.assertEqual(
            MetalPerformanceShadersGraph.MPSGraphTensorNamedDataLayoutHW, 6
        )

        self.assertEqual(MetalPerformanceShadersGraph.MPSGraphPaddingStyleExplicit, 0)
        self.assertEqual(MetalPerformanceShadersGraph.MPSGraphPaddingStyleTF_VALID, 1)
        self.assertEqual(MetalPerformanceShadersGraph.MPSGraphPaddingStyleTF_SAME, 2)

        self.assertEqual(MetalPerformanceShadersGraph.MPSGraphPaddingModeConstant, 0)
        self.assertEqual(MetalPerformanceShadersGraph.MPSGraphPaddingModeReflect, 1)
        self.assertEqual(MetalPerformanceShadersGraph.MPSGraphPaddingModeSymmetric, 2)
