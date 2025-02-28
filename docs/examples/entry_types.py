from ngdb import Long, NortonGuide, Short

if __name__ == "__main__":
    with NortonGuide("tests/guides/oslib.ng") as guide:
        guide.goto_first()
        while not guide.eof:
            entry = guide.load()
            if isinstance(entry, Short):
                print("Short")
            elif isinstance(entry, Long):
                print("Long")
            else:
                print("This can't be possible")
            guide.skip()
