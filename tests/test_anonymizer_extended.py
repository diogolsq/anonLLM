import unittest
import re
from anonLLM.anonymizer_extended import AnonymizerExtended



class TestAnonymizerExtended(unittest.TestCase):

    def setUp(self):
        self.anonymizer = AnonymizerExtended() 

    def match(self, pattern, text):
        match = re.search(pattern, text)
        return match.group(1) if match else None


    def extract_info(self, text):
        name_pattern = r"My name is ([\w\s]+),"
        email_pattern = r"email: ([\w\.-]+@[\w\.-]+),"
        phone_pattern = r"phone: ([\+\d\s\-]+)\."
        gps_pattern = r"coordinates: (\d+\.\d+ N, \d+\.\d+ W)"
        bank_account_pattern = r"bank account: (\d{4}-\d{4}-\d{4}-\d{4})"
        id_pattern = r"ID: (\w+)"
        credit_card_pattern = r"credit card: (\d{4} \d{4} \d{4} \d{4})"
        address_pattern = r"address: ([\w\s,]+)"

        name = self.match(name_pattern, text)
        email = self.match(email_pattern, text)
        phone = self.match(phone_pattern, text)
        gps = self.match(gps_pattern, text)
        bank_account =self.match(bank_account_pattern, text)
        id_ = self.match(id_pattern, text)
        credit_card = self.match(credit_card_pattern, text)
        address = self.match(address_pattern, text)

        return email, name, phone, gps, bank_account, id_, credit_card, address
 

    def test_anonymize_data_extended(self):
        test_examples = [
            "My coordinates: 40.7128 N, 74.0060 W, bank account: 1234-5678-9101-1121, ID: ABC123, credit card: 1234 5678 9101 1121, address: 123 Main St, Springfield", 
            "Here is the information of John, user_id: 53321, can you validate why he is not appearing in our final list?", 
            "json: {\"user_id\": \"53321\", \"name\": \"John\", \"email\": \", \"phone\": \", \"coordinates\": \"40.7128 N, 74.0060 W\", \"bank_account\": \"1234-5678-9101-1121\", \"id\": \"ABC123\", \"credit_card\": \"1234 5678 9101 1121\", \"address\": \"123 Main St, Springfield\"}"
        ]

        for example in test_examples:
            anonymized_text, _ = self.anonymizer.anonymize_data(example)

            name, email, phone, gps, bank_account, id_, credit_card, address = self.extract_info(example)

            if name: self.assertNotIn(name, anonymized_text)
            if email: self.assertNotIn(email, anonymized_text)
            if phone: self.assertNotIn(phone, anonymized_text)
            if gps: self.assertNotIn(gps, anonymized_text)
            if bank_account: self.assertNotIn(bank_account, anonymized_text)
            if id_: self.assertNotIn(id_, anonymized_text)
            if credit_card: self.assertNotIn(credit_card, anonymized_text)
            if address: self.assertNotIn(address, anonymized_text)



if __name__ == "__main__":
    unittest.main()