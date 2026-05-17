import ezdxf
import io
from typing import List, Dict, Any

class DXFService:
    @staticmethod
    def extract_attributes(file_content: bytes) -> List[Dict[str, Any]]:
        """
        Parses a DXF file from bytes and extracts block attributes.
        Specifically looks for 'INSERT' entities (blocks) that have attributes.
        """
        try:
            # We use a temporary file to leverage ezdxf.readfile's robust encoding detection
            import tempfile
            import os

            with tempfile.NamedTemporaryFile(delete=False, suffix=".dxf") as tmp:
                tmp.write(file_content)
                tmp_path = tmp.name

            try:
                doc = ezdxf.readfile(tmp_path)
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

            modelspace = doc.modelspace()
            extracted_items = []

            for entity in modelspace:
                if entity.dxftype() == "INSERT":
                    item_data = {}
                    for attrib in entity.attribs:
                        item_data[attrib.dxf.tag] = attrib.dxf.text

                    if item_data:
                        extracted_items.append(item_data)

            return extracted_items

        except ezdxf.DXFError as e:
            print(f"DXF Parsing Error: {e}")
            raise ValueError(f"Could not parse DXF file: {str(e)}")
        except Exception as e:
            print(f"Unexpected Error during DXF extraction: {e}")
            raise e
