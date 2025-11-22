"""
Examples demonstrating the video compression library
"""

from compress import (
    VideoCompressor, VideoCodec, CompressionPreset,
    CompressionSettings, get_vvc_advantages
)


def example_basic_vvc_encoding():
    """Example: Basic VVC encoding setup"""
    print("\n" + "=" * 80)
    print("Example 1: Basic VVC Encoding for 4K Content")
    print("=" * 80)
    
    compressor = VideoCompressor()
    
    # Create settings for high-quality 4K VVC encoding
    settings = compressor.create_compression_settings(
        codec=VideoCodec.VVC,
        quality="high",
        target_resolution=(3840, 2160)
    )
    
    print(f"\nCodec: {settings.codec.value.upper()}")
    print(f"Preset: {settings.preset.value}")
    print(f"CRF: {settings.crf}")
    print(f"Resolution: {settings.resolution}")
    print(f"Bit Depth: {settings.bit_depth}")
    print(f"HDR Enabled: {settings.enable_hdr}")
    
    # Validate and estimate
    valid, errors = compressor.validate_settings(settings)
    print(f"\nSettings Valid: {valid}")
    
    compression_ratio = compressor.estimate_compression_ratio(settings)
    print(f"Estimated Compression: {compression_ratio:.2f}x vs H.264")
    
    complexity = compressor.get_encoding_complexity_score(settings)
    print(f"Encoding Complexity: {complexity}/10")


def example_codec_comparison():
    """Example: Compare all codecs"""
    print("\n" + "=" * 80)
    print("Example 2: Codec Comparison")
    print("=" * 80)
    
    compressor = VideoCompressor()
    codecs = compressor.compare_codecs()
    
    print("\n{:<15} {:<15} {:<15} {:<12}".format(
        "Codec", "Max Resolution", "Efficiency", "HDR Support"
    ))
    print("-" * 80)
    
    for codec_name, caps in sorted(codecs.items()):
        print("{:<15} {:<15} {:<15} {:<12}".format(
            caps.name,
            caps.max_resolution,
            f"{caps.compression_efficiency}x",
            "Yes" if caps.hdr_support else "No"
        ))


def example_advanced_vvc_settings():
    """Example: Advanced VVC settings for professional use"""
    print("\n" + "=" * 80)
    print("Example 3: Advanced VVC Settings for 8K Professional Content")
    print("=" * 80)
    
    compressor = VideoCompressor()
    
    # Professional 8K settings with all VVC features enabled
    settings = CompressionSettings(
        codec=VideoCodec.VVC,
        preset=CompressionPreset.VERYSLOW,  # Best quality
        crf=15,  # Very high quality
        resolution=(7680, 4320),  # 8K
        framerate=60,
        bit_depth=12,  # Professional bit depth
        enable_hdr=True,
        enable_temporal_layers=True,
        enable_spatial_layers=True,  # VVC-exclusive
        tile_columns=4,
        tile_rows=2
    )
    
    print("\nConfiguration:")
    print(compressor.export_settings(settings))
    
    # Validate
    valid, errors = compressor.validate_settings(settings)
    print(f"\nValidation: {'Passed' if valid else 'Failed'}")
    if errors:
        for error in errors:
            print(f"  - {error}")
    
    # Generate encoding command
    cmd = compressor.generate_encoding_command(
        settings, 
        "input_8k.mov", 
        "output_8k.vvc"
    )
    print("\nEncoding Command:")
    print(cmd)


def example_streaming_optimization():
    """Example: Optimized settings for streaming"""
    print("\n" + "=" * 80)
    print("Example 4: Streaming-Optimized VVC Encoding")
    print("=" * 80)
    
    compressor = VideoCompressor()
    
    # Settings optimized for adaptive streaming
    resolutions = [
        (1920, 1080, "1080p"),
        (2560, 1440, "1440p"),
        (3840, 2160, "4K")
    ]
    
    print("\nMulti-resolution streaming ladder:")
    print("-" * 80)
    
    for width, height, label in resolutions:
        settings = CompressionSettings(
            codec=VideoCodec.VVC,
            preset=CompressionPreset.FAST,  # Faster for streaming
            crf=23,
            resolution=(width, height),
            framerate=30,
            bit_depth=10,
            enable_hdr=True,
            enable_temporal_layers=True,  # Important for streaming
            tile_columns=2,
            tile_rows=1
        )
        
        ratio = compressor.estimate_compression_ratio(settings)
        bitrate_estimate = int((width * height * 30 * 0.1) / ratio)  # Rough estimate
        
        print(f"\n{label} ({width}x{height}):")
        print(f"  Compression: {ratio:.2f}x")
        print(f"  Estimated bitrate: ~{bitrate_estimate} kbps")
        print(f"  Complexity: {compressor.get_encoding_complexity_score(settings)}/10")


def example_codec_recommendation():
    """Example: Get codec recommendations"""
    print("\n" + "=" * 80)
    print("Example 5: Codec Recommendations for Different Scenarios")
    print("=" * 80)
    
    compressor = VideoCompressor()
    
    scenarios = [
        {
            "name": "8K HDR Cinema",
            "resolution": "8K",
            "hdr": True,
            "complexity": "high"
        },
        {
            "name": "4K Streaming",
            "resolution": "4K",
            "hdr": True,
            "complexity": "high"
        },
        {
            "name": "HD Mobile Video",
            "resolution": "1080p",
            "hdr": False,
            "complexity": "low"
        },
        {
            "name": "16K Future Content",
            "resolution": "16K",
            "hdr": True,
            "complexity": "high"
        }
    ]
    
    print()
    for scenario in scenarios:
        recommended = compressor.get_recommended_codec(
            target_resolution=scenario["resolution"],
            require_hdr=scenario["hdr"],
            computational_limit=scenario["complexity"]
        )
        codec_info = compressor.get_codec_info(recommended)
        
        print(f"{scenario['name']}:")
        print(f"  Recommended: {codec_info.name}")
        print(f"  Efficiency: {codec_info.compression_efficiency}x vs H.264")
        print()


