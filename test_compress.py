"""
Unit tests for the video compression library
"""

import unittest
from compress import (
    VideoCompressor, VideoCodec, CompressionPreset, 
    CompressionSettings, get_vvc_advantages, get_omega_advantages
)


class TestVideoCodec(unittest.TestCase):
    """Test VideoCodec enum"""
    
    def test_codec_values(self):
        """Test codec enum values"""
        self.assertEqual(VideoCodec.H264.value, "h264")
        self.assertEqual(VideoCodec.H265.value, "h265")
        self.assertEqual(VideoCodec.AV1.value, "av1")
        self.assertEqual(VideoCodec.VVC.value, "vvc")
        self.assertEqual(VideoCodec.OMEGA.value, "omega")


class TestVideoCompressor(unittest.TestCase):
    """Test VideoCompressor class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.compressor = VideoCompressor()
    
    def test_initialization(self):
        """Test compressor initialization"""
        self.assertIsNotNone(self.compressor.codecs)
        self.assertEqual(len(self.compressor.codecs), 5)
    
    def test_get_codec_info(self):
        """Test getting codec information"""
        vvc_info = self.compressor.get_codec_info(VideoCodec.VVC)
        self.assertEqual(vvc_info.name, "VVC/H.266")
        self.assertEqual(vvc_info.max_resolution, "16K")
        self.assertEqual(vvc_info.compression_efficiency, 2.5)
        self.assertTrue(vvc_info.hdr_support)
    
    def test_compare_codecs(self):
        """Test codec comparison"""
        comparison = self.compressor.compare_codecs()
        self.assertEqual(len(comparison), 5)
        self.assertIn("vvc", comparison)
        self.assertIn("h264", comparison)
        self.assertIn("h265", comparison)
        self.assertIn("av1", comparison)
        self.assertIn("omega", comparison)
    
    def test_get_recommended_codec_8k_hdr(self):
        """Test codec recommendation for 8K HDR"""
        recommended = self.compressor.get_recommended_codec(
            target_resolution="8K",
            require_hdr=True,
            computational_limit="high"
        )
        self.assertEqual(recommended, VideoCodec.OMEGA)
    
    def test_get_recommended_codec_low_complexity(self):
        """Test codec recommendation for low complexity"""
        recommended = self.compressor.get_recommended_codec(
            target_resolution="1080p",
            require_hdr=False,
            computational_limit="low"
        )
        self.assertEqual(recommended, VideoCodec.H264)
    
    def test_create_compression_settings_vvc(self):
        """Test creating VVC compression settings"""
        settings = self.compressor.create_compression_settings(
            codec=VideoCodec.VVC,
            quality="high",
            target_resolution=(3840, 2160)
        )
        self.assertEqual(settings.codec, VideoCodec.VVC)
        self.assertEqual(settings.crf, 18)
        self.assertEqual(settings.resolution, (3840, 2160))
        self.assertEqual(settings.bit_depth, 10)
        self.assertTrue(settings.enable_hdr)
        self.assertTrue(settings.enable_temporal_layers)
    
    def test_create_compression_settings_h264(self):
        """Test creating H.264 compression settings"""
        settings = self.compressor.create_compression_settings(
            codec=VideoCodec.H264,
            quality="medium"
        )
        self.assertEqual(settings.codec, VideoCodec.H264)
        self.assertEqual(settings.crf, 23)
        self.assertEqual(settings.bit_depth, 8)
        self.assertFalse(settings.enable_hdr)
    
    def test_estimate_compression_ratio_vvc(self):
        """Test compression ratio estimation for VVC"""
        settings = CompressionSettings(
            codec=VideoCodec.VVC,
            preset=CompressionPreset.MEDIUM,
            crf=23,
            bit_depth=10,
            enable_temporal_layers=True,
            enable_spatial_layers=True
        )
        ratio = self.compressor.estimate_compression_ratio(settings)
        self.assertGreater(ratio, 2.0)  # Should be better than H.264
    
    def test_estimate_compression_ratio_h264(self):
        """Test compression ratio estimation for H.264"""
        settings = CompressionSettings(
            codec=VideoCodec.H264,
            preset=CompressionPreset.MEDIUM,
            crf=23,
            bit_depth=8
        )
        ratio = self.compressor.estimate_compression_ratio(settings)
        self.assertAlmostEqual(ratio, 1.0, delta=0.3)
    
    def test_encoding_complexity_score_vvc(self):
        """Test encoding complexity score for VVC"""
        settings = CompressionSettings(
            codec=VideoCodec.VVC,
            preset=CompressionPreset.SLOW,
            crf=18
        )
        complexity = self.compressor.get_encoding_complexity_score(settings)
        self.assertGreaterEqual(complexity, 8)  # VVC is very complex
    
    def test_encoding_complexity_score_h264_fast(self):
        """Test encoding complexity score for H.264 fast preset"""
        settings = CompressionSettings(
            codec=VideoCodec.H264,
            preset=CompressionPreset.ULTRAFAST,
            crf=23
        )
        complexity = self.compressor.get_encoding_complexity_score(settings)
        self.assertLessEqual(complexity, 3)  # Should be very low
    
    def test_validate_settings_valid_vvc(self):
        """Test validation of valid VVC settings"""
        settings = CompressionSettings(
            codec=VideoCodec.VVC,
            preset=CompressionPreset.MEDIUM,
            crf=20,
            bit_depth=10,
            enable_hdr=True,
            enable_spatial_layers=True
        )
        valid, errors = self.compressor.validate_settings(settings)
        self.assertTrue(valid)
        self.assertEqual(len(errors), 0)
    
    def test_validate_settings_invalid_bit_depth(self):
        """Test validation with invalid bit depth"""
        settings = CompressionSettings(
            codec=VideoCodec.H264,
            preset=CompressionPreset.MEDIUM,
            crf=20,
            bit_depth=10  # H.264 only supports 8-bit
        )
        valid, errors = self.compressor.validate_settings(settings)
        self.assertFalse(valid)
        self.assertGreater(len(errors), 0)
    
    def test_validate_settings_invalid_hdr(self):
        """Test validation with invalid HDR setting"""
        settings = CompressionSettings(
            codec=VideoCodec.H264,
            preset=CompressionPreset.MEDIUM,
            crf=20,
            bit_depth=8,
            enable_hdr=True  # H.264 doesn't support HDR
        )
        valid, errors = self.compressor.validate_settings(settings)
        self.assertFalse(valid)
        self.assertGreater(len(errors), 0)
    
    def test_validate_settings_invalid_crf(self):
        """Test validation with invalid CRF"""
        settings = CompressionSettings(
            codec=VideoCodec.VVC,
            preset=CompressionPreset.MEDIUM,
            crf=60  # CRF must be 0-51
        )
        valid, errors = self.compressor.validate_settings(settings)
        self.assertFalse(valid)
        self.assertGreater(len(errors), 0)
    
    def test_validate_settings_spatial_layers_non_vvc_omega(self):
        """Test validation of spatial layers with non-VVC/OMEGA codec"""
        settings = CompressionSettings(
            codec=VideoCodec.H265,
            preset=CompressionPreset.MEDIUM,
            crf=20,
            enable_spatial_layers=True  # Only VVC and OMEGA support this
        )
        valid, errors = self.compressor.validate_settings(settings)
        self.assertFalse(valid)
        self.assertGreater(len(errors), 0)
    
    def test_generate_encoding_command_vvc(self):
        """Test encoding command generation for VVC"""
        settings = CompressionSettings(
            codec=VideoCodec.VVC,
            preset=CompressionPreset.MEDIUM,
            crf=18,
            resolution=(3840, 2160),
            framerate=30,
            bit_depth=10
        )
        cmd = self.compressor.generate_encoding_command(
            settings, "input.mp4", "output.vvc"
        )
        self.assertIn("ffmpeg", cmd)
        self.assertIn("libvvenc", cmd)
        self.assertIn("-crf 18", cmd)
        self.assertIn("-s 3840x2160", cmd)
        self.assertIn("-r 30", cmd)
        self.assertIn("yuv420p10le", cmd)
        self.assertIn("vvenc-params", cmd)
    
    def test_generate_encoding_command_h264(self):
        """Test encoding command generation for H.264"""
        settings = CompressionSettings(
            codec=VideoCodec.H264,
            preset=CompressionPreset.FAST,
            crf=23
        )
        cmd = self.compressor.generate_encoding_command(
            settings, "input.mp4", "output.mp4"
        )
        self.assertIn("libx264", cmd)
        self.assertIn("-crf 23", cmd)
        self.assertIn("fast", cmd)
    
    def test_export_settings(self):
        """Test settings export to JSON"""
        settings = CompressionSettings(
            codec=VideoCodec.VVC,
            preset=CompressionPreset.SLOW,
            crf=18,
            resolution=(3840, 2160),
            bit_depth=10
        )
        json_str = self.compressor.export_settings(settings)
        self.assertIn('"codec": "vvc"', json_str)
        self.assertIn('"crf": 18', json_str)
        self.assertIn('"bit_depth": 10', json_str)


class TestVVCAdvantages(unittest.TestCase):
    """Test VVC advantages function"""
    
    def test_get_vvc_advantages(self):
        """Test getting VVC advantages"""
        advantages = get_vvc_advantages()
        self.assertIsInstance(advantages, list)
        self.assertGreater(len(advantages), 10)
        # Check for key advantages
        self.assertTrue(any("50%" in adv for adv in advantages))
        self.assertTrue(any("16K" in adv for adv in advantages))
        self.assertTrue(any("affine" in adv.lower() for adv in advantages))


class TestOMEGAAdvantages(unittest.TestCase):
    """Test OMEGA advantages function"""
    
    def test_get_omega_advantages(self):
        """Test getting OMEGA advantages"""
        advantages = get_omega_advantages()
        self.assertIsInstance(advantages, list)
        self.assertGreater(len(advantages), 20)
        # Check for key advantages
        self.assertTrue(any("75%" in adv for adv in advantages))
        self.assertTrue(any("32K" in adv for adv in advantages))
        self.assertTrue(any("AI" in adv or "neural" in adv.lower() for adv in advantages))


class TestOMEGAEncoder(unittest.TestCase):
    """Test OMEGA encoder functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.compressor = VideoCompressor()
    
    def test_omega_encoder_availability(self):
        """Test OMEGA encoder availability check"""
        available = self.compressor.is_omega_encoder_available()
        self.assertIsInstance(available, bool)
        # With numpy installed, it should be available
        self.assertTrue(available, "OMEGA encoder should be available with numpy")
    
    def test_get_omega_encoder(self):
        """Test getting OMEGA encoder instance"""
        if not self.compressor.is_omega_encoder_available():
            self.skipTest("OMEGA encoder not available")
        
        encoder = self.compressor.get_omega_encoder(320, 240, fps=30, quality=20)
        self.assertIsNotNone(encoder)
        self.assertEqual(encoder.width, 320)
        self.assertEqual(encoder.height, 240)
        self.assertEqual(encoder.fps, 30)
        self.assertEqual(encoder.quality, 20)
    
    def test_omega_encoder_basic_compression(self):
        """Test basic OMEGA compression functionality"""
        if not self.compressor.is_omega_encoder_available():
            self.skipTest("OMEGA encoder not available")
        
        try:
            import numpy as np
            
            # Create test frame
            width, height = 160, 120
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            frame[:, :, 0] = 128
            
            # Get encoder
            encoder = self.compressor.get_omega_encoder(width, height, quality=20)
            
            # Encode
            compressed = encoder.encode_frame(frame, is_keyframe=True)
            self.assertIsInstance(compressed, bytes)
            self.assertGreater(len(compressed), 0)
            
            # Decode
            decoded = encoder.decode_frame(compressed)
            self.assertEqual(decoded.shape, (height, width, 3))
            
            # Check compression happened
            compression_ratio = frame.nbytes / len(compressed)
            self.assertGreater(compression_ratio, 1.0, "Should achieve compression")
            
        except ImportError:
            self.skipTest("Numpy not available")


