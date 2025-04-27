import unittest
from mod_exporter import ModExporter

class TestModExporter(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.software_type_data = {
            "Software Name": "Test Software",
            "Description": "A test software",
            "Iterative": "True",
            "OptimalDevTime": "10",
            "Submarket Name One": "Market1",
            "Submarket Name Two": "Market2",
            "Popularity": "1",
            "Random": "False",
            "Retention": "0.5",
            "OSSpecific": "Computer",
            "InHouse": "False",
            "IdealPrice": "50",
            "NameGenerator": "name_gen.txt"
        }
        
        self.spec_feature = {
            "Name": "Feature1",
            "Spec": "True",
            "Description": "Test feature",
            "Dependencies": "Dep1; Dep2",
            "Unlock": "1990",
            "DevTime": "5",
            "CodeArt": "0.8",
            "Server": "False",
            "Optional": "True",
            "Software Categories": "Cat1; Cat2",
            "Submarket 1": "Sub1",
            "Submarket 2": "Sub2",
            "Submarket 3": ""
        }
        
        self.sub_feature = {
            "Name": "SubFeature1",
            "Description": "Test sub-feature",
            "Level": "1",
            "DevTime": "2",
            "CodeArt": "0.5",
            "Software Feature": "Feature1",
            "Submarket 1": "SubSub1",
            "Submarket 2": "",
            "Submarket 3": ""
        }

    def test_to_bool(self):
        """Test boolean conversion"""
        self.assertEqual(ModExporter.to_bool("true"), "True")
        self.assertEqual(ModExporter.to_bool("True"), "True")
        self.assertEqual(ModExporter.to_bool("false"), "False")
        self.assertEqual(ModExporter.to_bool("anything"), "False")

    def test_add_field_if_exists(self):
        """Test field addition"""
        # Test normal field
        result = ModExporter._add_field_if_exists({"test": "value"}, "test")
        self.assertEqual(result, '\n    test "value"')
        
        # Test boolean field
        result = ModExporter._add_field_if_exists({"test": "true"}, "test", bool_field=True)
        self.assertEqual(result, "\n    test True")
        
        # Test default value
        result = ModExporter._add_field_if_exists({}, "test", "default")
        self.assertEqual(result, "")

    def test_add_array_if_exists(self):
        """Test array addition"""
        data = {
            "field1": "value1",
            "field2": "value2",
            "field3": ""
        }
        result = ModExporter._add_array_if_exists(
            data,
            "ArrayName",
            ["field1", "field2", "field3"]
        )
        self.assertEqual(result, "\n    ArrayName [ value1; value2 ]")

    def test_export_mod_structure(self):
        """Test the structure of exported mod content"""
        # Create a temporary string to hold the export content
        export_content = ModExporter.export_mod_to_string(
            self.software_type_data,
            [self.spec_feature],
            [self.sub_feature]
        )
        
        # Test basic structure
        self.assertIn('SoftwareType', export_content)
        self.assertIn('Name "Test Software"', export_content)
        self.assertIn('Category "Development"', export_content)
        
        # Test feature structure
        self.assertIn('Name "Feature1"', export_content)
        self.assertIn('Spec "True"', export_content)
        
        # Test sub-feature structure
        self.assertIn('Name "SubFeature1"', export_content)
        self.assertIn('Level 1', export_content)

if __name__ == '__main__':
    unittest.main() 