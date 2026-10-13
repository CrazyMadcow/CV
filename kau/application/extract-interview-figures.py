"""Render selected figure regions from the applicant's interview PDF.

Usage: python extract-interview-figures.py --source PATH_TO_INTERVIEW_PDF
Coordinates are PDF points. These are direct crops, with no retouching.
The SolidWorks illustration is extracted as the original embedded image,
without the presentation's overlapping text. The regulatory-sandbox concept
figure is cropped from the article screenshot embedded on slide 18.
Optional --forest-source crops the operational flow from forestry slide 4.
Requires PyMuPDF; the source PDF is intentionally not included in this package.
"""

import argparse
from pathlib import Path

import pymupdf


FIGURES = (
    (6, (543, 280, 819, 437), "interview-delay-flight.png"),
    (14, (575, 171, 810, 245), "interview-pipe-hils.png"),
    (29, (36, 204, 464, 446), "interview-wildfire-interface.png"),
    (8, (46, 178, 357, 355), "interview-hoverbike-prototype.png"),
    (28, (348, 177, 604, 330), "interview-hoverbike-system.png"),
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--forest-source", type=Path)
    args = parser.parse_args()
    output_dir = Path(__file__).resolve().parents[1] / "assets" / "img"
    output_dir.mkdir(parents=True, exist_ok=True)
    with pymupdf.open(args.source) as document:
        if len(document) < 29:
            raise ValueError("Expected the 35-page interview presentation PDF.")
        for number, coordinates, name in FIGURES:
            page = document[number - 1]
            clip = pymupdf.Rect(coordinates)
            if not page.rect.contains(clip):
                raise ValueError(f"Crop is outside page {number}: {clip}")
            page.get_pixmap(matrix=pymupdf.Matrix(3, 3), clip=clip, alpha=False).save(output_dir / name)
            print(f"Page {number}: {name}")
        cad_images = [
            item for item in document[7].get_image_info(xrefs=True)
            if item["width"] == 1156 and item["height"] == 544
            and item["bbox"][0] > 390
        ]
        if len(cad_images) != 1:
            raise ValueError("Expected one SolidWorks system illustration on slide 8.")
        pymupdf.Pixmap(document, cad_images[0]["xref"]).save(
            output_dir / "interview-hoverbike-solidworks.png"
        )
        print("Page 8: interview-hoverbike-solidworks.png (embedded original)")
        sandbox_images = [
            item for item in document[17].get_image_info(xrefs=True)
            if item["width"] == 724 and item["height"] == 621
            and item["bbox"][0] > 590
        ]
        if len(sandbox_images) != 1:
            raise ValueError("Expected the regulatory-sandbox screenshot on slide 18.")
        original = document.extract_image(sandbox_images[0]["xref"])
        # Crop the figure within the embedded screenshot, avoiding the slide's
        # overlapping section header and excluding the article headline/UI.
        with pymupdf.open() as crop_document:
            page = crop_document.new_page(width=724, height=621)
            page.insert_image(page.rect, stream=original["image"])
            page.get_pixmap(
                matrix=pymupdf.Matrix(1, 1),
                clip=pymupdf.Rect(34, 184, 685, 599), alpha=False,
            ).save(output_dir / "interview-forest-sandbox.png")
        print("Page 18: interview-forest-sandbox.png (concept figure only)")
    if args.forest_source:
        with pymupdf.open(args.forest_source) as document:
            page = document[3]
            if "탐지→판단→진화→피드백" not in page.get_text():
                raise ValueError("Expected the forestry operational flow on page 4.")
            page.get_pixmap(
                matrix=pymupdf.Matrix(3, 3),
                clip=pymupdf.Rect(62, 132, 466, 283), alpha=False,
            ).save(output_dir / "forest-project-operation.png")
            print("Forestry page 4: forest-project-operation.png")


if __name__ == "__main__":
    main()
