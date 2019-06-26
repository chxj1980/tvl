import PIL.Image
import torch
from numpy.testing import assert_allclose

from tvl_backends.fffr import FffrBackendFactory


def test_memory_leakage(backend):
    """Check that the memory manager is not leaking memory."""
    device = backend.image_allocator.device
    if device.type == 'cuda':
        start_mem = torch.cuda.memory_allocated(device.index)
        for _ in range(5):
            backend.read_frame()
        end_mem = torch.cuda.memory_allocated(device.index)
        assert end_mem == start_mem
    else:
        for _ in range(5):
            backend.read_frame()
    assert len(backend.image_allocator.tensors) == 0


def test_read_frame_float32_cpu(video_filename, first_frame_image):
    backend = FffrBackendFactory().create(video_filename, 'cpu', torch.float32)
    rgb_frame = backend.read_frame()
    assert rgb_frame.shape == (3, 720, 1280)
    actual = PIL.Image.fromarray((rgb_frame * 255).byte().permute(1, 2, 0).numpy(), 'RGB')
    assert_allclose(actual, first_frame_image, atol=50)
