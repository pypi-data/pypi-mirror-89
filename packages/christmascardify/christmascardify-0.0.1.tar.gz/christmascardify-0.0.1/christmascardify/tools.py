import cv2
from PIL import Image, ImageFont, ImageDraw

styles = {
    1: {
        "photow": 1580,
        "photoh": 950,
        "photox": 210,
        "photoy": 400
    },
    "2": "hey"
}


def cardCreate(lastName, toWhom, photoPath, style, photoType, fontPath, bgPath):
    bg = Image.open(bgPath)
    photo = Image.open(photoPath)
    styleInfo = styles.get(style)
    bg = bg.resize((2000, 1500))

    photow, photoh = styleInfo.get("photow"), styleInfo.get("photoh")
    photox, photoy = styleInfo.get("photox"), styleInfo.get("photoy")
    photo = photo.resize((photow, photoh))

    bg.paste(photo, (photox, photoy))
    out = write(bg, fontPath, 'Merry Christmas', 2000, 20, fontSize=125)
    out = write(bg, fontPath, toWhom+'!', 2000, 150, offset=20)
    out = write(bg, fontPath, "From the " + lastName+'s', 2000, 1150, offset=20)

    return out


def write(img, fontPath, text, width, y, fontSize=200, offset=0):
    font = ImageFont.truetype(fontPath, fontSize)
    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(text, font=font)
    x = (width-w)/2+offset
    draw.text(text=text, font=font, xy=(x, y))

    return img
