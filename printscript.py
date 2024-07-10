import subprocess
import json
import xdg.BaseDirectory
from pathlib import Path

# requirements:
# - ipptool
# - posix compatible system


def main():
    confdir = Path(f"{xdg.BaseDirectory.xdg_config_home}/inkscript")
    confdir.mkdir(parents=True, exist_ok=True)
    ipp_conf_dir = setup_ipp(confdir)
    printer = setup_printer(confdir)

    ink_info(ipp_conf_dir, printer)


def setup_ipp(confdir: Path):
    ipp_conf = Path(confdir / "colors.ipp")
    if not ipp_conf.exists():
        ipp_conf.touch()
        print("writing colors.ipp ...")
        ipp_conf.write_text(get_ipp_conf())
    return ipp_conf


def setup_printer(confdir: Path):
    printer_conf = Path(confdir / "printer.conf")
    if not printer_conf.exists():
        printer = str(input("Enter printer network address: "))
        printer_conf.write_text(printer)
    return printer_conf.read_text()


def ink_info(ipp_conf: Path, printer):
    command = ["ipptool", "-v", "-t", "-j", f"ipp://{printer}", ipp_conf]
    try:
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
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
