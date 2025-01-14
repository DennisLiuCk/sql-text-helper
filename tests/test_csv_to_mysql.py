import unittest
import os
import tempfile
from csv_to_mysql import csv_column_to_mysql_tuple, csv_to_mysql_update_script

class TestCsvToMysql(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        # Clean up temporary files
        for file in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file))
        os.rmdir(self.test_dir)
    
    def create_test_csv(self, content):
        """Helper method to create test CSV files"""
        filepath = os.path.join(self.test_dir, "test.csv")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath
    
    def test_basic_conversion(self):
        """Test basic CSV to MySQL tuple conversion with quotes"""
        csv_content = "PRODUCT_CODE\nABC123\nDEF456\nGHI789"
        filepath = self.create_test_csv(csv_content)
        
        result = csv_column_to_mysql_tuple(filepath, "PRODUCT_CODE")
        expected = "('ABC123', 'DEF456', 'GHI789')"
        self.assertEqual(result, expected)
    
    def test_without_quotes(self):
        """Test conversion without quotes"""
        csv_content = "PRODUCT_CODE\nABC123\nDEF456\nGHI789"
        filepath = self.create_test_csv(csv_content)
        
        result = csv_column_to_mysql_tuple(filepath, "PRODUCT_CODE", add_quotes=False)
        expected = "(ABC123, DEF456, GHI789)"
        self.assertEqual(result, expected)
    
    def test_column_with_spaces(self):
        """Test handling of column names with spaces"""
        csv_content = "Product Code\nABC123\nDEF456"
        filepath = self.create_test_csv(csv_content)
        
        result = csv_column_to_mysql_tuple(filepath, "Product Code")
        expected = "('ABC123', 'DEF456')"
        self.assertEqual(result, expected)
    
    def test_case_insensitive_column(self):
        """Test case-insensitive column name matching"""
        csv_content = "PRODUCT_CODE\nABC123\nDEF456"
        filepath = self.create_test_csv(csv_content)
        
        result = csv_column_to_mysql_tuple(filepath, "product_code")
        expected = "('ABC123', 'DEF456')"
        self.assertEqual(result, expected)
    
    def test_empty_column(self):
        """Test handling of empty column values"""
        csv_content = "PRODUCT_CODE\nABC123\n\nDEF456"
        filepath = self.create_test_csv(csv_content)
        
        result = csv_column_to_mysql_tuple(filepath, "PRODUCT_CODE")
        expected = "('ABC123', 'DEF456')"  # Empty value should be filtered out
        self.assertEqual(result, expected)
    
    def test_column_not_found(self):
        """Test behavior when column is not found"""
        csv_content = "PRODUCT_CODE\nABC123"
        filepath = self.create_test_csv(csv_content)
        
        result = csv_column_to_mysql_tuple(filepath, "NONEXISTENT")
        self.assertIsNone(result)
    
    def test_file_not_found(self):
        """Test behavior with nonexistent file"""
        result = csv_column_to_mysql_tuple("nonexistent.csv", "PRODUCT_CODE")
        self.assertIsNone(result)
    
    def test_update_script_generation(self):
        """Test CSV to MySQL update script generation"""
        csv_content = "id,name,age\n1,'may',10\n2,'Allen',15"
        filepath = self.create_test_csv(csv_content)
        
        result = csv_to_mysql_update_script(filepath, "user")
        expected = "Update user set name = 'may', age = 10 where id = 1;\nUpdate user set name = 'Allen', age = 15 where id = 2;"
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
