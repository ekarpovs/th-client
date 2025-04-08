"""
For development purpose only
"""

import os
import sys

import uvicorn


if __name__ == "__main__":

    PORT = 8011
    
    # Run the server
    uvicorn.run("src.app:app", host='127.0.0.1', port=PORT,
                log_level="info", reload=True)
