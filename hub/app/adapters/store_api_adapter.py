import json
import logging
from typing import List

import pydantic_core
import requests

from app.entities.processed_agent_data import ProcessedAgentData
from app.interfaces.store_gateway import StoreGateway


class StoreApiAdapter(StoreGateway):
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    def save_data(self, processed_agent_data_batch: List[ProcessedAgentData]):
        """
        Save the processed road data to the Store API.
        Parameters:
            processed_agent_data_batch (dict): Processed road data to be saved.
        Returns:
            bool: True if the data is successfully saved, False otherwise.
        """
        link = f"{self.api_base_url}/processed_agent_data"
        data = [data.model_dump_json() for data in processed_agent_data_batch]
        header = {'Content-Type': 'application/json'}
        with requests.post(link, '[' + ','.join(data) + ']', header) as response:
            if response.status_code == 200:
                return True
            logging.error(f"Error. Passed data: {data}\nResponse: {response}")
            return False
