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

import os
import json
import tempfile

from .file import File
from .dataset import Dataset


class Metadata(File):
    """
    RO-Crate metadata file

    This object holds the data of an RO Crate Metadata File rocrate_
    """
    BASENAME = "ro-crate-metadata.json"
    PROFILE = "https://w3id.org/ro/crate/1.1"

    def __init__(self, crate):
        super().__init__(crate, None, self.BASENAME, False, None)

    def _empty(self):
        # default properties of the metadata entry
        val = {"@id": self.BASENAME,
               "@type": "CreativeWork",
               "conformsTo": {"@id": self.PROFILE},
               "about": {"@id": "./"}}
        return val

    # Generate the crate's `ro-crate-metadata.json`.
    # @return [String] The rendered JSON-LD as a "prettified" string.
    def generate(self):
        graph = []
        for entity in self.crate.get_entities():
            graph.append(entity.properties())
        return {'@context': f'{self.PROFILE}/context', '@graph': graph}

    def write(self, base_path):
        # writes itself in
        write_path = self.filepath(base_path)
        as_jsonld = self.generate()
        with open(write_path, 'w') as outfile:
            json.dump(as_jsonld, outfile, indent=4, sort_keys=True)

    def write_zip(self, zip_out):
        write_path = self.filepath()
        as_jsonld = self.generate()
        # with open(write_path, 'w') as outfile:
        # TODO: fix this, there is no need to use a tmp file
        tmpfile = tempfile.NamedTemporaryFile(mode='w', delete=False)
        tmpfile_path = tmpfile.name
        json.dump(as_jsonld, tmpfile, indent=4, sort_keys=True)
        tmpfile.close()
        zip_out.write(tmpfile_path, write_path)
        os.remove(tmpfile_path)

    @property
    def root(self) -> Dataset:
        return self.crate.root_dataset


class LegacyMetadata(Metadata):

    BASENAME = "ro-crate-metadata.jsonld"
    PROFILE = "https://w3id.org/ro/crate/1.0"
