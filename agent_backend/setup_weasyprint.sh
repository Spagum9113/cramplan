#!/bin/bash

# Set up environment variables for WeasyPrint
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"
export PKG_CONFIG_PATH="/opt/homebrew/lib/pkgconfig:/opt/homebrew/opt/libffi/lib/pkgconfig:/opt/homebrew/opt/libxml2/lib/pkgconfig:/opt/homebrew/opt/libxslt/lib/pkgconfig:$PKG_CONFIG_PATH"
export LDFLAGS="-L/opt/homebrew/lib -L/opt/homebrew/opt/libffi/lib -L/opt/homebrew/opt/libxml2/lib -L/opt/homebrew/opt/libxslt/lib"
export CPPFLAGS="-I/opt/homebrew/include -I/opt/homebrew/opt/libffi/include -I/opt/homebrew/opt/libxml2/include -I/opt/homebrew/opt/libxslt/include"

# Print success message
echo "Environment variables set up for WeasyPrint"
echo "Now try running your application again" 