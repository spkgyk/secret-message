# secret-message

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A character grid decoder that reveals hidden messages from coordinate-based Unicode character layouts. The program transforms 2D coordinate data into visual patterns that form secret messages in uppercase letters.

## Overview

This project provides a solution for decoding secret messages encoded as Unicode characters positioned in a 2D grid. Given a Google Doc containing character coordinates, the program reconstructs the original message by placing each character in its specified position and filling 

## Technical Details

The decoder:
1. Retrieves document content from the provided Google Doc URL
2. Parses coordinate and character data
3. Creates a dynamic 2D grid based on maximum coordinates
4. Places characters at specified positions
5. Fills empty positions with spaces
6. Prints the completed grid using monospace formatting

