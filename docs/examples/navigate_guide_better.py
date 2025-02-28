from ngdb import NortonGuide

if __name__ == "__main__":
    with NortonGuide("tests/guides/oslib.ng") as guide:
        guide.goto_first()
        while not guide.eof:
            print("Found an entry")
            guide.skip()
