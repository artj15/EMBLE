import os

import uvicorn  # type: ignore

from misc import (
    log,
)
from services.main import factory

app = factory()

if __name__ == '__main__':
    log.logger_conf()
    uvicorn.run(
        'emble_app:app', host='0.0.0.0', port=8010, reload=True, debug=True, log_config=os.getenv('LOG_CONFIG'),
    )
