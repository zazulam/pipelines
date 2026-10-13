// Copyright 2021 The Kubeflow Authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import { PipelineSpec } from 'src/generated/pipeline_spec';
import { testBestPractices } from 'src/TestUtils';
import { convertFlowElements } from './StaticFlow';
import v2YamlTemplateString from 'src/data/test/lightweight_python_functions_v2_pipeline_rev.yaml?raw';
import { load } from 'js-yaml';

testBestPractices();
describe('StaticFlow', () => {
  it('converts simple pipeline with element ids to graph', () => {
    const yamlObject = load(v2YamlTemplateString);

    const pipelineSpec = PipelineSpec.fromJSON(yamlObject);

    const graph = convertFlowElements(pipelineSpec);
    for (let element of graph) {
      const index = [
        'task.preprocess',
        'task.train',
        'artifact.preprocess.output_dataset_one',
        'artifact.preprocess.output_dataset_two_path',
        'artifact.train.model',
        'outedge.preprocess.output_dataset_one',
        'inedge.preprocess.output_dataset_two_path.train.dataset_two',
        'outedge.preprocess.output_dataset_two_path',
        'inedge.preprocess.output_dataset_one.train.dataset_one_path',
        'outedge.train.model',
        'paramedge.preprocess.train',
      ].findIndex((x) => x === element.id);
      expect(index > -1).toBeTruthy();
    }
  });

  it('converts static lists to unique dependency edges', () => {
    const pipelineSpec = PipelineSpec.fromJSON({
      root: {
        dag: {
          tasks: {
            trainerA: {
              taskInfo: { name: 'trainer-a' },
              componentRef: { name: 'comp-trainer-a' },
            },
            trainerB: {
              taskInfo: { name: 'trainer-b' },
              componentRef: { name: 'comp-trainer-b' },
            },
            evaluator: {
              taskInfo: { name: 'evaluator' },
              componentRef: { name: 'comp-evaluator' },
              inputs: {
                artifacts: {
                  models: {
                    artifactList: {
                      items: [
                        {
                          taskOutputArtifact: {
                            producerTask: 'trainerA',
                            outputArtifactKey: 'model',
                          },
                        },
                        {
                          taskOutputArtifact: {
                            producerTask: 'trainerB',
                            outputArtifactKey: 'model',
                          },
                        },
                        {
                          taskOutputArtifact: {
                            producerTask: 'trainerA',
                            outputArtifactKey: 'model',
                          },
                        },
                      ],
                    },
                  },
                },
              },
            },
          },
        },
      },
      components: {
        'comp-trainer-a': {
          executorLabel: 'trainer-a',
          outputDefinitions: { artifacts: { model: {} } },
        },
        'comp-trainer-b': {
          executorLabel: 'trainer-b',
          outputDefinitions: { artifacts: { model: {} } },
        },
        'comp-evaluator': {
          executorLabel: 'evaluator',
          inputDefinitions: { artifacts: { models: { isArtifactList: true } } },
        },
      },
    });

    const graph = convertFlowElements(pipelineSpec);
    const collectionEdges = graph.filter((element) => element.id.startsWith('inedge.'));

    expect(collectionEdges).toHaveLength(2);
    expect(collectionEdges.map((edge) => edge.id)).toEqual(
      expect.arrayContaining([
        'inedge.trainerA.model.evaluator.models',
        'inedge.trainerB.model.evaluator.models',
      ]),
    );
    expect(
      collectionEdges.find((edge) => edge.id === 'inedge.trainerA.model.evaluator.models')?.data,
    ).toEqual({ collectionPositions: [0, 2] });
  });
});
