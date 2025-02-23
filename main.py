"""
For development purpose only
"""

import os
import sys

import uvicorn


if __name__ == "__main__":

    PORT = 8011
    if len(sys.argv) > 1:
        ext_url = sys.argv[1]
        os.environ['EXTERNAL_URL'] = ext_url
        _, _, port = ext_url.split(':')
        PORT = int(port)
    if len(sys.argv) > 2:
        os.environ['BROADCAST_SERVICE'] = sys.argv[2]
    
    # Run the server
    uvicorn.run("src.app:app", host='127.0.0.1', port=PORT,
                log_level="info", reload=True)
