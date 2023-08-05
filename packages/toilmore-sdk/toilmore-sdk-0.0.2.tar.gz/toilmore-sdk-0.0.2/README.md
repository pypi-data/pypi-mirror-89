# Toilmore Python API

## Installing

    pip install toilmore-sdk


## How to use

Simplifies using the toilmore API by wrapping the request state machine.
To optimize an image, all you need is a valid API token, and domain.
See [here](https://pixellena.com/docs/quick-start-guide/) how to get them.

### Using the light API

```python
import os
import asyncio

from toilmoresdk import (
    LIGHT_API,
    Toilmore,
)
from toilmoresdk.submit_machine import OptimizationResponseStatus
from toilmoresdk.stream_helpers import store_file_content
from toilmoresdk.api_config import ApiConfig
from toilmoresdk.constants import PrecursorEnum

config = ApiConfig(
    # LIGHT_API contains our light api endpoint.
    api_endpoint=LIGHT_API,
    # Use a valid API token below:
    api_token='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    # Use a valid domain below, as received when
    # you created the token.
    domain='YYYYYYYYYYYYYYYYYYYYYYYYYY'
)

toilmore = Toilmore(config)

loop = asyncio.get_event_loop()

image_path = "./my_image.jpg"
precursor = PrecursorEnum.WEBP0
r = loop.run_until_complete(
    toilmore.optimize(image_path, precursor)
)

if r.status == OptimizationResponseStatus.FAILURE:
    rejection_notice = r.rejection_notice
    print(
        'rejection_notice: {}, inner_error: {}'.format(
            rejection_notice.rejection_notice,
            rejection_notice.inner_error
        )
    )
elif r.status == OptimizationResponseStatus.SUCCESS:
    output_dir = os.path.dirname(image_path)  # You can change that to any other directory.
    base_filename, file_extension = os.path.splitext(image_path)
    loop.run_until_complete(
        store_file_content(
            r.response_stream,
            output_dir,
            base_filename,
            precursor
        )
    )
    print('Optimized image stored at: ', output_dir)

```

### Using the Lux API

```python
import os
import asyncio

from toilmoresdk import (
    LUX_API,
    Toilmore,
)
from toilmoresdk.submit_machine import OptimizationResponseStatus
from toilmoresdk.stream_helpers import store_file_content
from toilmoresdk.api_config import ApiConfig
from toilmoresdk.constants import PrecursorEnum

config = ApiConfig(
    # LIGHT_API contains our light api endpoint.
    api_endpoint=LUX_API,
    # Use a valid API token below:
    api_token='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    # Use a valid domain below, as received when
    # you created the token.
    domain='YYYYYYYYYYYYYYYYYYYYYYYYYY'
)

toilmore = Toilmore(config)

loop = asyncio.get_event_loop()

image_path = "./my_image.jpg"
precursor = PrecursorEnum.WEBP0
adjustments = {
    "shifter": {
        "steps": [
            {
                "scale-to": {
                    "width": 90
                }
            }
        ]
    },
    "encoder": {
        "quality-measure": "fsim-c",
        "qual-threshold": 0.90
    }
}

r = loop.run_until_complete(
    toilmore.optimize(image_path, precursor, adjustments)
)

if r.status == OptimizationResponseStatus.FAILURE:
    rejection_notice = r.rejection_notice
    print(
        'rejection_notice: {}, inner_error: {}'.format(
            rejection_notice.rejection_notice,
            rejection_notice.inner_error
        )
    )
elif r.status == OptimizationResponseStatus.SUCCESS:
    output_dir = os.path.dirname(image_path)  # You can change that to any other directory.
    base_filename, file_extension = os.path.splitext(image_path)
    loop.run_until_complete(
        store_file_content(
            r.response_stream,
            output_dir,
            base_filename,
            precursor
        )
    )
    print('Optimized image stored at: ', output_dir)

```

Both the light and the lux API are supported as you could see above.
