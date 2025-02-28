from ngdb import NGEOF, NortonGuide

if __name__ == "__main__":
    with NortonGuide("tests/guides/oslib.ng") as guide:
        guide.goto_first()
        while True:
            print("Found an entry")
            try:
                guide.skip()
            except NGEOF:
                print("Hit the end of the guide!")
                break
