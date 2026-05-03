from API.api_client import create_api_client
from API.data_validator import validate_api_response
from urllib.parse import urlparse

class GETData:
    def __init__(self, json_data):
        """
        Initialize with dictionary of {dataset_url: query_json}
        
        Args:
            json_data: Dict where keys are full dataset URLs (e.g., 'https://andmed.stat.ee/api/v1/et/stat/RV262') 
                     and values are the JSON query objects
        """
        self.json_data = json_data
        self.response_data = dict()

    def _extract_base_url_and_dataset_id(self, full_url):
        """
        Extract base URL and dataset ID from full URL
        
        Args:
            full_url: Full URL like 'https://andmed.stat.ee/api/v1/et/stat/RV262'
            
        Returns:
            tuple: (base_url, dataset_id)
        """
        parsed = urlparse(full_url)
        base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path.rsplit('/', 1)[0]}"
        dataset_id = full_url.split('/')[-1]
        return base_url, dataset_id

    def get_data_through_API(self) -> dict:
        """
        Retrieve data for all datasets in the json_data dictionary.
        
        Returns:
            Dict where keys are dataset URLs and values are the API responses
        """
        if not self.json_data:
            print("No data requests provided")
            return {}
        
        # Process each dataset request
        for dataset_url, query_json in self.json_data.items():
            print(f"Requesting data for: {dataset_url}")
            
            # Extract base URL and dataset ID
            base_url, dataset_id = self._extract_base_url_and_dataset_id(dataset_url)
            
            # Create client for this specific base URL
            client = create_api_client(base_url=base_url)
            
            response = client.post_data(dataset_id, json_data=query_json)
            
            if response.success:
                print(f"Data retrieved successfully in {response.response_time:.2f}s")
                df, validation = validate_api_response(response.data, analysis_type="correlation")
                
                if validation.is_valid:
                    print(f"Data ready for analysis: {df.shape}")
                    self.response_data[dataset_url] = response.data
                else:
                    print(f"Validation issues: {validation.errors}")
                    # Still return the raw data even if validation fails
                    self.response_data[dataset_url] = response.data
            else:
                print(f"Request failed for {dataset_id}: {response.data}")
                print(f"Status code: {response.status_code}")
                self.response_data[dataset_url] = None
        
        return self.response_data
