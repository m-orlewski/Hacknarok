#!/usr/bin/env python3
import qrcode
import qrcode.image.svg

def make_qr(path, data):
    img = qrcode.make(data, image_factory=qrcode.image.svg.SvgImage)
    img.save(path)
    

make_qr('test.svg', '<adres>/start?customer_id=1&reader_id=1')
