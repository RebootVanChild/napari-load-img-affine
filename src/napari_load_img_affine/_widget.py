from pathlib import Path
from typing import TYPE_CHECKING, Sequence
from magicgui import magic_factory
from napari import Viewer

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
def widget(
    viewer: Viewer,
    img_file: Sequence[Path],
    transformation_file_type: str,
    transformation_file: Sequence[Path],
):
    print(f"you have selected")
