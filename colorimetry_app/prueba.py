from PIL import Image

rgb = (180, 130, 110)

pixel = Image.new("RGB", (1, 1), rgb)

lab = pixel.convert("LAB").getpixel((0, 0))

print(lab)