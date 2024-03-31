"""Code to support the DOS heritage of most Norton Guide databases."""

##############################################################################
# Python compatibility hackage.
from __future__ import annotations

##############################################################################
# Python imports.
from typing import Final

##############################################################################
DOS_MAP: Final[dict[int, str]] = str.maketrans(
    {
        0: " ",
        1: "\u263A",
        2: "\u263B",
        3: "\u2665",
        4: "\u2666",
        5: "\u2663",
        6: "\u2660",
        7: "\u2022",
        8: "\u25DB",
        9: "\u25CB",
        10: "\u25D9",
        11: "\u2642",
        12: "\u2640",
        13: "\u266A",
        14: "\u266B",
        15: "\u263C",
        16: "\u25BA",
        17: "\u25C4",
        18: "\u2195",
        19: "\u203C",
        20: "\u00B6",
        21: "\u00A7",
        22: "\u25AC",
        23: "\u21A8",
        24: "\u2191",
        25: "\u2193",
        26: "\u2192",
        27: "\u2190",
        28: "\u221F",
        29: "\u2194",
        30: "\u25B2",
        31: "\u25BC",
        127: "\u2302",
        128: "\u00C7",
        129: "\u00FC",
        130: "\u00E9",
        131: "\u00E2",
        132: "\u00E4",
        133: "\u00E0",
        134: "\u00E5",
        135: "\u00E7",
        136: "\u00EA",
        137: "\u00EB",
        138: "\u00E8",
        139: "\u00EF",
        140: "\u00EE",
        141: "\u00EC",
        142: "\u00C4",
        143: "\u00C5",
        144: "\u00C9",
        145: "\u00E6",
        146: "\u00C6",
        147: "\u00F4",
        148: "\u00F6",
        149: "\u00F2",
        150: "\u00FB",
        151: "\u00F9",
        152: "\u00FF",
        153: "\u00D6",
        154: "\u00DC",
        155: "\u00A2",
        156: "\u00A3",
        157: "\u00A5",
        158: "\u20A7",
        159: "\u0192",
        160: "\u00E1",
        161: "\u00ED",
        162: "\u00F3",
        163: "\u00FA",
        164: "\u00F1",
        165: "\u00D1",
        166: "\u00AA",
        167: "\u00BA",
        168: "\u00BF",
        169: "\u2319",
        170: "\u00AC",
        171: "\u00BD",
        172: "\u00BC",
        173: "\u00A1",
        174: "\u00AB",
        175: "\u00BB",
        176: "\u2591",
        177: "\u2592",
        178: "\u2593",
        179: "\u2502",
        180: "\u2524",
        181: "\u2561",
        182: "\u2562",
        183: "\u2556",
        184: "\u2555",
        185: "\u2563",
        186: "\u2551",
        187: "\u2557",
        188: "\u255D",
        189: "\u255C",
        190: "\u255B",
        191: "\u2510",
        192: "\u2514",
        193: "\u2534",
        194: "\u252C",
        195: "\u251C",
        196: "\u2500",
        197: "\u253C",
        198: "\u255E",
        199: "\u255F",
        200: "\u255A",
        201: "\u2554",
        202: "\u2569",
        203: "\u2566",
        204: "\u2560",
        205: "\u2550",
        206: "\u256C",
        207: "\u2567",
        208: "\u2568",
        209: "\u2564",
        210: "\u2565",
        211: "\u2559",
        212: "\u2558",
        213: "\u2552",
        214: "\u2553",
        215: "\u256B",
        216: "\u256A",
        217: "\u251B",
        218: "\u250C",
        219: "\u2588",
        220: "\u2584",
        221: "\u258C",
        222: "\u2590",
        223: "\u2580",
        224: "\u03B1",
        225: "\u00DF",
        226: "\u0393",
        227: "\u03C0",
        228: "\u03A3",
        229: "\u03C3",
        230: "\u00B5",
        231: "\u03C4",
        232: "\u03A6",
        233: "\u039B",
        234: "\u03A9",
        235: "\u03b4",
        236: "\u221E",
        237: "\u03C6",
        238: "\u03B5",
        239: "\u2229",
        240: "\u2261",
        241: "\u00B1",
        242: "\u2265",
        243: "\u2264",
        244: "\u2320",
        245: "\u2321",
        246: "\u00F7",
        248: "\u00B0",
        249: "\u2219",
        250: "\u00B7",
        251: "\u221A",
        252: "\u207F",
        253: "\u00B2",
        254: "\u25A0",
        255: "\u00A0",
    }
)
"""Map For translating into DOS-a-like characters."""


##############################################################################
def make_dos_like(text: str) -> str:
    """Try and make a string from a guide capable of retaining DOS-likeness.

    Args:
        text: The text to convert.

    Returns:
        The converted text.
    """
    return text.translate(DOS_MAP)


### dosify.py ends here
