from PIL import Image
import sys
import io
import lz4.block
import os

def b2i(b):
    return int.from_bytes(b, byteorder="little")

def save_to_png(width, height, data, filename):
    img = Image.frombytes('RGBA', (width,height), data)
    img.save(filename)

def main():
    with open(sys.argv[1], "rb") as f:
        magic = f.read(0x04)
        bpp = f.read(0x04)
        width = f.read(0x04)
        height = f.read(0x04)
        size = f.read(0x04)
        zsize = f.read(0x04)
        data = f.read(b2i(zsize))
        
        decompressed = io.BytesIO(lz4.block.decompress(data, uncompressed_size=b2i(size)))
        
        size = decompressed.read(0x04)
        zsize = decompressed.read(0x04)
        data = decompressed.read(b2i(zsize))

        decompressedf = lz4.block.decompress(data, uncompressed_size=b2i(size))

        save_to_png(b2i(width), b2i(height), decompressedf, os.path.basename(sys.argv[1]))


    return

if __name__ == "__main__":
    main()