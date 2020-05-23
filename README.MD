# archillect-scraper

Keep the last images from Archillect saved in your computer.

## Installation

Install the dependencies

```bash
pip3 install -r requirements.txt
```

## Usage

```bash
python3 scraper.py
```

## Scheduling

### Linux
Run ```crontab -e``` and append the command ``` python3 scraper.py```

### Windows
Run ```taskschd.msc``` create a new schedule for the file ```scraper schedule.bat```






## Configuration

See [config.cfg](config.cfg)
