# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
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

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import numpy as np
import paddle
import signal
import random

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(__dir__, '../..')))

import copy
from paddle.io import Dataset, DataLoader, BatchSampler, DistributedBatchSampler
import paddle.distributed as dist

from ppocr.data.imaug import transform, create_operators
from ppocr.data.simple_dataset import SimpleDataSet
from ppocr.data.lmdb_dataset import LMDBDateSet

__all__ = ['build_dataloader', 'transform', 'create_operators']


def term_mp(sig_num, frame):
    """ kill all child processes
    """
    pid = os.getpid()
    pgid = os.getpgid(os.getpid())
    print("main proc {} exit, kill process group " "{}".format(pid, pgid))
    os.killpg(pgid, signal.SIGKILL)


signal.signal(signal.SIGINT, term_mp)
signal.signal(signal.SIGTERM, term_mp)


def build_dataloader(config, mode, device, logger):
    config = copy.deepcopy(config)

    support_dict = ['SimpleDataSet', 'LMDBDateSet']
    module_name = config[mode]['dataset']['name']
    assert module_name in support_dict, Exception(
        'DataSet only support {}'.format(support_dict))
    assert mode in ['Train', 'Eval', 'Test'
                    ], "Mode should be Train, Eval or Test."

    dataset = eval(module_name)(config, mode, logger)
    loader_config = config[mode]['loader']
    batch_size = loader_config['batch_size_per_card']
    drop_last = loader_config['drop_last']
    num_workers = loader_config['num_workers']

    use_shared_memory = False
    if mode == "Train":
        #Distribute data to multiple cards
        batch_sampler = DistributedBatchSampler(
            dataset=dataset,
            batch_size=batch_size,
            shuffle=False,
            drop_last=drop_last)
        use_shared_memory = True
    else:
        #Distribute data to single card
        batch_sampler = BatchSampler(
            dataset=dataset,
            batch_size=batch_size,
            shuffle=False,
            drop_last=drop_last)

    data_loader = DataLoader(
        dataset=dataset,
        batch_sampler=batch_sampler,
        places=device,
        num_workers=num_workers,
        return_list=True,
        use_shared_memory=use_shared_memory)

    return data_loader
