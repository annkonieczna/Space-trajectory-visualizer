import spiceypy as spice


def load_kernels(meta_kernel_path):
    spice.furnsh(str(meta_kernel_path))


def clear_kernels():
    spice.kclear()
