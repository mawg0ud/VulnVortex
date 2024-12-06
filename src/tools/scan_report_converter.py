import json
import xml.etree.ElementTree as ET
import csv
import yaml
from typing import Dict, Union
import logging


class ScanReportConverter:
    """
    A utility class to convert scan reports between various formats.

    Supported Formats:
    - JSON
    - XML
    - CSV
    - YAML

    Features:
    - Flexible format conversion with validation.
    - Error handling with descriptive messages.
    - Extendable to support additional formats.
    - Generates summaries of the converted reports.
    """

    def __init__(self):
        self.logger = logging.getLogger("ScanReportConverter")
        self.logger.setLevel(logging.INFO)

    def convert(self, input_file: str, output_file: str, output_format: str):
        """
        Convert a scan report from one format to another.

        Args:
            input_file (str): Path to the input file.
            output_file (str): Path to the output file.
            output_format (str): Desired output format (json, xml, csv, yaml).

        Raises:
            ValueError: If the output format is not supported or conversion fails.
        """
        self.logger.info(f"Starting conversion: {input_file} -> {output_file} ({output_format})")

        # Load the input file
        data = self._load_file(input_file)
        if data is None:
            raise ValueError("Failed to load input file.")

        # Save the file in the desired format
        self._save_file(data, output_file, output_format)
        self.logger.info(f"Conversion completed successfully: {output_file}")

    def _load_file(self, file_path: str) -> Union[Dict, list]:
        """
        Load the contents of a file into a Python dictionary or list.

        Args:
            file_path (str): Path to the file.

        Returns:
            Union[Dict, list]: Parsed data from the file.
        """
        try:
            if file_path.endswith(".json"):
                with open(file_path, "r") as file:
                    self.logger.debug(f"Loading JSON file: {file_path}")
                    return json.load(file)

            elif file_path.endswith(".yaml") or file_path.endswith(".yml"):
                with open(file_path, "r") as file:
                    self.logger.debug(f"Loading YAML file: {file_path}")
                    return yaml.safe_load(file)

            elif file_path.endswith(".xml"):
                self.logger.debug(f"Loading XML file: {file_path}")
                return self._parse_xml(file_path)

            elif file_path.endswith(".csv"):
                self.logger.debug(f"Loading CSV file: {file_path}")
                return self._parse_csv(file_path)

            else:
                raise ValueError("Unsupported input file format.")
        except Exception as e:
            self.logger.error(f"Error loading file {file_path}: {e}")
            return None

    def _save_file(self, data: Union[Dict, list], file_path: str, format: str):
        """
        Save data to a file in the specified format.

        Args:
            data (Union[Dict, list]): Data to save.
            file_path (str): Path to the output file.
            format (str): Format to save the file in (json, xml, csv, yaml).

        Raises:
            ValueError: If the format is not supported.
        """
        try:
            if format == "json":
                with open(file_path, "w") as file:
                    self.logger.debug(f"Saving JSON file: {file_path}")
                    json.dump(data, file, indent=4)

            elif format == "yaml":
                with open(file_path, "w") as file:
                    self.logger.debug(f"Saving YAML file: {file_path}")
                    yaml.safe_dump(data, file)

            elif format == "xml":
                self.logger.debug(f"Saving XML file: {file_path}")
                self._write_xml(data, file_path)

            elif format == "csv":
                self.logger.debug(f"Saving CSV file: {file_path}")
                self._write_csv(data, file_path)

            else:
                raise ValueError("Unsupported output file format.")
        except Exception as e:
            self.logger.error(f"Error saving file {file_path}: {e}")
            raise

    def _parse_xml(self, file_path: str) -> Dict:
        """
        Parse an XML file into a Python dictionary.

        Args:
            file_path (str): Path to the XML file.

        Returns:
            Dict: Parsed data.
        """
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            def element_to_dict(element):
                return {
                    element.tag: element.text if len(element) == 0 else {child.tag: element_to_dict(child) for child in element}
                }

            return element_to_dict(root)
        except Exception as e:
            self.logger.error(f"Error parsing XML file {file_path}: {e}")
            raise

    def _parse_csv(self, file_path: str) -> List[Dict]:
        """
        Parse a CSV file into a list of dictionaries.

        Args:
            file_path (str): Path to the CSV file.

        Returns:
            List[Dict]: Parsed data.
        """
        try:
            with open(file_path, "r") as file:
                reader = csv.DictReader(file)
                return [row for row in reader]
        except Exception as e:
            self.logger.error(f"Error parsing CSV file {file_path}: {e}")
            raise

    def _write_xml(self, data: Dict, file_path: str):
        """
        Write data to an XML file.

        Args:
            data (Dict): Data to write.
            file_path (str): Path to the XML file.
        """
        try:
            def dict_to_element(tag, content):
                element = ET.Element(tag)
                if isinstance(content, dict):
                    for key, value in content.items():
                        element.append(dict_to_element(key, value))
                else:
                    element.text = str(content)
                return element

            root_tag = list(data.keys())[0]
            root_element = dict_to_element(root_tag, data[root_tag])

            tree = ET.ElementTree(root_element)
            tree.write(file_path, encoding="utf-8", xml_declaration=True)
        except Exception as e:
            self.logger.error(f"Error writing XML file {file_path}: {e}")
            raise

    def _write_csv(self, data: List[Dict], file_path: str):
        """
        Write data to a CSV file.

        Args:
            data (List[Dict]): Data to write.
            file_path (str): Path to the CSV file.
        """
        try:
            if not data or not isinstance(data, list) or not isinstance(data[0], dict):
                raise ValueError("Invalid data format for CSV output.")

            with open(file_path, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
        except Exception as e:
            self.logger.error(f"Error writing CSV file {file_path}: {e}")
            raise


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)

    converter = ScanReportConverter()
    converter.convert(
        input_file="scan_report.json",
        output_file="scan_report.yaml",
        output_format="yaml"
    )
