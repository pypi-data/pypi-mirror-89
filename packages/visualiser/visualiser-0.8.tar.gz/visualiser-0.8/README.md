# Visualiser
A terminal visualiser for songs.

## Installation
```bash
pip3 install visualiser
```

## Usage
```python
from visualiser import Visualiser

viz = Visualiser('path/to/audio-file') 

viz.visualise()
```

For rgb colours:
```python
viz = Visualiser('path/to/audio-file', is_rgb=True)
```