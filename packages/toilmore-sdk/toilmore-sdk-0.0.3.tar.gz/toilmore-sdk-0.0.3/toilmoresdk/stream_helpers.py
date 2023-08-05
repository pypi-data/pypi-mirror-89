from typing import (
    NamedTuple,
    Union,
    Callable,
)
import hashlib
import io
import os
from inspect import isfunction

from asyncfile import (
    AsyncBufferedReader,
    AsyncFileIO,
)

from toilmoresdk import constants

BUF_SIZE = 65536  # 64KB


StreamFactory = Callable[[Union[str, bytes]], AsyncBufferedReader]


# A mechanism for _repeatedly_ reading the bytes of an image.
# We need this so that we can generate a hash of the image (one read)
# and later send the image contents (a second read) without _necessarily_
# storing the full image in RAM. This way, with some careful handling, the
# API can be used to process a very large number of very large images
# concurrently without hogging the RAM of the machine.
#
# If a string is provided, it is interpreted as a filename.
# If bytes, its contents are taken as the byte contents of the
# image file.
# If a StreamFactory (that is, a function which takes no parameters and returns
# an AsyncBufferedReader), then the factory may be called multiple times to
# read the file multiple times.
ImageArg = Union[str, bytes, StreamFactory]


class OnePassInfo(NamedTuple):
    file_hash: str
    file_size: int


async def stream_from_argument(arg: ImageArg) -> Callable:
    def from_file_path() -> AsyncBufferedReader:
        assert isinstance(arg, str)
        wrap = AsyncFileIO(arg, 'rb')
        return AsyncBufferedReader(wrap, buffer_size=BUF_SIZE)

    def from_bytes() -> AsyncBufferedReader:
        assert isinstance(arg, bytes)
        return AsyncBufferedReader(io.BytesIO(arg), buffer_size=BUF_SIZE)

    if isinstance(arg, str):
        # Consider it a filename.
        return from_file_path
    elif isinstance(arg, bytes):
        return from_bytes
    elif isfunction(arg):
        return arg
    else:
        raise Exception('BadArgument. {}'.format(type(arg)))


async def pass_and_compute_hash(stream: AsyncBufferedReader) -> OnePassInfo:
    # stream is a stream with the data.
    sha1 = hashlib.sha1()
    total_size = 0
    async for chunk in stream:
        if not chunk:
            break
        sha1.update(chunk)
        total_size += len(chunk)

    return OnePassInfo(
        file_hash=sha1.hexdigest(),
        file_size=total_size
    )


async def store_file_content(
    stream: AsyncBufferedReader,
    output_path: str,
    base_filename: str,
    precursor: constants.PrecursorEnum
) -> None:

    optimized_filename = '{}{}'.format(
        base_filename,
        constants.PrecursorToExtensionEnum[precursor.name].value
    )
    optimized_path = os.path.join(
        output_path,
        optimized_filename
    )
    size = 0
    with open(optimized_path, 'wb+') as f:
        async for chunk in stream:
            f.write(chunk)
            size += len(chunk)

    return size
