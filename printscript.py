#!env python
"""ink_master_5000: simple script that informs you about remaining ink supply"""

import json
import subprocess
from pathlib import Path

from xdg.BaseDirectory import xdg_config_home as xdghomeconfdir

# requirements:
# - ipptool
# - posix compatible system


def main():
    """main function"""
    confdir = Path(xdghomeconfdir+"/inkmaster")
    confdir.mkdir(parents=True, exist_ok=True)
    ipp_conf_dir = setup_ipp(confdir)
    printer = setup_printer(confdir)

    ink_info(ipp_conf_dir, printer)


def setup_ipp(confdir: Path):
    """checks for ipp conf file and returns its contents"""
    ipp_conf = Path(confdir / "colors.ipp")
    if not ipp_conf.exists():
        ipp_conf.touch()
        print("writing colors.ipp ...")
        ipp_conf.write_text(get_ipp_conf())
    return ipp_conf


def setup_printer(confdir: Path):
    """checks for printer conf and returns its contents"""
    printer_conf = Path(confdir / "printer.conf")
    if not printer_conf.exists():
        printer = str(input("Enter printer network address: "))
        printer_conf.write_text(printer, encoding="utf-8")
    return printer_conf.read_text(encoding="utf-8")


def ink_info(ipp_conf: Path, printer):
    """prints cartidge consumption percentage acquired from ipptool program"""
    command = ["ipptool", "-v", "-t", "-j", f"ipp://{printer}", ipp_conf]
    try:
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True
        )
        decoded_output = result.stdout.decode("utf-8")

        try:
            data_json = json.loads(decoded_output)

            for item in data_json:
                for name, level in zip(
                    item.get("marker-names", []), item.get("marker-levels", [])
                ):
                    print(f"{name}: {level}%")

        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
    except subprocess.CalledProcessError as e:
        print(
            f"Command failed with exit code {
                e.returncode}, stderr: {e.stderr.decode('utf-8')}"
        )


def get_ipp_conf():
    """returns ipp script"""
    ipp_content = """
{
    VERSION 2.0
    OPERATION Get-Printer-Attributes

    GROUP operation-attributes-tag
    ATTR charset "attributes-charset" "utf-8"
    ATTR naturalLanguage "attributes-natural-language" "en"
    ATTR uri "printer-uri" $uri
    ATTR name "requesting-user-name" "John Doe"
    ATTR keyword "requested-attributes" "marker-colors","marker-high-levels","marker-levels","marker-low-levels","marker-names","marker-types"
}
    """
    return ipp_content


if __name__ == "__main__":
    main()
