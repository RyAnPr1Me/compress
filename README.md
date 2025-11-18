# Advanced Video Compression Library

A comprehensive video compression library with support for the most advanced video codecs, including **VVC/H.266** - the successor to both H.265/HEVC and AV1.

## Features

### Supported Codecs

- **H.264/AVC** - Legacy standard, widely compatible
- **H.265/HEVC** - 2x compression efficiency over H.264
- **AV1** - Royalty-free, 2.2x compression efficiency over H.264
- **VVC/H.266** ⭐ - **Most Advanced** - 2.5x compression efficiency over H.264

### VVC/H.266 - The Most Advanced Codec

VVC (Versatile Video Coding), also known as H.266, is the latest generation video codec that offers:

#### Key Advantages
- **50% bitrate savings** compared to H.265/HEVC
- **40% bitrate savings** compared to AV1
- Support for **up to 16K resolution**
- **16-bit color depth** support
- Enhanced **HDR and wide color gamut** support
- Native **360-degree video** support
- Advanced **screen content coding** tools

#### Advanced Technical Features

**Enhanced Partitioning**
- Quad-tree with multi-type tree structure
- More flexible block partitioning
- Triangle and geometric partitioning modes

**Superior Prediction**
- 67 directional intra prediction modes (vs 35 in HEVC)
- Matrix-based intra prediction (MIP)
- Affine motion compensation for complex motion
- Decoder-side motion vector refinement (DMVR)
- Bi-directional optical flow (BDOF)
- Combined inter/intra prediction (CIIP)

**Advanced Filtering**
- Adaptive loop filter (ALF) with enhanced capabilities
- Sample adaptive offset (SAO)
- Deblocking filter improvements

**Cutting-Edge Transform & Quantization**
- Low-frequency non-separable transform (LFNST)
- Dependent quantization for better perceptual quality
- Multiple transform selection (MTS)
- Block differential pulse-code modulation (BDPCM)

**Other Innovations**
- Reference picture resampling for adaptive streaming
- Subblock-based temporal motion vector prediction (SbTMVP)
- Adaptive color transform
- Enhanced parallel processing capabilities

## Installation

```bash
# Clone the repository
git clone https://github.com/RyAnPr1Me/compress.git
cd compress

# Run the demo
python compress.py
```

## Quick Start

### Basic Usage

```python
from compress import VideoCompressor, VideoCodec

# Initialize compressor
compressor = VideoCompressor()

# Create VVC encoding settings
settings = compressor.create_compression_settings(
    codec=VideoCodec.VVC,
    quality="high",
    target_resolution=(3840, 2160)  # 4K
)

# Validate settings
valid, errors = compressor.validate_settings(settings)
if valid:
    print("Settings are valid!")
    
# Get estimated compression ratio
ratio = compressor.estimate_compression_ratio(settings)
print(f"Estimated compression: {ratio:.2f}x vs H.264")

# Generate encoding command
cmd = compressor.generate_encoding_command(
    settings, 
    "input.mp4", 
    "output.vvc"
)
print(cmd)
```

### Compare Codecs

```python
from compress import VideoCompressor

compressor = VideoCompressor()

# Get all codec capabilities
codecs = compressor.compare_codecs()

for codec_name, capabilities in codecs.items():
    print(f"{capabilities.name}:")
    print(f"  Efficiency: {capabilities.compression_efficiency}x")
    print(f"  Max Resolution: {capabilities.max_resolution}")
    print(f"  HDR: {capabilities.hdr_support}")
```

### Get Codec Recommendations

```python
from compress import VideoCompressor

compressor = VideoCompressor()

# Get recommended codec for 8K HDR content
recommended = compressor.get_recommended_codec(
    target_resolution="8K",
    require_hdr=True,
    computational_limit="high"
)

print(f"Recommended codec: {recommended.value}")  # Output: vvc
```

### Advanced VVC Settings

