import sys
from hardle import download


def main():
    if len(sys.argv) != 3:
        print("Usage: hardle path/to/file.har out/")
        sys.exit()

    print("Downloading...")
    download(sys.argv[1], sys.argv[2])
    print("Done! Saved files to " + sys.argv[2])


if __name__ == "__main__":
    main()
