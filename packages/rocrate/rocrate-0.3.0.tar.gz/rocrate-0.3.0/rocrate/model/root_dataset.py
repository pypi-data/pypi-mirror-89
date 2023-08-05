#!/usr/bin/env python

# Copyright 2019-2020 The University of Manchester, UK
# Copyright 2020 Vlaams Instituut voor Biotechnologie (VIB), BE
# Copyright 2020 Barcelona Supercomputing Center (BSC), ES
# Copyright 2020 Center for Advanced Studies, Research and Development in Sardinia (CRS4), IT
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime

from .dataset import Dataset


class RootDataset(Dataset):

    def __init__(self, crate, properties=None):
        default_properties = {
            'datePublished': datetime.datetime.now().isoformat()
        }
        if properties:
            default_properties.update(properties)
        super(RootDataset, self).__init__(crate, None, './',
                                          default_properties)

    def format_id(self, identifier):
        return './'

    def _empty(self):
        # Hard-coded bootstrap for now
        val = {
            "@id": "./",
            "@type": "Dataset",
        }
        return val

    # def write(self, base_path):
        # os.mkdir(base_path)

    def properties(self):
        parts = []
        for entity in self.crate.data_entities:
            parts.append(entity.reference())
        properties = self._jsonld
        properties.update({'hasPart': parts})
        return properties