```python
from compress import CompressionSettings, VideoCodec, CompressionPreset

settings = CompressionSettings(
    codec=VideoCodec.VVC,
    preset=CompressionPreset.SLOW,
    crf=18,  # High quality (0-51, lower = better)
    resolution=(7680, 4320),  # 8K
    framerate=60,
    bit_depth=10,
    enable_hdr=True,
    enable_temporal_layers=True,
    enable_spatial_layers=True,  # VVC-exclusive feature
    tile_columns=4,
    tile_rows=2
)

# Validate and use
compressor = VideoCompressor()
valid, errors = compressor.validate_settings(settings)
```

## API Reference

### VideoCompressor Class

Main class for video compression operations.

#### Methods

- `get_codec_info(codec: VideoCodec) -> CodecCapabilities`
  - Get detailed information about a specific codec

- `compare_codecs() -> Dict[str, CodecCapabilities]`
  - Compare all available codecs

- `get_recommended_codec(target_resolution, require_hdr, computational_limit) -> VideoCodec`
  - Get codec recommendation based on requirements

- `create_compression_settings(codec, quality, target_resolution) -> CompressionSettings`
  - Create compression settings with sensible defaults

- `estimate_compression_ratio(settings: CompressionSettings) -> float`
  - Estimate compression ratio for given settings

- `get_encoding_complexity_score(settings: CompressionSettings) -> int`
  - Get encoding complexity score (1-10)

- `validate_settings(settings: CompressionSettings) -> Tuple[bool, List[str]]`
  - Validate compression settings

- `generate_encoding_command(settings, input_file, output_file) -> str`
  - Generate FFmpeg-compatible encoding command

- `export_settings(settings: CompressionSettings) -> str`
  - Export settings to JSON format

### Enums

#### VideoCodec
- `H264` - H.264/AVC
- `H265` - H.265/HEVC
- `AV1` - AV1
- `VVC` - VVC/H.266 (Most Advanced)

#### CompressionPreset
- `ULTRAFAST` - Fastest encoding
- `SUPERFAST`
- `VERYFAST`
- `FASTER`
- `FAST`
- `MEDIUM` - Balanced (default)
- `SLOW`
- `SLOWER`
- `VERYSLOW`
- `PLACEBO` - Slowest, best compression

### Data Classes

#### CompressionSettings
Configuration for video compression with the following attributes:
- `codec: VideoCodec` - Selected video codec
- `preset: CompressionPreset` - Encoding speed/quality preset
- `crf: int` - Constant rate factor (0-51)
- `bitrate: Optional[int]` - Target bitrate in kbps
- `resolution: Optional[Tuple[int, int]]` - Video resolution
- `framerate: Optional[int]` - Target framerate
- `bit_depth: int` - Color bit depth (8, 10, 12, 14, 16)
- `enable_hdr: bool` - Enable HDR encoding
- `enable_temporal_layers: bool` - Enable temporal scalability
- `enable_spatial_layers: bool` - Enable spatial scalability (VVC only)
- `tile_columns: int` - Number of tile columns for parallel encoding
- `tile_rows: int` - Number of tile rows for parallel encoding

#### CodecCapabilities
Describes codec capabilities:
- `name: str` - Codec name
- `max_resolution: str` - Maximum supported resolution
- `bit_depth_support: List[int]` - Supported bit depths
- `compression_efficiency: float` - Efficiency relative to H.264
- `computational_complexity: str` - Encoding complexity level
- `hdr_support: bool` - HDR support flag
- `vbr_support: bool` - Variable bitrate support
- `streaming_optimized: bool` - Streaming optimization flag
- `advanced_features: List[str]` - List of advanced features

## Codec Comparison

| Feature | H.264 | H.265 | AV1 | VVC/H.266 ⭐ |
|---------|-------|-------|-----|-------------|
| **Compression Efficiency** | 1.0x | 2.0x | 2.2x | **2.5x** |
| **Max Resolution** | 4K | 8K | 8K+ | **16K** |
| **Bit Depth** | 8 | 8-12 | 8-12 | **8-16** |
| **HDR Support** | ❌ | ✅ | ✅ | ✅ |
| **Complexity** | Low | Med-High | Very High | Very High |
| **Intra Modes** | 9 | 35 | 10 | **67** |
| **Spatial Layers** | ❌ | ❌ | ❌ | ✅ |
| **360° Video** | ❌ | Limited | Limited | ✅ |
| **Screen Content** | Basic | Good | Good | **Excellent** |
| **Year** | 2003 | 2013 | 2018 | **2020** |

