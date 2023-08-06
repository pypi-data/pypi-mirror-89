from typing import Optional
import yaml

from pyrasgo.connection import Connection
from pyrasgo.monitoring import track_usage
from pyrasgo.rasgo import Rasgo

class RasgoOrchestration(Connection):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rasgo = Rasgo(api_key=self._api_key)

    @track_usage
    def simulate_orchestration(self, source_table: str, func):
        '''
        Run a python function against a source table
        
        param source_table: Snowflake table holding raw data
        param func: function containing feature transformation code (should be named generate_feature)

        return: Success or Failure message
        '''
        df = self.rasgo.get_source_table(table_name=source_table, record_limit=-1)
        dx = func(df)
        return f'Code successfully created dataframe with shape {dx.shape}'

    @track_usage
    def publish_features_from_yml(self, yml_file: str, orchestrationStatus: Optional[str]='Sandboxed', gitRepo: Optional[str]=None):
        '''
        Creates a featureset from a yml file

        :param yml_file: Rasgo compliant yml file that describes the featureset(s) being created
        :param orchestrationStatus: Sandboxed or Productionized
        :return: description of the featureset created
        '''

        with open(yml_file) as fobj:
            featuresets = yaml.load(fobj, Loader=yaml.SafeLoader)
        for fs in featuresets:
            # publish featureset
            member = self.rasgo.get_member()
            org_id = member.organization_id()
            datasource = self.rasgo.publish_datasource(org_id, fs["datasource"])
            featureset_name = fs.get("name", fs["table"])
            snowflake_table = fs["table"]
            if not snowflake_table:
                raise Exception("A valid table name is required")
            granularity = fs.get('granularity')
            tags = list()
            if fs.get('tags'):
                for t in fs.get('tags'):
                    tags.append(t)
            featureset = self.rasgo.publish_feature_set(name=featureset_name, datasource_id=datasource['id'], table_name=snowflake_table, org_id=org_id, granularity=granularity)

            return_featureset = {}
            return_featureset['id'] = featureset['id']
            return_featureset['name'] = featureset['name']
            return_featureset['granularity'] = featureset['granularity']
            return_featureset['snowflakeTable'] = featureset['snowflakeTable']
            if featureset['dataSource']:
                return_featureset['dataSource'] = featureset['dataSource']['name']
            if featureset['organizationId']:
                return_featureset['organizationId'] = featureset['organizationId']
            
            # publish dimensions
            return_dimensions = {}
            for dim in fs['dimensions']:
                name = dim.get('name')
                data_type = dim.get('data_type')
                # allow granularity on a dimension to override the featureset granularity
                dim_granularity = dim.get('granularity', granularity)
                d = self.rasgo.publish_dimension(org_id, featureset['id'], name, data_type, None, dim_granularity)
                return_dimensions.update({d['id']: {"name": d['name']}})
            return_featureset['dimensions'] = return_dimensions

            # publish features
            return_features = {}
            #Note: gitRepo will be passed in from Orchestrator as a github/ or bitbucket/ path
            #      we'll want to pick up the sql/py file from the featureset yml
            gitUrl = gitRepo+fs.get('script', '') if gitRepo else fs.get('script', '')
            for feature in fs['features']:
                name = feature['display_name']
                code = feature.get('name', name)
                data_type = feature.get('data_type')
                description = feature.get('description', f"Feature that contains {name} data")
                # apply featureset tags to all features...
                feature_tags = list()
                feature_tags += tags
                # ...and add feature-specific tags
                if feature.get('tags'):
                    for t in feature.get('tags'):
                        feature_tags.append(t)
                f = self.rasgo.publish_feature(org_id, featureset['id'], name, data_type, code, description, granularity,
                                         orchestrationStatus, feature_tags, gitUrl)
                return_features.update({f['id']:
                                            {"id": f['id'],
                                             "name": f['name'],
                                             "column": f['code']
                                             }})
            return_featureset['features'] = return_features
        return return_featureset

    @track_usage
    def run_stats_for_feature(self, feature_id: int):
        '''
        Triggers stats generation for a feature
        
        param feature_id: ID of the feature to build
        '''
        return self.rasgo.post_feature_stats(feature_id)

    @track_usage
    def run_stats_for_featureset(self, featureset_id: int):
        '''
        Triggers stats generation for a feature
        
        param feature_id: ID of the feature to build
        '''
        return self.rasgo.post_feature_set_stats(featureset_id)
    
    @track_usage
    def get_featureset_id(self, snowflakeTable: str):
        fs = self._get(f"/feature-sets/", {"source_table": snowflakeTable}, api_version=1).json()
        #TODO: v0 assume a 1:1 relationship btw featureset and snowflake table 
        # If we ever see >1 featuresets built against a single table we will need to revisit this logic
        return fs[0]["id"] if fs else None