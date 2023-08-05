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
import os
import pathlib
import shutil

from .data_entity import DataEntity


class Dataset(DataEntity):

    def __init__(self, crate, source=None, dest_path=None, properties=None):
        identifier = None
        self.source = source
        if not dest_path:
            identifier = os.path.dirname(source)
        else:
            identifier = dest_path
        super().__init__(crate, identifier, properties)

    def _empty(self):
        val = {
            "@id": self.id,
            "@type": 'Dataset'
        }
        return val

    # SHOULD end with /
    def format_id(self, identifier):
        return identifier.rstrip("/") + "/"

    def directory_entries(self, base_path=None):
        # iterate over the source dir contents to list all entries
        directory_entries = []
        if self.source and os.path.exists(self.source):
            for base, subd, filenames in os.walk(self.source):
                for filename in filenames:
                    file_source = os.path.join(base, filename)
                    rel_path = os.path.relpath(file_source, self.source)
                    if base_path:
                        dest_path = os.path.join(base_path, rel_path)
                    else:
                        dest_path = rel_path
                    file_entry = (file_source, dest_path)
                    directory_entries.append(file_entry)
        return directory_entries

    def write(self, base_path):
        out_path = self.filepath(base_path)
        pathlib.Path(out_path).mkdir(parents=True, exist_ok=True)
        for file_src, file_dest in self.directory_entries(out_path):
            file_dest_path = os.path.dirname(file_dest)
            if not os.path.exists(file_dest_path):
                os.makedirs(file_dest_path)
            shutil.copyfile(file_src, file_dest)

    def write_zip(self, zip_out):
        out_path = self.filepath()
        # create the dir in the zip
        # zip_out.writestr(out_path, '')
        # out_path = os.path.join(base_path, self.dest)
        # iterate over the entries
        for file_src, rel_path in self.directory_entries():
            dest_path = os.path.join(out_path, rel_path)
            zip_out.write(file_src, dest_path)
