import warnings
from pathlib import Path
from typing import Tuple
import torch
import numpy as np
import nibabel as nib
import SimpleITK as sitk
from ..typing import TypePath, TypeData
from ..utils import nib_to_sitk, sitk_to_nib, check_uint_to_int


FLIPXY = np.diag([-1, -1, 1, 1])


def read_image(path: TypePath) -> Tuple[torch.Tensor, np.ndarray]:
    try:
        result = _read_sitk(path)
    except RuntimeError:  # try with NiBabel
        try:
            result = _read_nibabel(path)
        except nib.loadsave.ImageFileError:
            raise RuntimeError(f'File "{path}" not understood')
    return result


def _read_nibabel(path: TypePath) -> Tuple[torch.Tensor, np.ndarray]:
    img = nib.load(str(path), mmap=False)
    data = img.get_fdata(dtype=np.float32)
    if data.ndim == 5:
        data = data[..., 0, :]
        data = data.transpose(3, 0, 1, 2)
    data = check_uint_to_int(data)
    tensor = torch.from_numpy(data)
    affine = img.affine
    return tensor, affine


def _read_sitk(path: TypePath) -> Tuple[torch.Tensor, np.ndarray]:
    if Path(path).is_dir():  # assume DICOM
        image = _read_dicom(path)
    else:
        image = sitk.ReadImage(str(path))
    data, affine = sitk_to_nib(image, keepdim=True)
    data = check_uint_to_int(data)
    tensor = torch.from_numpy(data)
    return tensor, affine


def _read_dicom(directory: TypePath):
    directory = Path(directory)
    if not directory.is_dir():  # unreachable if called from _read_sitk
        raise FileNotFoundError(f'Directory "{directory}" not found')
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(str(directory))
    if not dicom_names:
        message = (
            f'The directory "{directory}"'
            ' does not seem to contain DICOM files'
        )
        raise FileNotFoundError(message)
    reader.SetFileNames(dicom_names)
    image = reader.Execute()
    return image


def write_image(
        tensor: torch.Tensor,
        affine: TypeData,
        path: TypePath,
        squeeze: bool = True,
        ) -> None:
    args = tensor, affine, path
    try:
        _write_sitk(*args, squeeze=squeeze)
    except RuntimeError:  # try with NiBabel
        _write_nibabel(*args, squeeze=squeeze)


def _write_nibabel(
        tensor: TypeData,
        affine: TypeData,
        path: TypePath,
        squeeze: bool = False,
        ) -> None:
    """
    Expects a path with an extension that can be used by nibabel.save
    to write a NIfTI-1 image, such as '.nii.gz' or '.img'
    """
    assert tensor.ndim == 4
    num_components = tensor.shape[0]

    # NIfTI components must be at the end, in a 5D array
    if num_components == 1:
        tensor = tensor[0]
    else:
        tensor = tensor[np.newaxis].permute(2, 3, 4, 0, 1)
    tensor = tensor.squeeze() if squeeze else tensor
    suffix = Path(str(path).replace('.gz', '')).suffix
    if '.nii' in suffix:
        img = nib.Nifti1Image(np.asarray(tensor), affine)
    elif '.hdr' in suffix or '.img' in suffix:
        img = nib.Nifti1Pair(np.asarray(tensor), affine)
    else:
        raise nib.loadsave.ImageFileError
    if num_components > 1:
        img.header.set_intent('vector')
    img.header['qform_code'] = 1
    img.header['sform_code'] = 0
    nib.save(img, str(path))


def _write_sitk(
        tensor: torch.Tensor,
        affine: TypeData,
        path: TypePath,
        squeeze: bool = True,
        use_compression: bool = True,
        ) -> None:
    assert tensor.ndim == 4
    path = Path(path)
    if path.suffix in ('.png', '.jpg', '.jpeg'):
        warnings.warn(
            f'Casting to uint 8 before saving to {path}',
            RuntimeWarning,
        )
        tensor = tensor.numpy().astype(np.uint8)
    image = nib_to_sitk(tensor, affine, squeeze=squeeze)
    sitk.WriteImage(image, str(path), use_compression)


def read_matrix(path: TypePath):
    """Read an affine transform and convert to tensor."""
    path = Path(path)
    suffix = path.suffix
    if suffix in ('.tfm', '.h5'):  # ITK
        tensor = _read_itk_matrix(path)
    elif suffix in ('.txt', '.trsf'):  # NiftyReg, blockmatching
        tensor = _read_niftyreg_matrix(path)
    return tensor


def write_matrix(matrix: torch.Tensor, path: TypePath):
    """Write an affine transform."""
    path = Path(path)
    suffix = path.suffix
    if suffix in ('.tfm', '.h5'):  # ITK
        _write_itk_matrix(matrix, path)
    elif suffix in ('.txt', '.trsf'):  # NiftyReg, blockmatching
        _write_niftyreg_matrix(matrix, path)


def _to_itk_convention(matrix):
    """RAS to LPS"""
    matrix = np.dot(FLIPXY, matrix)
    matrix = np.dot(matrix, FLIPXY)
    matrix = np.linalg.inv(matrix)
    return matrix


def _from_itk_convention(matrix):
    """LPS to RAS"""
    matrix = np.dot(matrix, FLIPXY)
    matrix = np.dot(FLIPXY, matrix)
    matrix = np.linalg.inv(matrix)
    return matrix


def _read_itk_matrix(path):
    """Read an affine transform in ITK's .tfm format"""
    transform = sitk.ReadTransform(str(path))
    parameters = transform.GetParameters()
    rotation_parameters = parameters[:9]
    rotation_matrix = np.array(rotation_parameters).reshape(3, 3)
    translation_parameters = parameters[9:]
    translation_vector = np.array(translation_parameters).reshape(3, 1)
    matrix = np.hstack([rotation_matrix, translation_vector])
    homogeneous_matrix_lps = np.vstack([matrix, [0, 0, 0, 1]])
    homogeneous_matrix_ras = _from_itk_convention(homogeneous_matrix_lps)
    return torch.from_numpy(homogeneous_matrix_ras)


def _write_itk_matrix(matrix, tfm_path):
    """The tfm file contains the matrix from floating to reference."""
    transform = _matrix_to_itk_transform(matrix)
    transform.WriteTransform(str(tfm_path))


def _matrix_to_itk_transform(matrix, dimensions=3):
    matrix = _to_itk_convention(matrix)
    rotation = matrix[:dimensions, :dimensions].ravel().tolist()
    translation = matrix[:dimensions, 3].tolist()
    transform = sitk.AffineTransform(rotation, translation)
    return transform


def _read_niftyreg_matrix(trsf_path):
    """Read a NiftyReg matrix and return it as a NumPy array"""
    matrix = np.loadtxt(trsf_path)
    matrix = np.linalg.inv(matrix)
    return torch.from_numpy(matrix)


def _write_niftyreg_matrix(matrix, txt_path):
    """Write an affine transform in NiftyReg's .txt format (ref -> flo)"""
    matrix = np.linalg.inv(matrix)
    np.savetxt(txt_path, matrix, fmt='%.8f')
