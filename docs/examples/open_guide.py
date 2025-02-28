from ngdb import NortonGuide

if __name__ == "__main__":
    with NortonGuide("tests/guides/oslib.ng") as guide:
        print(guide.title)
