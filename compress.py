"""
Video Compression Library with Advanced Codec Support
Supports VVC/H.266 - the most advanced video codec available
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import json


class VideoCodec(Enum):
    """Supported video codecs"""
    H264 = "h264"
    H265 = "h265"  # HEVC
    AV1 = "av1"
    VVC = "vvc"  # H.266 - Most advanced codec


class CompressionPreset(Enum):
    """Compression speed/quality presets"""
    ULTRAFAST = "ultrafast"
    SUPERFAST = "superfast"
    VERYFAST = "veryfast"
    FASTER = "faster"
    FAST = "fast"
    MEDIUM = "medium"
    SLOW = "slow"
    SLOWER = "slower"
    VERYSLOW = "veryslow"
    PLACEBO = "placebo"


@dataclass
class CodecCapabilities:
    """Capabilities of a video codec"""
    name: str
    max_resolution: str
    bit_depth_support: List[int]
    compression_efficiency: float  # Relative to H.264 (1.0 = baseline)
    computational_complexity: str
    hdr_support: bool
    vbr_support: bool
    streaming_optimized: bool
    advanced_features: List[str]


@dataclass
class CompressionSettings:
    """Settings for video compression"""
    codec: VideoCodec
    preset: CompressionPreset
    crf: int  # Constant Rate Factor (0-51, lower = better quality)
    bitrate: Optional[int] = None  # Target bitrate in kbps
    resolution: Optional[Tuple[int, int]] = None
    framerate: Optional[int] = None
    bit_depth: int = 8
    enable_hdr: bool = False
    enable_temporal_layers: bool = True
    enable_spatial_layers: bool = False
    tile_columns: int = 1
    tile_rows: int = 1


class VideoCompressor:
    """Advanced video compression engine"""
    
    def __init__(self):
        self.codecs = self._initialize_codecs()
        
    def _initialize_codecs(self) -> Dict[VideoCodec, CodecCapabilities]:
        """Initialize codec capabilities"""
        return {
            VideoCodec.H264: CodecCapabilities(
                name="H.264/AVC",
                max_resolution="4K",
                bit_depth_support=[8],
                compression_efficiency=1.0,
                computational_complexity="Low",
                hdr_support=False,
                vbr_support=True,
                streaming_optimized=True,
                advanced_features=["CABAC", "B-frames", "Multiple reference frames"]
            ),
            VideoCodec.H265: CodecCapabilities(
                name="H.265/HEVC",
                max_resolution="8K",
                bit_depth_support=[8, 10, 12],
                compression_efficiency=2.0,
                computational_complexity="Medium-High",
                hdr_support=True,
                vbr_support=True,
                streaming_optimized=True,
                advanced_features=[
                    "CTU (Coding Tree Units)",
                    "Advanced motion compensation",
                    "Improved intra prediction",
                    "Sample Adaptive Offset (SAO)",
                    "Tiles and slices"
                ]
            ),
            VideoCodec.AV1: CodecCapabilities(
                name="AV1",
                max_resolution="8K+",
                bit_depth_support=[8, 10, 12],
                compression_efficiency=2.2,
                computational_complexity="Very High",
                hdr_support=True,
                vbr_support=True,
                streaming_optimized=True,
                advanced_features=[
                    "Film grain synthesis",
                    "Compound prediction",
                    "Intra block copy",
                    "Superblock structure (128x128)",
                    "CDEF (Constrained Directional Enhancement Filter)",
                    "Loop restoration filter"
                ]
            ),
            VideoCodec.VVC: CodecCapabilities(
                name="VVC/H.266",
                max_resolution="16K",
                bit_depth_support=[8, 10, 12, 14, 16],
                compression_efficiency=2.5,
                computational_complexity="Very High",
                hdr_support=True,
                vbr_support=True,
                streaming_optimized=True,
                advanced_features=[
                    "Enhanced quad-tree partitioning with multi-type tree",
                    "Improved intra prediction (67 directional modes)",
                    "Affine motion compensation",
                    "Adaptive loop filter (ALF)",
                    "Decoder-side motion vector refinement (DMVR)",
                    "Bi-directional optical flow (BDOF)",
                    "Combined inter/intra prediction (CIIP)",
                    "Geometric partitioning mode (GPM)",
                    "Matrix-based intra prediction (MIP)",
                    "Subblock-based temporal motion vector prediction (SbTMVP)",
                    "Triangle partitioning mode",
                    "Advanced motion vector prediction (AMVP) enhancements",
                    "Dependent quantization",
                    "Low-frequency non-separable transform (LFNST)",
                    "Block differential pulse-code modulation (BDPCM)",
                    "Adaptive color transform",
                    "Reference picture resampling",
                    "360-degree video support",
                    "Screen content coding tools"
                ]
            )
        }
    
    def get_codec_info(self, codec: VideoCodec) -> CodecCapabilities:
        """Get information about a specific codec"""
        return self.codecs[codec]
    
    def compare_codecs(self) -> Dict[str, CodecCapabilities]:
        """Compare all available codecs"""
        return {codec.value: caps for codec, caps in self.codecs.items()}
    
    def get_recommended_codec(self, 
                            target_resolution: str = "4K",
                            require_hdr: bool = False,
                            computational_limit: str = "high") -> VideoCodec:
        """Get recommended codec based on requirements"""
        if require_hdr and computational_limit == "low":
            return VideoCodec.H265
        elif require_hdr and target_resolution in ["8K", "16K"]:
            return VideoCodec.VVC
        elif computational_limit == "low":
            return VideoCodec.H264
        else:
            return VideoCodec.VVC  # Most advanced option
    
    def create_compression_settings(self,
                                   codec: VideoCodec = VideoCodec.VVC,
                                   quality: str = "high",
                                   target_resolution: Optional[Tuple[int, int]] = None) -> CompressionSettings:
        """Create compression settings with sensible defaults"""
        preset_map = {
            "fastest": CompressionPreset.ULTRAFAST,
            "fast": CompressionPreset.FAST,
            "medium": CompressionPreset.MEDIUM,
            "high": CompressionPreset.SLOW,
            "highest": CompressionPreset.VERYSLOW
        }
        
        crf_map = {
            "low": 28,
            "medium": 23,
            "high": 18,
            "highest": 15
        }
        
        return CompressionSettings(
            codec=codec,
            preset=preset_map.get(quality, CompressionPreset.MEDIUM),
            crf=crf_map.get(quality, 23),
            resolution=target_resolution,
            bit_depth=10 if codec in [VideoCodec.H265, VideoCodec.AV1, VideoCodec.VVC] else 8,
            enable_hdr=codec in [VideoCodec.H265, VideoCodec.AV1, VideoCodec.VVC],
            enable_temporal_layers=codec in [VideoCodec.AV1, VideoCodec.VVC],
            enable_spatial_layers=codec == VideoCodec.VVC
        )
    
    def estimate_compression_ratio(self, settings: CompressionSettings) -> float:
        """Estimate compression ratio based on settings"""
        codec_caps = self.codecs[settings.codec]
        base_efficiency = codec_caps.compression_efficiency
        
        # Adjust for CRF
        crf_factor = 1.0 + (23 - settings.crf) * 0.1
        
        # Adjust for advanced features
        feature_factor = 1.0
        if settings.enable_temporal_layers:
            feature_factor *= 1.1
        if settings.enable_spatial_layers:
            feature_factor *= 1.05
        if settings.bit_depth > 8:
            feature_factor *= 0.95  # Slightly less compression for higher bit depth
            
        return base_efficiency * crf_factor * feature_factor
    
    def get_encoding_complexity_score(self, settings: CompressionSettings) -> int:
        """Get encoding complexity score (1-10, higher = more complex)"""
        complexity_map = {
            "Low": 2,
            "Medium": 4,
            "Medium-High": 6,
            "High": 8,
            "Very High": 10
        }
        
        codec_caps = self.codecs[settings.codec]
        base_complexity = complexity_map.get(codec_caps.computational_complexity, 5)
        
        # Adjust for preset
        preset_adjustment = {
            CompressionPreset.ULTRAFAST: -2,
            CompressionPreset.FAST: -1,
            CompressionPreset.MEDIUM: 0,
            CompressionPreset.SLOW: 1,
            CompressionPreset.VERYSLOW: 2
        }.get(settings.preset, 0)
        
        return min(10, max(1, base_complexity + preset_adjustment))
    
    def validate_settings(self, settings: CompressionSettings) -> Tuple[bool, List[str]]:
        """Validate compression settings"""
        errors = []
        codec_caps = self.codecs[settings.codec]
        
        # Check bit depth support
        if settings.bit_depth not in codec_caps.bit_depth_support:
            errors.append(
                f"{codec_caps.name} does not support {settings.bit_depth}-bit encoding. "
                f"Supported: {codec_caps.bit_depth_support}"
            )
        
        # Check HDR support
        if settings.enable_hdr and not codec_caps.hdr_support:
            errors.append(f"{codec_caps.name} does not support HDR encoding")
        
        # Check CRF range
        if not (0 <= settings.crf <= 51):
            errors.append(f"CRF must be between 0 and 51, got {settings.crf}")
        
        # Check spatial layers
        if settings.enable_spatial_layers and settings.codec != VideoCodec.VVC:
            errors.append("Spatial layers are only supported with VVC/H.266 codec")
        
        return len(errors) == 0, errors
    
    def generate_encoding_command(self, settings: CompressionSettings, 
                                 input_file: str, output_file: str) -> str:
        """Generate encoding command string (for demonstration)"""
        codec_name_map = {
            VideoCodec.H264: "libx264",
            VideoCodec.H265: "libx265",
            VideoCodec.AV1: "libaom-av1",
            VideoCodec.VVC: "libvvenc"
        }
        
        codec_lib = codec_name_map[settings.codec]
        cmd_parts = [
            f"ffmpeg -i {input_file}",
            f"-c:v {codec_lib}",
            f"-preset {settings.preset.value}",
            f"-crf {settings.crf}"
        ]
        
        if settings.resolution:
            cmd_parts.append(f"-s {settings.resolution[0]}x{settings.resolution[1]}")
        
        if settings.framerate:
            cmd_parts.append(f"-r {settings.framerate}")
        
        if settings.bit_depth > 8:
            cmd_parts.append(f"-pix_fmt yuv420p{settings.bit_depth}le")
        
        if settings.bitrate:
            cmd_parts.append(f"-b:v {settings.bitrate}k")
        
        # VVC-specific advanced options
        if settings.codec == VideoCodec.VVC:
            cmd_parts.extend([
                "-vvenc-params",
                "qpa=1:alf=1:mctf=1"  # Enable advanced VVC features
            ])
        
        cmd_parts.append(output_file)
        return " ".join(cmd_parts)
    
    def export_settings(self, settings: CompressionSettings) -> str:
        """Export settings to JSON"""
        return json.dumps({
            "codec": settings.codec.value,
            "preset": settings.preset.value,
            "crf": settings.crf,
            "bitrate": settings.bitrate,
            "resolution": settings.resolution,
            "framerate": settings.framerate,
            "bit_depth": settings.bit_depth,
            "enable_hdr": settings.enable_hdr,
            "enable_temporal_layers": settings.enable_temporal_layers,
            "enable_spatial_layers": settings.enable_spatial_layers,
            "tile_columns": settings.tile_columns,
            "tile_rows": settings.tile_rows
        }, indent=2)


def get_vvc_advantages() -> List[str]:
    """Get list of VVC/H.266 advantages over other codecs"""
    return [
        "50% bitrate savings compared to H.265/HEVC",
        "40% bitrate savings compared to AV1",
        "Support for up to 16K resolution",
        "Enhanced bit depth support (up to 16-bit)",
        "Advanced partitioning with multi-type tree structure",
        "67 directional intra prediction modes (vs 35 in HEVC)",
        "Affine motion compensation for non-translational motion",
        "Decoder-side motion vector refinement",
        "Bi-directional optical flow",
        "Geometric and triangle partitioning modes",
        "Matrix-based intra prediction",
        "Adaptive loop filter with enhanced filtering",
        "Dependent quantization for better perceptual quality",
        "Low-frequency non-separable transform",
        "Native 360-degree video support",
        "Advanced screen content coding tools",
        "Reference picture resampling for adaptive streaming",
        "Better parallel processing capabilities",
        "Improved HDR and wide color gamut support"
    ]


if __name__ == "__main__":
    # Demonstration
    compressor = VideoCompressor()
    
    print("=" * 80)
    print("Advanced Video Compression Library - VVC/H.266 Support")
    print("=" * 80)
    print()
    
    # Show codec comparison
    print("Codec Comparison:")
    print("-" * 80)
    for codec_enum, caps in compressor.compare_codecs().items():
        print(f"\n{caps.name} ({codec_enum}):")
        print(f"  Max Resolution: {caps.max_resolution}")
        print(f"  Compression Efficiency: {caps.compression_efficiency}x vs H.264")
        print(f"  Computational Complexity: {caps.computational_complexity}")
        print(f"  HDR Support: {caps.hdr_support}")
        print(f"  Bit Depth: {caps.bit_depth_support}")
    
    print("\n" + "=" * 80)
    print("VVC/H.266 Advantages:")
    print("-" * 80)
    for i, advantage in enumerate(get_vvc_advantages(), 1):
        print(f"{i:2}. {advantage}")
    
    print("\n" + "=" * 80)
    print("Example: High-Quality 4K VVC Encoding")
    print("-" * 80)
    
    # Create VVC settings
    settings = compressor.create_compression_settings(
        codec=VideoCodec.VVC,
        quality="high",
        target_resolution=(3840, 2160)
    )
    
    print("\nSettings:")
    print(compressor.export_settings(settings))
    
    # Validate
    valid, errors = compressor.validate_settings(settings)
    print(f"\nSettings Valid: {valid}")
    if errors:
        for error in errors:
            print(f"  Error: {error}")
    
    # Estimates
    compression_ratio = compressor.estimate_compression_ratio(settings)
    complexity = compressor.get_encoding_complexity_score(settings)
    
    print(f"\nEstimated Compression Ratio: {compression_ratio:.2f}x vs H.264")
    print(f"Encoding Complexity: {complexity}/10")
    
    # Generate command
    print("\nExample Encoding Command:")
    print(compressor.generate_encoding_command(settings, "input.mp4", "output.vvc"))
    
    print("\n" + "=" * 80)
