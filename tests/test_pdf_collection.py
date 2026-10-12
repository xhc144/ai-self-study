"""Joining PDFs must preserve both explicit and named internal links."""
import importlib.util,tempfile,unittest
from pathlib import Path
@unittest.skipUnless(importlib.util.find_spec('fitz'),'optional build dependency PyMuPDF not installed')
class PDFCollection(unittest.TestCase):
    def fixture(self,folder,named=False):
        import fitz
        d=fitz.open();d.new_page(width=612,height=792);d.new_page(width=612,height=792)
        d[0].insert_link({'kind':fitz.LINK_GOTO,'from':fitz.Rect(10,10,80,30),'page':1,'to':fitz.Point(30,50)})
        first=folder/'initial.pdf';d.save(first);d.close()
        d=fitz.open(first)
        if named:
            d.xref_set_key(d.pdf_catalog(),'Names',f'<< /Dests << /Names [(target) [{d.page_xref(1)} 0 R /XYZ 30 742 0]] >> >>')
            xref=d[0].get_links()[0]['xref'];d.xref_set_key(xref,'A','<< /S /GoTo /D (target) >>');d.xref_set_key(xref,'Dest','null')
        p=folder/('named.pdf' if named else 'explicit.pdf');d.save(p);d.close();return p
    def check(self,named):
        import fitz
        from scripts.build_collection import merge
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp);src=self.fixture(folder,named);out=folder/'merged.pdf'
            d=fitz.open(src);self.assertEqual(d[0].get_links()[0]['kind'],fitz.LINK_NAMED if named else fitz.LINK_GOTO);d.close()
            merge([('first',src),('second',src)],out,'test');d=fitz.open(out)
            for source,dest in [(0,1),(2,3)]:
                links=d[source].get_links();self.assertEqual(len(links),1);a=links[0]
                self.assertEqual(a['kind'],fitz.LINK_GOTO);self.assertEqual(a['page'],dest)
                self.assertAlmostEqual(a['to'].x,30,places=3);self.assertAlmostEqual(a['to'].y,50,places=3)
            self.assertEqual(len(d.get_toc()),2);d.close()
    def test_explicit_page_offset(self):self.check(False)
    def test_named_destination_is_resolved_not_discarded(self):self.check(True)