## Performance Characteristics

### Encoding Speed vs. Compression Quality

```
Preset          Encoding Speed    File Size    Quality
---------------------------------------------------------
ultrafast       Fastest           Largest      Good
fast            Very Fast         Large        Good
medium          Moderate          Medium       Very Good
slow            Slow              Small        Excellent
veryslow        Very Slow         Smallest     Excellent
```

### VVC/H.266 Performance

**Bitrate Savings (compared to H.265/HEVC):**
- 1080p content: ~45-50% smaller
- 4K content: ~50-55% smaller
- 8K content: ~50-60% smaller

**Encoding Time:**
- 2-5x slower than H.265/HEVC
- Highly parallelizable
- Optimized implementations improving rapidly

## Use Cases

### VVC/H.266 is Ideal For:

1. **Ultra High Resolution Content**
   - 8K and 16K video
   - Future-proof archival
   - High-quality streaming

2. **Bandwidth-Constrained Scenarios**
   - Mobile video streaming
   - Satellite broadcasting
   - Remote video conferencing

3. **Professional Applications**
   - Cinema and broadcast
   - Professional video editing
   - Medical imaging

4. **Specialized Content**
   - 360-degree VR video
   - Screen content (presentations, gaming)
   - HDR and wide color gamut content

5. **Storage Optimization**
   - Video archives
   - Cloud storage
   - Content delivery networks

## Technical Background

### Why VVC/H.266 is More Advanced

VVC/H.266 represents a generational leap in video compression technology:

1. **Quadtree with Multi-Type Tree (QTMT)**
   - More flexible block partitioning than predecessors
   - Better adaptation to video content structure
   - Improved compression at boundaries and complex regions

2. **Enhanced Motion Compensation**
   - Affine motion: handles rotation, zoom, shear
   - DMVR: decoder-side refinement reduces bitrate
   - BDOF: optical flow for better interpolation
   - Larger motion vector range

3. **Advanced Intra Prediction**
   - 67 angular modes vs 35 in HEVC
   - Matrix-based intra prediction (MIP)
   - Combined inter/intra prediction (CIIP)
   - Better handling of texture and edges

4. **Sophisticated Filtering**
   - Adaptive loop filter with multiple configurations
   - Better artifact reduction
   - Enhanced edge preservation

5. **Modern Transform Techniques**
   - Low-frequency non-separable transform
   - Multiple transform selection
   - Dependent quantization
   - Better perceptual quality

### Industry Adoption

VVC/H.266 is being adopted by:
- Broadcasting organizations
- Streaming platforms
- Professional video production
- Telecommunications industry
- Consumer electronics manufacturers

## Requirements

- Python 3.7+
- No external dependencies for the library core
- FFmpeg with VVC support (for actual encoding)

## Examples

Run the included demo:

```bash
python compress.py
```

This will display:
- Codec comparison table
- VVC/H.266 advantages
- Example encoding configuration
- Estimated compression ratios
- Sample encoding commands

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

MIT License - See LICENSE file for details

## References

- [VVC/H.266 Specification](https://www.itu.int/rec/T-REC-H.266)
- [Fraunhofer HHI VVC Information](https://www.hhi.fraunhofer.de/en/departments/vca/technologies-and-solutions/h266-vvc.html)
- [MPEG VVC Overview](https://mpeg.chiariglione.org/standards/mpeg-i/versatile-video-coding)

## Acknowledgments

This library implements support for VVC/H.266, the most advanced video codec standardized by ITU-T and ISO/IEC, offering up to 50% bitrate savings compared to its predecessor H.265/HEVC.