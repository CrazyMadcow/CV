"""Check the generated five-page plan for missing text, assets, and footers.

Run after generate-pdf.ps1. Requires PyMuPDF. Visual inspection is still needed
for layout quality and the legibility of text embedded in the source figures.
"""

from html.parser import HTMLParser
from pathlib import Path
import re

import pymupdf


class PlanParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.pages = []
        self.current = None
        self.assets = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "section" and attrs.get("id", "").startswith("page-"):
            self.current = []
            self.pages.append(self.current)
        if tag == "img":
            self.assets.append(attrs["src"])

    def handle_endtag(self, tag):
        if tag == "section":
            self.current = None

    def handle_data(self, data):
        if self.current is not None and data.strip():
            self.current.append(data.strip())


def normalize(value):
    return re.sub(r"\s+", "", value)


def main():
    application = Path(__file__).resolve().parent
    parser = PlanParser()
    parser.feed((application / "kau-collaboration.html").read_text(encoding="utf-8"))
    missing_assets = [name for name in parser.assets if not (application / name).is_file()]
    assert not missing_assets, f"Missing assets: {missing_assets}"
    pdf = application.parent / "dist" / "Kwangwoo_Jang_KAU_Collaboration_Plan.pdf"
    with pymupdf.open(pdf) as document:
        assert len(document) == len(parser.pages) == 5, "Expected five A4 pages"
        for index, (page, source_text) in enumerate(zip(document, parser.pages), start=1):
            extracted = normalize(page.get_text())
            missing = [text for text in source_text if normalize(text) not in extracted]
            assert not missing, f"Page {index}, missing text: {missing}"
            footer = page.search_for(f"{index:02d} / 05")
            assert len(footer) == 1, f"Page {index}, missing/duplicate footer"
            bottom_margin = page.rect.height - footer[0].y1
            assert bottom_margin >= 28, f"Page {index}, footer is too low"
            assert 594 < page.rect.width < 597 and 841 < page.rect.height < 844
            print(f"Page {index}: all text present, footer margin {bottom_margin:.1f} pt, images {len(page.get_images())}")
        assert [len(page.get_images()) for page in document] == [2, 0, 0, 2, 2]
        assert "기관전체연간전략사업직접비규모" in normalize(document[2].get_text())
        assert "미래도전국방기술성과홍보기여" in normalize(document[4].get_text())
        assert "HashEye" not in document[3].get_text()
        assert "규제샌드박스" in document[3].get_text()
        assert "SolidWorks" in document[4].get_text()
        for index in [2, 3, 4]:
            assert "COLLABORATION" in document[index].get_text()
    print("PASS: five pages, six source figures, all referenced assets and text present.")


if __name__ == "__main__":
    main()