def example_batch_encoding_comparison():
    """Example: Compare encoding settings across codecs"""
    print("\n" + "=" * 80)
    print("Example 6: Batch Encoding Comparison (Same Settings)")
    print("=" * 80)
    
    compressor = VideoCompressor()
    
    # Same settings for all codecs (where supported)
    base_settings = {
        "preset": CompressionPreset.MEDIUM,
        "crf": 23,
        "resolution": (1920, 1080),
        "framerate": 30
    }
    
    print("\nComparison for 1080p30 content:")
    print("-" * 80)
    print("{:<12} {:<15} {:<15} {:<15}".format(
        "Codec", "Compression", "Complexity", "Bit Depth"
    ))
    print("-" * 80)
    
    for codec in [VideoCodec.H264, VideoCodec.H265, VideoCodec.AV1, VideoCodec.VVC]:
        # Adjust bit depth based on codec support
        bit_depth = 8 if codec == VideoCodec.H264 else 10
        
        settings = CompressionSettings(
            codec=codec,
            bit_depth=bit_depth,
            **base_settings
        )
        
        valid, _ = compressor.validate_settings(settings)
        if valid:
            ratio = compressor.estimate_compression_ratio(settings)
            complexity = compressor.get_encoding_complexity_score(settings)
            codec_info = compressor.get_codec_info(codec)
            
            print("{:<12} {:<15} {:<15} {:<15}".format(
                codec_info.name,
                f"{ratio:.2f}x",
                f"{complexity}/10",
                f"{bit_depth}-bit"
            ))


def example_vvc_advantages():
    """Example: Display VVC advantages"""
    print("\n" + "=" * 80)
    print("Example 7: Why VVC/H.266 is More Advanced")
    print("=" * 80)
    
    advantages = get_vvc_advantages()
    
    print("\nKey advantages of VVC/H.266:")
    print("-" * 80)
    
    categories = {
        "Compression": [],
        "Resolution": [],
        "Quality": [],
        "Features": [],
        "Content Types": []
    }
    
    # Categorize advantages
    for adv in advantages:
        if "bitrate" in adv.lower() or "compression" in adv.lower():
            categories["Compression"].append(adv)
        elif "resolution" in adv.lower() or "16k" in adv.lower() or "8k" in adv.lower():
            categories["Resolution"].append(adv)
        elif "bit depth" in adv.lower() or "hdr" in adv.lower() or "quality" in adv.lower():
            categories["Quality"].append(adv)
        elif "360" in adv.lower() or "screen" in adv.lower() or "streaming" in adv.lower():
            categories["Content Types"].append(adv)
        else:
            categories["Features"].append(adv)
    
    for category, items in categories.items():
        if items:
            print(f"\n{category}:")
            for item in items:
                print(f"  • {item}")


def example_quality_ladder():
    """Example: Quality ladder for same content"""
    print("\n" + "=" * 80)
    print("Example 8: VVC Quality Ladder (4K Content)")
    print("=" * 80)
    
    compressor = VideoCompressor()
    
    quality_levels = [
        ("highest", 15, "Archive/Master"),
        ("high", 18, "Professional"),
        ("medium", 23, "High-quality Streaming"),
        ("low", 28, "Standard Streaming")
    ]
    
    print("\nQuality ladder for 4K VVC encoding:")
    print("-" * 80)
    print("{:<20} {:<8} {:<15} {:<15}".format(
        "Use Case", "CRF", "Compression", "File Size*"
    ))
    print("-" * 80)
    
    base_size = 10000  # MB, hypothetical
    
    for quality, crf, use_case in quality_levels:
        settings = compressor.create_compression_settings(
            codec=VideoCodec.VVC,
            quality=quality,
            target_resolution=(3840, 2160)
        )
        
        ratio = compressor.estimate_compression_ratio(settings)
        estimated_size = int(base_size / ratio)
        
        print("{:<20} {:<8} {:<15} {:<15}".format(
            use_case,
            crf,
            f"{ratio:.2f}x",
            f"~{estimated_size} MB"
        ))
    
    print("\n* Relative to uncompressed 4K source")


def main():
    """Run all examples"""
    print("\n" + "=" * 80)
    print("VIDEO COMPRESSION LIBRARY - VVC/H.266 EXAMPLES")
    print("=" * 80)
    print("\nThis library supports VVC/H.266, the most advanced video codec,")
    print("offering up to 50% bitrate savings compared to H.265/HEVC")
    print("and 40% savings compared to AV1.")
    
    examples = [
        example_basic_vvc_encoding,
        example_codec_comparison,
        example_advanced_vvc_settings,
        example_streaming_optimization,
        example_codec_recommendation,
        example_batch_encoding_comparison,
        example_vvc_advantages,
        example_quality_ladder
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\nError in {example.__name__}: {e}")
    
    print("\n" + "=" * 80)
    print("Examples completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()
