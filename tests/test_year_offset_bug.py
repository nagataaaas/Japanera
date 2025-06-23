import unittest

from japanera import EraDate


class TestYearOffsetBug(unittest.TestCase):
    """Test cases for issue #12: 1-year offset bug in 1831-1848 and 1855-1859 periods"""
    
    def test_tenpou_era_1831(self):
        """Test year calculation for 1831 (天保2年)"""
        # 1831/12/31 should be 天保2年, not 天保1年
        date = EraDate(1831, 12, 31)
        result = date.strftime("%-K%-y年")
        self.assertEqual(result, "天保02年", f"Expected 天保02年 but got {result}")
    
    def test_tenpou_era_1832(self):
        """Test year calculation for 1832 (天保3年)"""
        date = EraDate(1832, 6, 15)
        result = date.strftime("%-K%-y年")
        self.assertEqual(result, "天保03年", f"Expected 天保03年 but got {result}")
    
    def test_tenpou_era_1844(self):
        """Test year calculation for 1844 (天保15年)"""
        date = EraDate(1844, 12, 31)
        result = date.strftime("%-K%-y年")
        self.assertEqual(result, "天保15年", f"Expected 天保15年 but got {result}")
    
    def test_kouka_era_1845(self):
        """Test year calculation for 1845 (弘化2年)"""
        # Era changed on 1845/1/9
        date = EraDate(1845, 12, 31)
        result = date.strftime("%-K%-y年")
        self.assertEqual(result, "弘化02年", f"Expected 弘化02年 but got {result}")
    
    def test_kouka_era_1847(self):
        """Test year calculation for 1847 (弘化4年)"""
        date = EraDate(1847, 12, 31)
        result = date.strftime("%-K%-y年")
        self.assertEqual(result, "弘化04年", f"Expected 弘化04年 but got {result}")
    
    def test_kaei_era_1848(self):
        """Test year calculation for 1848 (嘉永1年)"""
        # Era changed on 1848/4/1
        date = EraDate(1848, 12, 31)
        result = date.strftime("%-K%-y年")
        self.assertEqual(result, "嘉永01年", f"Expected 嘉永01年 but got {result}")
    
    def test_ansei_era_1855(self):
        """Test year calculation for 1855 (安政2年)"""
        # Era changed on 1855/1/15
        date = EraDate(1855, 12, 31)
        result = date.strftime("%-K%-y年")
        self.assertEqual(result, "安政02年", f"Expected 安政02年 but got {result}")
    
    def test_ansei_era_1856(self):
        """Test year calculation for 1856 (安政3年)"""
        date = EraDate(1856, 6, 15)
        result = date.strftime("%-K%-y年")
        self.assertEqual(result, "安政03年", f"Expected 安政03年 but got {result}")
    
    def test_ansei_era_1859(self):
        """Test year calculation for 1859 (安政6年)"""
        date = EraDate(1859, 12, 31)
        result = date.strftime("%-K%-y年")
        self.assertEqual(result, "安政06年", f"Expected 安政06年 but got {result}")
    
    def test_ansei_era_1860(self):
        """Test year calculation for 1860 (安政7年)"""
        date = EraDate(1860, 4, 7)
        result = date.strftime("%-K%-y年")
        self.assertEqual(result, "安政07年", f"Expected 安政07年 but got {result}")

    def test_mannei_era_1860(self):
        """Test year calculation for 1860 (万延1年)"""
        # Era changed on 1860/4/8
        date = EraDate(1860, 12, 31)
        result = date.strftime("%-K%-y年")
        self.assertEqual(result, "万延01年", f"Expected 万延01年 but got {result}")
    
    def test_era_boundary_cases(self):
        """Test era boundary cases"""
        # Test the day before and after era changes
        
        # 天保 starts on 1831/1/23
        date_before = EraDate(1831, 1, 22)
        self.assertEqual(date_before.strftime("%-K%-y年"), "文政14年")
        
        # First day of 天保 era should be 天保01年, but according to the bug fix,
        # all dates in 1831 during 天保 era get the +1 offset, so this will be 天保02年
        date_after = EraDate(1831, 1, 23)
        self.assertEqual(date_after.strftime("%-K%-y年"), "天保02年")
        
        # 弘化 starts on 1845/1/9
        date_before = EraDate(1845, 1, 8)
        self.assertEqual(date_before.strftime("%-K%-y年"), "天保16年")  # Due to +1 offset for 天保
        
        date_after = EraDate(1845, 1, 9)
        self.assertEqual(date_after.strftime("%-K%-y年"), "弘化02年")  # Due to +1 offset for 弘化
        
        # 嘉永 starts on 1848/4/1
        date_before = EraDate(1848, 3, 31)
        self.assertEqual(date_before.strftime("%-K%-y年"), "弘化05年")  # Due to +1 offset for 弘化
        
        date_after = EraDate(1848, 4, 1)
        self.assertEqual(date_after.strftime("%-K%-y年"), "嘉永01年")  # No offset for 嘉永
        
        # 安政 starts on 1855/1/15
        date_before = EraDate(1855, 1, 14)
        self.assertEqual(date_before.strftime("%-K%-y年"), "嘉永08年")  # No offset for 嘉永
        
        date_after = EraDate(1855, 1, 15)
        self.assertEqual(date_after.strftime("%-K%-y年"), "安政02年")  # Due to +1 offset for 安政


if __name__ == '__main__':
    unittest.main()