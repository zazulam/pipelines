# Copyright 2020 The Kubeflow Authors
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

from kfp import compiler, dsl

@dsl.component()
def print_op(s: int):
    print(s)

@dsl.pipeline(name='my-pipeline')
def pipeline():
    loop_args = [{'A_a': 1, 'B_b': 2}, {'A_a': 10, 'B_b': 20}]
    with dsl.ParallelFor(items=loop_args, parallelism=10) as item:
        print_op(s=item.A_a)
        print_op(s=item.B_b)


if __name__ == '__main__':
    compiler.Compiler().compile(pipeline, __file__ + '.yaml')
