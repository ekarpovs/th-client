"""
For development purpose only
"""

import os
import sys

import uvicorn


if __name__ == "__main__":

    PORT = 8011
    if len(sys.argv) > 1:
        os.environ['EXTERNAL_URL'] = sys.argv[1]
    if len(sys.argv) > 2:
        os.environ['BROADCAST_SERVICE'] = sys.argv[2]
    
    # Run the server
    uvicorn.run("src.app:app", host='0.0.0.0', port=PORT,
                log_level="info", reload=True)
