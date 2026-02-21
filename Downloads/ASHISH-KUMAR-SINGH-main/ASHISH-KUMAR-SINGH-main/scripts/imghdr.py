"""Compatibility shim for Python 3.13+ where stdlib imghdr was removed.

Provides a minimal `what` function used by Streamlit to detect image types.
It tries to use Pillow if available and falls back to None.
"""

from __future__ import annotations

from typing import Optional, Union, BinaryIO


def what(file: Union[str, bytes, BinaryIO], h: Optional[bytes] = None) -> Optional[str]:
    """Best-effort image type detection.

    Parameters
    ----------
    file: path, file-like object, or bytes
    h: optional header bytes (ignored; kept for API compatibility)

    Returns
    -------
    str or None
        Lowercase image format name like 'png', 'jpeg', etc., or None if unknown.
    """
    try:
        from PIL import Image  # type: ignore
    except Exception:
        return None

    try:
        if hasattr(file, "read"):
            # file-like object
            pos = file.tell()
            try:
                img = Image.open(file)
                fmt = img.format
            finally:
                file.seek(pos)
        else:
            # path or bytes
            img = Image.open(file)
            fmt = img.format

        return fmt.lower() if fmt else None
    except Exception:
        return None


__all__ = ["what"]
