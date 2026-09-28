#!/usr/bin/env python3
"""Build the public product feed from APUNOKAGI's public Minne shop page."""

from __future__ import annotations

import json
import sys
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

SHOP_URL = "https://minne.com/@apunokagi"
OUTPUT = Path(__file__).resolve().parents[1] / "data" / "minne-products.json"


class NextDataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_next_data = False
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "script" and values.get("id") == "__NEXT_DATA__":
            self.in_next_data = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self.in_next_data:
            self.in_next_data = False

    def handle_data(self, data: str) -> None:
        if self.in_next_data:
            self.parts.append(data)


def fetch_shop() -> str:
    request = urllib.request.Request(
        SHOP_URL,
        headers={"User-Agent": "APUNOKAGI website product sync/1.0"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def product_feed(html: str) -> dict:
    parser = NextDataParser()
    parser.feed(html)
    if not parser.parts:
        raise RuntimeError("Minne page did not contain __NEXT_DATA__")

    payload = json.loads("".join(parser.parts))
    page = payload["props"]["pageProps"]
    products = []

    for item in page.get("products", []):
        if not item.get("saleFlg") or item.get("isSoldout"):
            continue
        photo = item.get("photo") or {}
        image = photo.get("largeUrl") or photo.get("baseUrl") or ""
        if image.startswith("//"):
            image = "https:" + image
        stock = item.get("stockNum")
        products.append(
            {
                "id": int(item["id"]),
                "name": item.get("productName", ""),
                "price": int(item.get("price") or 0),
                "image": image,
                "url": f"https://minne.com/items/{item['id']}",
                "stock": stock if isinstance(stock, int) else None,
                "oneOfAKind": stock == 1,
                "startedSellingAt": item.get("startedSellingAt"),
            }
        )

    return {
        "shop": SHOP_URL,
        "syncedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "count": len(products),
        "products": products,
    }


def main() -> int:
    try:
        feed = product_feed(fetch_shop())
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(
            json.dumps(feed, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"Synced {feed['count']} available Minne products to {OUTPUT}")
        return 0
    except Exception as error:
        print(f"Minne sync failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
