#  Copyright (c) maiot GmbH 2020. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
"""Definition of the GCAIP Training Backend"""

from typing import Text

from zenml.core.backends.training.training_local_backend import \
    TrainingLocalBackend


class TrainingGCAIPBackend(TrainingLocalBackend):
    """
    Runs a TrainerStep on Google Cloud AI Platform.

    A training backend can be used to efficiently train a machine learning
    model on large amounts of data. Since most common machine learning models
    leverage mainly linear algebra operations under the hood, they can
    potentially benefit a lot from dedicated training hardware like Graphics
    Processing Units (GPUs) or application-specific integrated circuits
    (ASICs). Local training backends or cloud-based training backends
    like Google Cloud AI Platform (GCAIP) with or without GPU/ASIC support
    can be used.

    This backend is not implemented yet.
    """
    BACKEND_TYPE = 'gcaip'

    def __init__(
            self,
            image: Text = '',
            scale_tier: Text = 'BASIC',
            runtime_version: Text = '2.2',
            python_version: Text = '3.7',
            max_running_time: Text = '7200s',
            **kwargs):
        raise NotImplementedError('Its coming soon!')
        self.image = image
        self.scale_tier = scale_tier
        self.runtime_version = runtime_version
        self.python_version = python_version
        self.max_running_time = max_running_time
        super().__init__(**kwargs)
