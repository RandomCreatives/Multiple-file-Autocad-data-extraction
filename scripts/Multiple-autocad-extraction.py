import os
import pandas as pd
import ezdxf
from typing import Dict, Any

def extract_dxf_attributes(folder_path: str) -> pd.DataFrame:
    """
    Scans a folder for DXF files and extracts block attributes.
    Specifically looks for blocks (INSERT entities) containing the 'NUMEROARTICOLO' attribute.
    """
    extracted_data = {}

    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' not found.")
        return pd.DataFrame()

    print(f"Starting extraction from: {folder_path}")

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".dxf"):
            try:
                file_path = os.path.join(folder_path, filename)
                doc = ezdxf.readfile(file_path)
                modelspace = doc.modelspace()

                for entity in modelspace:
                    # Look for INSERT entities (blocks)
                    if entity.dxftype() == "INSERT":
                        # Check if the block has the key attribute 'NUMEROARTICOLO'
                        if entity.has_attrib("NUMEROARTICOLO"):
                            attributes = {}
                            # Extract all attributes of the block
                            for attrib in entity.attribs:
                                attributes[attrib.dxf.tag] = attrib.dxf.text

                            # Use 'NUMEROARTICOLO' as the unique key
                            item_id = attributes["NUMEROARTICOLO"]
                            extracted_data[item_id] = attributes
                            print(f"  Extracted item: {item_id} from {filename}")

            except Exception as e:
                print(f"  Error reading file {filename}: {e}")

    if not extracted_data:
        print("No data extracted.")
        return pd.DataFrame()

    # Create a Pandas DataFrame from the dictionary
    df = pd.DataFrame.from_dict(extracted_data, orient='index')
    return df

if __name__ == "__main__":
    # Example usage:
    # Use the 'prof' folder in the current directory
    target_folder = "prof"
    output_csv = os.path.join(target_folder, "extraction_results.csv")

    results_df = extract_dxf_attributes(target_folder)

    if not results_df.empty:
        results_df.to_csv(output_csv, sep=';', index=False)
        print(f"\nSuccess! Results saved to: {output_csv}")
    else:
        print("\nExtraction failed or no relevant data found.")
