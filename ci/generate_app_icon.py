from pathlib import Path
import math
import struct
import zlib


def png_chunk(kind: bytes, data: bytes) -> bytes:
    return (
        struct.pack(">I", len(data))
        + kind
        + data
        + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    )


def write_png(path: Path, width: int, height: int, rows: list[bytes]) -> None:
    raw = b"".join(b"\x00" + row for row in rows)
    data = b"\x89PNG\r\n\x1a\n"
    data += png_chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    data += png_chunk(b"IDAT", zlib.compress(raw, 9))
    data += png_chunk(b"IEND", b"")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def lerp(a: int, b: int, t: float) -> int:
    return int(a + (b - a) * t)


def make_icon() -> list[bytes]:
    size = 1024
    rows: list[bytes] = []
    for y in range(size):
        row = bytearray()
        for x in range(size):
            nx = (x / size) - 0.5
            ny = (y / size) - 0.5
            radial = max(0.0, 1.0 - math.sqrt(nx * nx + ny * ny) * 1.7)
            ember = max(0.0, 1.0 - math.sqrt((nx + 0.28) ** 2 + (ny - 0.22) ** 2) * 2.1)
            green = max(0.0, 1.0 - math.sqrt((nx - 0.24) ** 2 + (ny + 0.18) ** 2) * 2.4)

            r = 5 + int(54 * radial) + int(68 * ember)
            g = 7 + int(42 * radial) + int(32 * green) + int(28 * ember)
            b = 8 + int(22 * radial) + int(18 * green)

            monogram = False
            if 350 < x < 430 and 310 < y < 715:
                monogram = True
            if 594 < x < 674 and 310 < y < 715:
                monogram = True
            if abs((x - 512) - (y - 512) * 0.55) < 34 and 355 < y < 675:
                monogram = True

            ring = abs(math.sqrt(nx * nx + ny * ny) - 0.36) < 0.012
            if monogram or ring:
                glow = 1.0 if monogram else 0.76
                r = lerp(r, 225, glow)
                g = lerp(g, 185, glow)
                b = lerp(b, 105, glow)

            row.extend((min(r, 255), min(g, 255), min(b, 255)))
        rows.append(bytes(row))
    return rows


if __name__ == "__main__":
    output = Path("NOX Apothecary/Resources/Assets.xcassets/AppIcon.appiconset/nox-icon.png")
    write_png(output, 1024, 1024, make_icon())
    print(f"Wrote {output}")
