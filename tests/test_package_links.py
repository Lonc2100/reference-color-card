from pathlib import Path
import unittest, re
class PackageLinks(unittest.TestCase):
 def test_entrypoint_references_resolve(self):
  root=Path(__file__).resolve().parents[1]
  links=re.findall(r"\]\(([^)]+)\)",(root/'SKILL.md').read_text(encoding='utf-8'))
  self.assertTrue(links)
  for link in links:
   if not link.startswith(('http:','https:','#')):
    self.assertTrue((root/link).is_file(),link)