class TestCodecCapabilities(unittest.TestCase):
    """Test codec capabilities"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.compressor = VideoCompressor()
    
    def test_vvc_capabilities(self):
        """Test VVC/H.266 capabilities"""
        caps = self.compressor.get_codec_info(VideoCodec.VVC)
        self.assertEqual(caps.max_resolution, "16K")
        self.assertIn(8, caps.bit_depth_support)
        self.assertIn(10, caps.bit_depth_support)
        self.assertIn(12, caps.bit_depth_support)
        self.assertIn(14, caps.bit_depth_support)
        self.assertIn(16, caps.bit_depth_support)
        self.assertEqual(caps.compression_efficiency, 2.5)
        self.assertTrue(caps.hdr_support)
        self.assertTrue(caps.streaming_optimized)
        self.assertGreater(len(caps.advanced_features), 15)
    
    def test_omega_capabilities(self):
        """Test OMEGA codec capabilities"""
        caps = self.compressor.get_codec_info(VideoCodec.OMEGA)
        self.assertEqual(caps.max_resolution, "32K+")
        self.assertIn(8, caps.bit_depth_support)
        self.assertIn(10, caps.bit_depth_support)
        self.assertIn(12, caps.bit_depth_support)
        self.assertIn(16, caps.bit_depth_support)
        self.assertIn(20, caps.bit_depth_support)
        self.assertIn(24, caps.bit_depth_support)
        self.assertEqual(caps.compression_efficiency, 4.0)
        self.assertTrue(caps.hdr_support)
        self.assertTrue(caps.streaming_optimized)
        self.assertGreater(len(caps.advanced_features), 20)
    
    def test_h265_capabilities(self):
        """Test H.265/HEVC capabilities"""
        caps = self.compressor.get_codec_info(VideoCodec.H265)
        self.assertEqual(caps.max_resolution, "8K")
        self.assertIn(8, caps.bit_depth_support)
        self.assertIn(10, caps.bit_depth_support)
        self.assertEqual(caps.compression_efficiency, 2.0)
        self.assertTrue(caps.hdr_support)
    
    def test_av1_capabilities(self):
        """Test AV1 capabilities"""
        caps = self.compressor.get_codec_info(VideoCodec.AV1)
        self.assertEqual(caps.max_resolution, "8K+")
        self.assertEqual(caps.compression_efficiency, 2.2)
        self.assertTrue(caps.hdr_support)
        self.assertIn("Film grain synthesis", caps.advanced_features)
    
    def test_h264_capabilities(self):
        """Test H.264/AVC capabilities"""
        caps = self.compressor.get_codec_info(VideoCodec.H264)
        self.assertEqual(caps.max_resolution, "4K")
        self.assertEqual(caps.bit_depth_support, [8])
        self.assertEqual(caps.compression_efficiency, 1.0)
        self.assertFalse(caps.hdr_support)
    
    def test_omega_is_most_efficient(self):
        """Test that OMEGA has the highest compression efficiency"""
        codecs = self.compressor.compare_codecs()
        omega_efficiency = codecs["omega"].compression_efficiency
        
        for codec_name, caps in codecs.items():
            if codec_name != "omega":
                self.assertGreater(omega_efficiency, caps.compression_efficiency,
                                 f"OMEGA should be more efficient than {codec_name}")
    
    def test_omega_highest_resolution_support(self):
        """Test that OMEGA supports the highest resolution"""
        omega_caps = self.compressor.get_codec_info(VideoCodec.OMEGA)
        vvc_caps = self.compressor.get_codec_info(VideoCodec.VVC)
        h265_caps = self.compressor.get_codec_info(VideoCodec.H265)
        
        self.assertEqual(omega_caps.max_resolution, "32K+")
        self.assertEqual(vvc_caps.max_resolution, "16K")
        self.assertEqual(h265_caps.max_resolution, "8K")
    
    def test_omega_most_advanced_features(self):
        """Test that OMEGA has the most advanced features"""
        codecs = self.compressor.compare_codecs()
        omega_features = len(codecs["omega"].advanced_features)
        
        for codec_name, caps in codecs.items():
            if codec_name != "omega":
                self.assertGreater(omega_features, len(caps.advanced_features),
                                 f"OMEGA should have more features than {codec_name}")


class TestCompressionSettings(unittest.TestCase):
    """Test CompressionSettings dataclass"""
    
    def test_default_settings(self):
        """Test default compression settings"""
        settings = CompressionSettings(
            codec=VideoCodec.VVC,
            preset=CompressionPreset.MEDIUM,
            crf=23
        )
        self.assertEqual(settings.codec, VideoCodec.VVC)
        self.assertEqual(settings.crf, 23)
        self.assertIsNone(settings.bitrate)
        self.assertEqual(settings.bit_depth, 8)
    
    def test_custom_settings(self):
        """Test custom compression settings"""
        settings = CompressionSettings(
            codec=VideoCodec.VVC,
            preset=CompressionPreset.VERYSLOW,
            crf=15,
            bitrate=10000,
            resolution=(7680, 4320),
            framerate=60,
            bit_depth=12,
            enable_hdr=True,
            enable_temporal_layers=True,
            enable_spatial_layers=True,
            tile_columns=4,
            tile_rows=2
        )
        self.assertEqual(settings.bitrate, 10000)
        self.assertEqual(settings.resolution, (7680, 4320))
        self.assertEqual(settings.framerate, 60)
        self.assertEqual(settings.bit_depth, 12)
        self.assertTrue(settings.enable_hdr)
        self.assertTrue(settings.enable_spatial_layers)
        self.assertEqual(settings.tile_columns, 4)


if __name__ == "__main__":
    unittest.main()
