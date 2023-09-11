from pathlib import Path
from typing import TYPE_CHECKING, Sequence
from magicgui import magic_factory
from napari import Viewer
import numpy as np

if TYPE_CHECKING:
    import napari


def get_affine_matrix_from_landmarks(
        source_points_landmarks, target_points_landmarks
):
    pts_count = len(source_points_landmarks)
    A = np.zeros((pts_count * 3, 12))
    b = np.zeros(pts_count * 3)
    for i in range(pts_count):
        # build A
        A[i * 3][0] = source_points_landmarks[i][0]
        A[i * 3][1] = source_points_landmarks[i][1]
        A[i * 3][2] = source_points_landmarks[i][2]
        A[i * 3][3] = 1
        A[i * 3 + 1][4] = source_points_landmarks[i][0]
        A[i * 3 + 1][5] = source_points_landmarks[i][1]
        A[i * 3 + 1][6] = source_points_landmarks[i][2]
        A[i * 3 + 1][7] = 1
        A[i * 3 + 2][8] = source_points_landmarks[i][0]
        A[i * 3 + 2][9] = source_points_landmarks[i][1]
        A[i * 3 + 2][10] = source_points_landmarks[i][2]
        A[i * 3 + 2][11] = 1
        # build b
        b[i * 3] = target_points_landmarks[i, 0]
        b[i * 3 + 1] = target_points_landmarks[i, 1]
        b[i * 3 + 2] = target_points_landmarks[i, 2]
    x = np.linalg.solve(np.dot(A.T, A), np.dot(A.T, b.T))
    matrix = np.append(x.reshape(3, 4), [[0.0, 0.0, 0.0, 1.0]], axis=0)
    return matrix


def rot_matrix_xyz_to_zyx(matrix_xyz):
    matrix_zyx = np.rot90(matrix_xyz, 2)
    return matrix_zyx


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
        "tooltip": "Specify the transformation file type"
    },
    transformation_file={
        "label": "transformation file",
        "filter": "*.csv",
        "tooltip": "Select the transformation file"
                   "A landmarks file following the BigWarp format, or a 4x4 affine transformation matrix",
    },
)
def widget(
        viewer: Viewer,
        img_file: Sequence[Path],
        transformation_file_type: str,
        transformation_file: Sequence[Path],
):
    transformation_file_path = str(transformation_file[0])
    affine_matrix = np.identity(4)
    if transformation_file_type == "landmark pairs":
        # load landmark pairs
        landmarks = np.loadtxt(
            transformation_file_path,
            delimiter=",",
            converters=lambda x: float(eval(x)),
            usecols=(2, 3, 4, 5, 6, 7),
        )
        # landmark coordinates in xyz order
        source_landmarks = landmarks[:, [0, 1, 2]]
        target_landmarks = landmarks[:, [3, 4, 5]]
        affine_matrix = get_affine_matrix_from_landmarks(source_landmarks, target_landmarks)
    if transformation_file_type == "affine matrix":
        affine_matrix = np.loadtxt(
            transformation_file_path,
            delimiter=",",
            converters=lambda x: float(eval(x)),
        )
    affine_matrix_napari = rot_matrix_xyz_to_zyx(affine_matrix)
    img_file_path = str(img_file[0])
    print("load image")
    img = viewer.open(img_file_path)
    print("apply affine")
    for layer in img:
        layer.affine = affine_matrix_napari
