import unittest
import io
import ezdxf
from backend.app.services.dxf_service import DXFService

class TestDXFService(unittest.TestCase):
    def test_extraction(self):
        # Create a simple DXF in memory with a block and attributes
        doc = ezdxf.new('R2010')
        doc.blocks.new(name='TEST_BLOCK')
        block = doc.blocks.get('TEST_BLOCK')
        block.add_attdef(tag='TAG1', text='DEFAULT')

        msp = doc.modelspace()
        block_ref = msp.add_blockref('TEST_BLOCK', (0, 0))
        block_ref.add_attrib('TAG1', 'EXTRACTED_VALUE')

        # Use a StringIO to get the DXF content as string, then encode to bytes
        out = io.StringIO()
        doc.write(out)
        dxf_content = out.getvalue().encode('utf-8')

        results = DXFService.extract_attributes(dxf_content)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['TAG1'], 'EXTRACTED_VALUE')

if __name__ == '__main__':
    unittest.main()
