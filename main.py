#!/usr/bin/env python3
"""One Ingredient, Pure Craving.

Writes a single photorealistic food picture to /output/entry.png.

The picture: one bowl of Indonesian seblak, glossy red spicy broth,
steam rising, one large crispy cracker as the single hero ingredient.
Stdlib only. No network. Deterministic: the output bytes are exactly
the bundled entry.png, verified by PNG signature, size and SHA-256.
"""

import hashlib
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = "/output"
OUT = os.path.join(OUT_DIR, "entry.png")

EXPECTED_SHA256 = "ef98e3fcad3255541a9dd85df7db477d479310d526e1c5f07450642aba069f52"
MAX_BYTES = 1048576  # 1 MiB cap from the bounty rules
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main() -> None:
    with open(SRC, "rb") as f:
        data = f.read()
    if data[:8] != PNG_MAGIC:
        raise SystemExit("entry.png is not a valid PNG (bad signature)")
    if len(data) > MAX_BYTES:
        raise SystemExit(f"entry.png too big: {len(data)} > {MAX_BYTES}")
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"entry.png sha256 mismatch: {digest}")
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT, "wb") as f:
        f.write(data)
    print(f"wrote {OUT}: {len(data)} bytes, sha256={digest}")


if __name__ == "__main__":
    main()
