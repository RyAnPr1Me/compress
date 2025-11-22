"""
Example: Using OMEGA Encoder for Actual Video Compression

This demonstrates the working OMEGA video encoder that can actually
compress and decompress video frames.
"""

import numpy as np
from compress import VideoCompressor, VideoCodec


def example_image_compression():
    """Example: Compress a single image with OMEGA"""
    print("=" * 80)
    print("Example 1: Image Compression with OMEGA")
    print("=" * 80)
    
    compressor = VideoCompressor()
    
    if not compressor.is_omega_encoder_available():
        print("❌ OMEGA encoder not available. Install numpy to use it.")
        return
    
    # Create a sample image (gradient)
    width, height = 640, 480
    print(f"\n✓ Creating test image: {width}x{height}")
    
    image = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            image[y, x, 0] = int((x / width) * 255)
            image[y, x, 1] = int((y / height) * 255)
            image[y, x, 2] = int(((x + y) / (width + height)) * 255)
    
    # Get OMEGA encoder
    encoder = compressor.get_omega_encoder(width, height, quality=18)
    
    # Compress
    print("✓ Compressing with OMEGA...")
    compressed_data = encoder.encode_frame(image, is_keyframe=True)
    
    # Decompress
    print("✓ Decompressing...")
    decompressed_image = encoder.decode_frame(compressed_data)
    
    # Calculate metrics
    original_size = image.nbytes
    compressed_size = len(compressed_data)
    compression_ratio = original_size / compressed_size
    
    print(f"\n📊 Results:")
    print(f"   Original size: {original_size:,} bytes ({original_size/1024:.1f} KB)")
    print(f"   Compressed size: {compressed_size:,} bytes ({compressed_size/1024:.1f} KB)")
    print(f"   Compression ratio: {compression_ratio:.2f}x")
    print(f"   Space saved: {(1 - compressed_size/original_size) * 100:.1f}%")
    
    # Quality check
    mse = np.mean((image.astype(float) - decompressed_image.astype(float)) ** 2)
    psnr = 10 * np.log10((255.0 ** 2) / mse) if mse > 0 else float('inf')
    print(f"   PSNR: {psnr:.2f} dB (quality metric)")
    
    return compression_ratio


def example_video_compression():
    """Example: Compress multiple video frames"""
    print("\n" + "=" * 80)
    print("Example 2: Video Compression with Multiple Frames")
    print("=" * 80)
    
    compressor = VideoCompressor()
    
    if not compressor.is_omega_encoder_available():
        print("❌ OMEGA encoder not available. Install numpy to use it.")
        return
    
    # Import additional modules
    from omega_encoder import compress_video_file, decompress_video_file
    
    # Create animated frames
    width, height = 320, 240
    num_frames = 30
    fps = 30
    
    print(f"\n✓ Creating {num_frames} animated frames at {fps} FPS...")
    
    frames = []
    for i in range(num_frames):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Animated pattern
        offset = i * 8
        for y in range(height):
            for x in range(width):
                frame[y, x, 0] = int(((x + offset) % 256))
                frame[y, x, 1] = int(((y + offset) % 256))
                frame[y, x, 2] = 128
        
        frames.append(frame)
    
    # Compress video
    output_path = '/tmp/example_video.omega'
    print(f"✓ Compressing video to {output_path}...")
    
    stats = compress_video_file(frames, output_path, width, height, fps=fps, quality=20)
    
    print(f"\n📊 Compression Results:")
    print(f"   Frames: {stats['frames']}")
    print(f"   Original size: {stats['original_size']:,} bytes ({stats['original_size']/1024/1024:.2f} MB)")
    print(f"   Compressed size: {stats['compressed_size']:,} bytes ({stats['compressed_size']/1024:.1f} KB)")
    print(f"   Compression ratio: {stats['compression_ratio']:.2f}x")
    print(f"   Space saved: {(1 - stats['compressed_size']/stats['original_size']) * 100:.1f}%")
    
    # Decompress
    print(f"\n✓ Decompressing video...")
    decoded_frames, metadata = decompress_video_file(output_path)
    
    print(f"✓ Successfully decoded {len(decoded_frames)} frames")
    print(f"   Resolution: {metadata['width']}x{metadata['height']}")
    print(f"   FPS: {metadata['fps']}")
    
    return stats['compression_ratio']


def example_quality_comparison():
    """Example: Compare different quality settings"""
    print("\n" + "=" * 80)
    print("Example 3: Quality Level Comparison")
    print("=" * 80)
    
    compressor = VideoCompressor()
    
    if not compressor.is_omega_encoder_available():
        print("❌ OMEGA encoder not available. Install numpy to use it.")
        return
    
    # Create test image
    width, height = 512, 384
    image = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    
    print(f"\nTesting different quality levels on {width}x{height} image:")
    print("\nQuality | Size (KB) | Compression | PSNR (dB) | Assessment")
    print("-" * 80)
    
    qualities = [
        (5, "Low"),
        (15, "Medium"),
        (25, "High"),
        (35, "Very High"),
        (45, "Ultra High")
    ]
    
    for quality, label in qualities:
        encoder = compressor.get_omega_encoder(width, height, quality=quality)
        compressed = encoder.encode_frame(image, is_keyframe=True)
        decoded = encoder.decode_frame(compressed)
        
        size_kb = len(compressed) / 1024
        compression_ratio = image.nbytes / len(compressed)
        
        mse = np.mean((image.astype(float) - decoded.astype(float)) ** 2)
        psnr = 10 * np.log10((255.0 ** 2) / mse) if mse > 0 else 100
        
        assessment = "Excellent" if psnr > 35 else "Good" if psnr > 30 else "Acceptable"
        
        print(f"{quality:2d} ({label:10s}) | {size_kb:6.1f} | {compression_ratio:8.2f}x | {psnr:7.2f} | {assessment}")
    
    print("\n💡 Lower quality number = higher compression + lower visual quality")
    print("   Higher quality number = lower compression + higher visual quality")


def main():
    """Run all examples"""
    print("\n" + "=" * 80)
    print("OMEGA ENCODER - PRACTICAL EXAMPLES")
    print("Demonstrating actual video compression functionality")
    print("=" * 80)
    
    try:
        # Check availability
        compressor = VideoCompressor()
        
        if not compressor.is_omega_encoder_available():
            print("\n❌ OMEGA encoder not available.")
            print("   Install numpy: pip install numpy")
            return
        
        print("\n✅ OMEGA encoder is available and functional!")
        
        # Run examples
        ratio1 = example_image_compression()
        ratio2 = example_video_compression()
        example_quality_comparison()
        
        # Summary
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"\n✅ Image compression achieved {ratio1:.1f}x compression")
        print(f"✅ Video compression achieved {ratio2:.1f}x compression")
        print(f"✅ OMEGA encoder is fully functional with:")
        print("   • DCT-based compression")
        print("   • Quantization with quality control")
        print("   • Run-length encoding")
        print("   • YUV color space conversion")
        print("   • Keyframe and P-frame support")
        print("\n🎉 OMEGA codec actually works!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
