import re
from faker import Faker
import spacy
from anonLLM.anonymizer import Anonymizer


class AnonymizerExtended(Anonymizer):
    def __init__(self):
        super().__init__()

    def anonymize_data(self, sentence):
        anon_sentence, mappings = super().anonymize_data(sentence)

        # GPS Coordinates, format: "40.7128 N, 74.0060 W"
        gps_pattern = r"\b\d{1,3}\.\d{3,4}\s*[NS],?\s*\d{1,3}\.\d{3,4}\s*[EW]\b"
        
        # Bank Account Numbers, format: "1234-5678-9101-1121"
        bank_account_pattern = r"\b\d{4}-\d{4}-\d{4}-\d{4}\b"

        # IDs, format: "ID:123456"
        id_pattern = r"\bID:\d{6}\b"
        
        # Credit Cards, format: "1234 5678 9101 1121"
        credit_card_pattern = r"\b\d{4}\s\d{4}\s\d{4}\s\d{4}\b"

        # Addresses, format: "123 Main St, Springfield"
        address_pattern = r"\b\d+\s[\w\s]+,\s[\w\s]+\b"

        gps_map = {}
        bank_account_map = {}
        id_map = {}
        credit_card_map = {}
        address_map = {}

        for gps in re.findall(gps_pattern, sentence):
            fake_gps = f"{self.fake.latitude()} N, {self.fake.longitude()} W"
            gps_map[gps] = fake_gps
            anon_sentence = anon_sentence.replace(gps, fake_gps)

        for account in re.findall(bank_account_pattern, sentence):
            fake_account = f"{self.fake.random_int(min=1000, max=9999)}-{self.fake.random_int(min=1000, max=9999)}-{self.fake.random_int(min=1000, max=9999)}-{self.fake.random_int(min=1000, max=9999)}"
            bank_account_map[account] = fake_account
            anon_sentence = anon_sentence.replace(account, fake_account)

        for id in re.findall(id_pattern, sentence):
            fake_id = f"ID:{self.fake.random_int(min=100000, max=999999)}"
            id_map[id] = fake_id
            anon_sentence = anon_sentence.replace(id, fake_id)

        for cc in re.findall(credit_card_pattern, sentence):
            fake_cc = f"{self.fake.credit_card_number(card_type='mastercard')}"
            credit_card_map[cc] = fake_cc
            anon_sentence = anon_sentence.replace(cc, fake_cc)

        for addr in re.findall(address_pattern, sentence):
            fake_addr = self.fake.address().replace("\n", " ")
            address_map[addr] = fake_addr
            anon_sentence = anon_sentence.replace(addr, fake_addr)

        mappings['gps_map'] = gps_map
        mappings['bank_account_map'] = bank_account_map
        mappings['id_map'] = id_map
        mappings['credit_card_map'] = credit_card_map
        mappings['address_map'] = address_map

        return anon_sentence, mappings


