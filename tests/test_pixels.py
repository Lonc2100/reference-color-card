from pathlib import Path
import unittest,tempfile,importlib.util
from PIL import Image
class PixelProvenance(unittest.TestCase):
 def test_actual_pixels_and_no_synthetic_colors(self):
  root=Path(__file__).resolve().parents[1]
  spec=importlib.util.spec_from_file_location('palette',root/'scripts/extract_card.py')
  m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  with tempfile.TemporaryDirectory() as t:
   path=Path(t)/'source.png';im=Image.new('RGB',(20,20),(16,32,48));im.paste((201,101,51),(10,0,20,20));im.save(path)
   source,data=m.extract(path)
   self.assertEqual(data['count'],2)
   self.assertEqual({tuple(s['rgb']) for s in data['swatches']},{(16,32,48),(201,101,51)})
   for s in data['swatches']:
    self.assertEqual(tuple(s['rgb']),source.getpixel(tuple(s['source_point'])))
    self.assertEqual(s['hex'],'#'+''.join(f'{x:02X}' for x in s['rgb']))
