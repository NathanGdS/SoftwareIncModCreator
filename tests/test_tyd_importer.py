import unittest
from tyd_importer import TydImporter

class TestTydImporter(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.sample_tyd_content = '''
        Name "Test Software"
        Description "A test software"
        Iterative "True"
        OptimalDevTime "10"
        Popularity "1"
        Random "False"
        Retention "0.5"
        OSSpecific "Computer"
        InHouse "False"
        IdealPrice "50"
        NameGenerator "name_gen.txt"
        SubmarketNames [
            "Market1";
            "Market2"
        ]
        Features [
            {
                Name "Feature1"
                Spec "True"
                Description "Test feature"
                Dependencies ["Dep1"; "Dep2"]
                Unlock "1990"
                DevTime "5"
                CodeArt "0.8"
                Server "False"
                Optional "True"
                Categories ["Cat1"; "Cat2"]
                Submarkets ["Sub1"; "Sub2"]
                Features [
                    {
                        Name "SubFeature1"
                        Description "Test sub-feature"
                        Level "1"
                        Unlock "1991"
                        DevTime "2"
                        CodeArt "0.5"
                        Submarkets ["SubSub1"]
                    }
                ]
            }
        ]
        '''

    def test_extract_value(self):
        """Test _extract_value method"""
        self.assertEqual(
            TydImporter._extract_value(self.sample_tyd_content, "Name"),
            "Test Software"
        )
        self.assertEqual(
            TydImporter._extract_value(self.sample_tyd_content, "Iterative"),
            "True"
        )
        self.assertEqual(
            TydImporter._extract_value(self.sample_tyd_content, "NonExistent", "default"),
            "default"
        )

    def test_split_blocks(self):
        """Test _split_blocks method"""
        test_content = '''
        {
            block1 "value1"
        }
        {
            block2 "value2"
            {
                nested "value3"
            }
        }
        '''
        blocks = TydImporter._split_blocks(test_content)
        self.assertEqual(len(blocks), 2)
        self.assertIn("block1", blocks[0])
        self.assertIn("block2", blocks[1])
        self.assertIn("nested", blocks[1])

if __name__ == '__main__':
    unittest.main() 