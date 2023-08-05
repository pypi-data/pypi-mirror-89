# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# coding: utf-8

"""
    Kubeflow Pipelines API

    This file contains REST API specification for Kubeflow Pipelines. The file is autogenerated from the swagger definition.

    Contact: kubeflow-pipelines@google.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import kfp_server_api
from kfp_server_api.api.experiment_service_api import ExperimentServiceApi  # noqa: E501
from kfp_server_api.rest import ApiException


class TestExperimentServiceApi(unittest.TestCase):
    """ExperimentServiceApi unit test stubs"""

    def setUp(self):
        self.api = kfp_server_api.api.experiment_service_api.ExperimentServiceApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_archive_experiment(self):
        """Test case for archive_experiment

        Archives an experiment and the experiment's runs and jobs.  # noqa: E501
        """
        pass

    def test_create_experiment(self):
        """Test case for create_experiment

        Creates a new experiment.  # noqa: E501
        """
        pass

    def test_delete_experiment(self):
        """Test case for delete_experiment

        Deletes an experiment without deleting the experiment's runs and jobs. To avoid unexpected behaviors, delete an experiment's runs and jobs before deleting the experiment.  # noqa: E501
        """
        pass

    def test_get_experiment(self):
        """Test case for get_experiment

        Finds a specific experiment by ID.  # noqa: E501
        """
        pass

    def test_list_experiment(self):
        """Test case for list_experiment

        Finds all experiments. Supports pagination, and sorting on certain fields.  # noqa: E501
        """
        pass

    def test_unarchive_experiment(self):
        """Test case for unarchive_experiment

        Restores an archived experiment. The experiment's archived runs and jobs will stay archived.  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
