# installer SVG2PNG
# Copyright 2023 Johanna Roedenbeck
# Distributed under the terms of the GNU Public License (GPLv3)

from weecfg.extension import ExtensionInstaller

def loader():
    return SVG2PNGInstaller()

class SVG2PNGInstaller(ExtensionInstaller):
    def __init__(self):
        super(SVG2PNGInstaller, self).__init__(
            version="0.1",
            name='SVG2PNG',
            description='convert SVG to PNG files',
            author="Johanna Roedenbeck",
            author_email="",
            files=[('bin/user', ['bin/user/svg2png.py'])]
            )
