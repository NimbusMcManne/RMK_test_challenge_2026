from API.api_client import create_api_client
from API.data_validator import validate_api_response

class GETData:
    def __init__(self, json_data):
        """
        Initialize with dictionary of {dataset_id: query_json}
        
        Args:
            json_data: Dict where keys are dataset IDs (e.g., 'RV262') 
                     and values are the JSON query objects
        """
        self.json_data = json_data
        self.response_data = dict()
        self.base_url = "https://andmed.stat.ee/api/v1/et/stat"

    def get_data_through_API(self) -> dict:
        """
        Retrieve data for all datasets in the json_data dictionary.
        
        Returns:
            Dict where keys are dataset IDs and values are the API responses
        """
        client = create_api_client(base_url=self.base_url)
        
        if not self.json_data:
            print("No data requests provided")
            return {}
        
        # Process each dataset request
        for dataset_id, query_json in self.json_data.items():
            print(f"Requesting data for dataset: {dataset_id}")
            
            response = client.post_data(dataset_id, json_data=query_json)
            
            if response.success:
                print(f"Data retrieved successfully in {response.response_time:.2f}s")
                df, validation = validate_api_response(response.data, analysis_type="correlation")
                
                if validation.is_valid:
                    print(f"Data ready for analysis: {df.shape}")
                    self.response_data[dataset_id] = response.data
                else:
                    print(f"Validation issues: {validation.errors}")
                    # Still return the raw data even if validation fails
                    self.response_data[dataset_id] = response.data
            else:
                print(f"Request failed for {dataset_id}: {response.data}")
                print(f"Status code: {response.status_code}")
                self.response_data[dataset_id] = None
        
        return self.response_data
        return self.response_data
