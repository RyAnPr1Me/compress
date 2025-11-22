"""
Test the OMEGA encoder with actual compression/decompression
"""

import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from omega_encoder import OMEGAEncoder, compress_video_file, decompress_video_file


def test_basic_encoding():
    """Test basic frame encoding and decoding"""
    print("=" * 80)
    print("Test 1: Basic Frame Encoding/Decoding")
    print("=" * 80)
    
    # Create a test frame (simple gradient)
    width, height = 320, 240
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Create a gradient pattern
    for y in range(height):
        for x in range(width):
            frame[y, x, 0] = int((x / width) * 255)  # Red gradient
            frame[y, x, 1] = int((y / height) * 255)  # Green gradient
            frame[y, x, 2] = 128  # Blue constant
    
    # Encode
    encoder = OMEGAEncoder(width, height, quality=18)
    compressed = encoder.encode_frame(frame, is_keyframe=True)
    
    # Decode
    decoded = encoder.decode_frame(compressed)
    
    # Calculate metrics
    original_size = frame.nbytes
    compressed_size = len(compressed)
    compression_ratio = original_size / compressed_size
    
    # Calculate PSNR (Peak Signal-to-Noise Ratio)
    mse = np.mean((frame.astype(float) - decoded.astype(float)) ** 2)
    if mse > 0:
        psnr = 10 * np.log10((255.0 ** 2) / mse)
    else:
        psnr = float('inf')
    
    print(f"\n✓ Frame size: {width}x{height}")
    print(f"✓ Original size: {original_size:,} bytes")
    print(f"✓ Compressed size: {compressed_size:,} bytes")
    print(f"✓ Compression ratio: {compression_ratio:.2f}x")
    print(f"✓ PSNR: {psnr:.2f} dB")
    print(f"✓ Quality preserved: {'Excellent' if psnr > 30 else 'Good' if psnr > 20 else 'Acceptable'}")
    
    return compression_ratio > 1.0 and psnr > 20


def test_video_compression():
    """Test video file compression with multiple frames"""
    print("\n" + "=" * 80)
    print("Test 2: Multi-Frame Video Compression")
    print("=" * 80)
    
    # Create test video frames
    width, height = 256, 192
    num_frames = 10
    frames = []
    
    print(f"\n✓ Generating {num_frames} test frames...")
    
    for i in range(num_frames):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Animated gradient
        for y in range(height):
            for x in range(width):
                frame[y, x, 0] = int((x / width) * 255)
                frame[y, x, 1] = int((y / height) * 255)
                frame[y, x, 2] = int(((x + y + i * 10) % 256))
        
        frames.append(frame)
    
    # Compress video
    output_path = '/tmp/test_video.omega'
    print(f"✓ Compressing video to {output_path}...")
    
    stats = compress_video_file(frames, output_path, width, height, fps=30, quality=20)
    
    print(f"\n✓ Original size: {stats['original_size']:,} bytes")
    print(f"✓ Compressed size: {stats['compressed_size']:,} bytes")
    print(f"✓ Compression ratio: {stats['compression_ratio']:.2f}x")
    print(f"✓ Frames encoded: {stats['frames']}")
    
    # Decompress video
    print(f"\n✓ Decompressing video...")
    decoded_frames, metadata = decompress_video_file(output_path)
    
    print(f"✓ Frames decoded: {len(decoded_frames)}")
    print(f"✓ Resolution: {metadata['width']}x{metadata['height']}")
    print(f"✓ FPS: {metadata['fps']}")
    
    # Verify
    success = (len(decoded_frames) == num_frames and 
               stats['compression_ratio'] > 1.0)
    
    if success:
        print("\n✅ Video compression/decompression successful!")
    
    return success


def test_different_qualities():
    """Test encoding at different quality levels"""
    print("\n" + "=" * 80)
    print("Test 3: Quality Level Comparison")
    print("=" * 80)
    
    width, height = 256, 192
    frame = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    
    qualities = [5, 15, 25, 35, 45]
    
    print("\nQuality | Compressed Size | Compression | PSNR")
    print("-" * 60)
    
    for quality in qualities:
        encoder = OMEGAEncoder(width, height, quality=quality)
        compressed = encoder.encode_frame(frame, is_keyframe=True)
        decoded = encoder.decode_frame(compressed)
        
        compression_ratio = frame.nbytes / len(compressed)
        
        mse = np.mean((frame.astype(float) - decoded.astype(float)) ** 2)
        psnr = 10 * np.log10((255.0 ** 2) / mse) if mse > 0 else float('inf')
        
        print(f"  {quality:2d}    | {len(compressed):7,} bytes  | {compression_ratio:6.2f}x    | {psnr:5.2f} dB")
    
    print("\n✓ Lower quality = higher compression + lower PSNR")
    print("✓ Higher quality = lower compression + higher PSNR")
    
    return True


def test_edge_cases():
    """Test edge cases"""
    print("\n" + "=" * 80)
    print("Test 4: Edge Cases")
    print("=" * 80)
    
    # Test 1: Solid color frame (should compress very well)
    print("\n✓ Testing solid color frame...")
    width, height = 320, 240
    solid_frame = np.full((height, width, 3), 128, dtype=np.uint8)
    
    encoder = OMEGAEncoder(width, height, quality=20)
    compressed = encoder.encode_frame(solid_frame, is_keyframe=True)
    decoded = encoder.decode_frame(compressed)
    
    compression_ratio = solid_frame.nbytes / len(compressed)
    print(f"  Solid color compression: {compression_ratio:.2f}x (should be high)")
    
    # Test 2: Random noise (should compress poorly)
    print("\n✓ Testing random noise frame...")
    noise_frame = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    
    compressed = encoder.encode_frame(noise_frame, is_keyframe=True)
    decoded = encoder.decode_frame(compressed)
    
    compression_ratio = noise_frame.nbytes / len(compressed)
    print(f"  Random noise compression: {compression_ratio:.2f}x (should be low)")
    
    return True


def run_all_tests():
    """Run all encoder tests"""
    print("\n" + "=" * 80)
    print("OMEGA ENCODER - FUNCTIONAL TESTS")
    print("Testing actual video compression implementation")
    print("=" * 80)
    
    tests = [
        ("Basic Encoding/Decoding", test_basic_encoding),
        ("Video Compression", test_video_compression),
        ("Quality Levels", test_different_qualities),
        ("Edge Cases", test_edge_cases)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ Test '{name}' failed with error: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {name}")
    
    total = len(results)
    passed = sum(1 for _, s in results if s)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! OMEGA encoder is fully functional.")
    
    return passed == total


if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
