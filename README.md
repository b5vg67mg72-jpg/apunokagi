# Apunokagi website

Open `index.html` in a browser to preview the website.

The public website supports Japanese, English, and Spanish. English is the default for new visitors; visitors can switch instantly between `JP`, `EN`, and `ES`, and their choice is remembered in the browser.

## Automatic Minne product sync

The public collection is generated from `https://minne.com/@apunokagi` without a
login. It includes only products that Minne publicly marks as available, with
their image, name, price, stock and direct product link.

- GitHub Actions updates `data/minne-products.json` every day at approximately
  04:17 Japan time.
- Run the **Sync Minne products** workflow manually for an immediate refresh.
- To update locally, run `python scripts/sync_minne.py` and reload the website.
- Checkout, shipping, full specifications and definitive availability remain on
  Minne.

If Minne changes its page structure, the workflow fails without replacing the
last valid product feed.

## Curated Instagram gallery

The website uses selected local photographs from `assets/instagram/` so the
brand story stays visually consistent without a Meta developer account. Every
gallery photograph links visitors to `https://www.instagram.com/apunokagi/`,
where they can see the newest posts and behind-the-scenes work.

To refresh the website gallery, add an optimized photograph to
`assets/instagram/` and update the gallery markup in `index.html`. Minne remains
the automatically synchronized source for products, prices and availability.

## Optional product manager

Open `product-manager.html` to preview manually entered product information in the same browser. The public Minne feed takes priority when it is available.

1. Enter the product name, price, and exact Minne product URL.
2. Add verified dimensions, weight, materials, capacity, lining, pocket, closure, and care instructions.
3. A product photo is optional and can be added later; the website shows a clean placeholder when no photo is supplied.
4. Turn on `この作品を公開する`.
5. Click `保存する`.
6. Open the public website and check the collection section.

Use `データを保存` regularly to download a backup of the product catalog.

## Before publishing

1. Confirm that every published product is still available.
2. Unpublish or remove sold products in `product-manager.html`.
3. Complete measurements and specifications on every Minne listing.
4. Confirm that shipping remains within three days.
5. Until you publish a product, the public website directs customers to the live Minne shop without claiming that no products are available.
6. Add genuine customer reviews only after receiving permission.

## Current working links

- Instagram: `https://www.instagram.com/apunokagi/`
- Minne shop: `https://minne.com/@apunokagi`
- Every product you publish links directly to the Minne URL you enter.

## Publish with GitHub Pages

Upload `index.html` to the root of a GitHub repository, then enable GitHub Pages under **Settings → Pages**. Select the main branch and root folder.
