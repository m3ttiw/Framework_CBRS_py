from src.content_analyzer.content_representation.content_field import FeaturesBagField
from src.content_analyzer.field_content_production_techniques.field_content_production_technique import TfIdfTechnique
from src.content_analyzer.memory_interfaces.text_interface import IndexInterface
from src.content_analyzer.raw_information_source import RawInformationSource
from src.utils.id_merger import id_merger


class LuceneTfIdf(TfIdfTechnique):
    """
    Class that produces a Bag of words with tf-idf metric
    """

    def __init__(self):
        super().__init__()
        self.__index = IndexInterface('./frequency-index')

    def __str__(self):
        return "LuceneTfIdf"

    def __repr__(self):
        return "< LuceneTfIdf: " + "index = " + str(self.__index) + ">"

    def produce_content(self, field_representation_name: str, content_id: str,
                        field_name: str, pipeline_id: str) -> FeaturesBagField:
        return FeaturesBagField(field_representation_name, self.__index.get_tf_idf(field_name + pipeline_id, content_id))

    def dataset_refactor(self, information_source: RawInformationSource, id_field_names: str):
        """
        This method restructures the raw data in a way functional to the final representation.
        This is done only for those field representations that require this phase to be done.
        Args:
            information_source (RawInformationSource):
            id_field_names:

        """
        if len(self.get_need_refactor().keys()) != 0:
            self.__index = IndexInterface('./frequency-index')
            self.__index.init_writing()
            for raw_content in information_source:
                self.__index.new_content()
                id_values = []

                for name in id_field_names:
                    id_values.append(raw_content[name])

                self.__index.new_field("content_id", id_merger(id_values))

                for (field_name, pipeline_id) in self.get_need_refactor().keys():
                    preprocessor_list = self.get_need_refactor()[(field_name, pipeline_id)]
                    processed_field_data = raw_content[field_name]
                    for preprocessor in preprocessor_list:
                        processed_field_data = preprocessor.process(processed_field_data)
                    self.__index.new_field(field_name + pipeline_id, processed_field_data)
                self.__index.serialize_content()

            self.__index.stop_writing()