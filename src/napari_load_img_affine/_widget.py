"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/stable/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
from typing import TYPE_CHECKING
from magicgui import magic_factory

if TYPE_CHECKING:
    import napari


@magic_factory(
    call_button="register",
    img_file={
        "label": "image",
        "filter": "*.czi",
        "tooltip": "Select the image",
    },
    transformation_file_type={
        "choices": [
            "landmark pairs",
            "affine matrix",
        ],
        "tooltip": "Specify the transformation file type",
    },
    transformation_file={
        "label": "transformation file",
        "filter": "*.csv",
        "tooltip": "Select the transformation file",
    },
)
def widget(img_layer: "napari.layers.Image"):
    print(f"you have selected {img_layer}")
