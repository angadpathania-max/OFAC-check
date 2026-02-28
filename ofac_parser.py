"""Parse OFAC advanced XML files and extract entity/party names for screening."""
import os
import xml.etree.ElementTree as ET
from pathlib import Path

# OFAC Advanced XML default namespace (elements have no prefix in the file)
OFAC_NS = "https://sanctionslistservice.ofac.treas.gov/api/PublicationPreview/exports/ADVANCED_XML"


def _tag(name: str) -> str:
    """Return full tag name with namespace."""
    return f"{{{OFAC_NS}}}{name}"


def _get_text(el):
    """Get text from NamePartValue or similar element."""
    if el is None:
        return ""
    return (el.text or "").strip()


def parse_ofac_xml(filepath: str) -> list[dict]:
    """
    Parse a single OFAC advanced XML file and yield records with:
    - name: the party/alias name
    - fixed_ref: DistinctParty FixedRef
    - profile_id: Profile ID
    - alias_type_id: 1400 A.K.A., 1401 F.K.A., 1402 N.K.A., 1403 Name
    - source_file: basename of the XML file
    """
    filepath = os.path.abspath(filepath)
    source_name = os.path.basename(filepath)
    records = []

    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML in {filepath}: {e}") from e

    # DistinctParties > DistinctParty (default namespace)
    for dparty in root.findall(f".//{_tag('DistinctParty')}"):
        fixed_ref = dparty.get("FixedRef", "")
        for profile in dparty.findall(f".//{_tag('Profile')}"):
            profile_id = profile.get("ID", "")
            for alias in profile.findall(f".//{_tag('Alias')}"):
                alias_type_id = alias.get("AliasTypeID", "")
                for docname in alias.findall(f".//{_tag('DocumentedName')}"):
                    for part in docname.findall(f".//{_tag('DocumentedNamePart')}"):
                        npv = part.find(_tag("NamePartValue"))
                        if npv is not None:
                            name = _get_text(npv)
                            if name:
                                records.append(
                                    {
                                        "name": name,
                                        "fixed_ref": fixed_ref,
                                        "profile_id": profile_id,
                                        "alias_type_id": alias_type_id,
                                        "source_file": source_name,
                                    }
                                )
    return records


def load_all_xml_from_folder(folder: str) -> list[dict]:
    """Load all .xml files from folder and return combined list of records."""
    folder = os.path.abspath(folder)
    if not os.path.isdir(folder):
        raise FileNotFoundError(f"OFAC DB folder not found: {folder}")

    all_records = []
    for path in Path(folder).glob("*.xml"):
        try:
            records = parse_ofac_xml(str(path))
            all_records.extend(records)
        except Exception as e:
            raise RuntimeError(f"Error parsing {path}: {e}") from e
    return all_records
