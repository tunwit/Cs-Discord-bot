import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask

qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
qr.add_data('https://www.canva.com/design/DAGKjjqrxcU/HxN9ZuuJaBhnradnYKZ0Dw/edit')

# img_1 = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer())
# img_2 = qr.make_image(image_factory=StyledPilImage, color_mask=RadialGradiantColorMask())
img_3 = qr.make_image(image_factory=StyledPilImage, embeded_image_path="round.png",
                      color_mask=RadialGradiantColorMask(center_color=((3, 1, 51)),edge_color=((27, 12, 69))),
                      eye_drawer=RoundedModuleDrawer(radius_ratio=1))
img_3.show()