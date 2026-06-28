"""Scrape and display data about the invention of the computer.

This example uses Beautiful Soup to extract structured records from HTML.
The page data is included in the script so the output is always available,
even when internet access is blocked.
"""

from __future__ import annotations

from dataclasses import dataclass

from bs4 import BeautifulSoup


HTML_DATA = """
<html>
  <body>
    <h1>Invention and Development of Computers</h1>

    <div class="computer-record">
      <h2>Abacus</h2>
      <p class="inventor">Inventor/Origin: Ancient Mesopotamia, China, and other early civilizations</p>
      <p class="year">Period: Around 2400 BCE</p>
      <p class="details">The abacus was one of the earliest known calculating devices. It helped people perform arithmetic before mechanical or electronic computers existed.</p>
    </div>

    <div class="computer-record">
      <h2>Pascaline</h2>
      <p class="inventor">Inventor/Origin: Blaise Pascal</p>
      <p class="year">Period: 1642</p>
      <p class="details">The Pascaline was a mechanical calculator created to add and subtract numbers. It is considered an important step toward automatic calculation.</p>
    </div>

    <div class="computer-record">
      <h2>Analytical Engine</h2>
      <p class="inventor">Inventor/Origin: Charles Babbage</p>
      <p class="year">Period: 1830s</p>
      <p class="details">Charles Babbage designed the Analytical Engine, a proposed general-purpose mechanical computer. It included ideas similar to a processor, memory, and input/output.</p>
    </div>

    <div class="computer-record">
      <h2>First Computer Program</h2>
      <p class="inventor">Inventor/Origin: Ada Lovelace</p>
      <p class="year">Period: 1843</p>
      <p class="details">Ada Lovelace wrote notes for Babbage's Analytical Engine and described an algorithm for it. She is often called the first computer programmer.</p>
    </div>

    <div class="computer-record">
      <h2>ENIAC</h2>
      <p class="inventor">Inventor/Origin: J. Presper Eckert and John Mauchly</p>
      <p class="year">Period: 1945</p>
      <p class="details">ENIAC was one of the first general-purpose electronic digital computers. It was used for large mathematical calculations and showed the power of electronic computing.</p>
    </div>
  </body>
</html>
"""


@dataclass
class ComputerHistoryRecord:
    invention: str
    inventor: str
    period: str
    details: str


def clean_label(text: str) -> str:
    return text.split(":", 1)[-1].strip()


def scrape_computer_history(html: str) -> tuple[str, list[ComputerHistoryRecord]]:
    soup = BeautifulSoup(html, "html.parser")
    heading = soup.find("h1")
    title = heading.get_text(strip=True) if heading else "Computer Invention Data"
    records: list[ComputerHistoryRecord] = []

    for item in soup.select(".computer-record"):
        invention = item.find("h2").get_text(strip=True)
        inventor = clean_label(item.select_one(".inventor").get_text(strip=True))
        period = clean_label(item.select_one(".year").get_text(strip=True))
        details = item.select_one(".details").get_text(strip=True)

        records.append(
            ComputerHistoryRecord(
                invention=invention,
                inventor=inventor,
                period=period,
                details=details,
            )
        )

    return title, records


def main() -> None:
    title, records = scrape_computer_history(HTML_DATA)

    print(f"Topic: {title}")
    print(f"Records found: {len(records)}\n")

    for index, record in enumerate(records, start=1):
        print(f"{index}. {record.invention}")
        print(f"   Inventor/Origin: {record.inventor}")
        print(f"   Year/Period: {record.period}")
        print(f"   Details: {record.details}\n")


if __name__ == "__main__":
    main()
