#!/usr/bin/env python3
import qrcode
import qrcode.image.svg
import aes

# example use: make_qr('test.svg', 'client_id=1&direction=out')
def make_qr(path, data):
    encrypted_data = aes.encrypt(data)
    img = qrcode.make(encrypted_data, image_factory=qrcode.image.svg.SvgImage)
    img.save(path)
    
