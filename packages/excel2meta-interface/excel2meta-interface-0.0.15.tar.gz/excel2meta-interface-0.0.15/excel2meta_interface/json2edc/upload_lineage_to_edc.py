from excel2meta_interface.utils import messages
# import informatica_edc_rest_api_samples
from edc_rest_api.metadata_utilities import load_json_metadata
import glob


class UploadLineageToEDC:
    def __init__(self):
        self.result = messages.message["ok"]
        self.config_directory = "lineage_output/one-on-one/config/"

    def upload_lineage(self):
        print("Uploading lineage to EDC with config files in >%s<" % self.config_directory)
        for file in glob.glob(self.config_directory + "config_for_*.json"):
            print("Lineage processing with configuration file >%s<" % file)
            load_json = load_json_metadata.ConvertJSONtoEDCLineage(configuration_file=file)
            load_json.main(ignore_metafile_creation=True)


if __name__ == "__main__":
    UploadLineageToEDC().upload_lineage()
