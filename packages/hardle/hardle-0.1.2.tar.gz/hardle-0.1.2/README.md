# Hardle

A simple & lightweight utility for (synchronously) downloading content from .HAR files. Useful when you want to download static sites for offline use.

## Installation

```
$ pip3 install hardle
```

Hardle uses type annotations, so Python 3.5 (minimum) is required.

## Usage

### From the Command Line

```
$ hardle path/to/file.har out/
```

### From Python

```py
from hardle import download

download("path/to/file.har", "out/")
```

## License

[MIT](./LICENSE)
