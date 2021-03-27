#!/usr/bin/env python3
import qrcode
import qrcode.image.svg
import aes

# example use: make_qr('customer_id=<id>')
def make(data):
    encrypted_data = aes.encrypt(data)
    img = qrcode.make(encrypted_data, image_factory=qrcode.image.svg.SvgImage)
    return img

