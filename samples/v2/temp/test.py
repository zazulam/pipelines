from kfp import local
from kfp import dsl
from kfp.client import Client
from kfp.dsl import Output, Artifact, Dataset, Model
import json
from typing import List

local.init(runner=local.SubprocessRunner())

client = Client()


@dsl.component
def add(a: int, b: int) -> int:
    return a + b

# run a single component
# task = add(a=1, b=2)
# assert task.output == 3


@dsl.component
def multiply(a: int, b: int) -> int:
    return a*b

@dsl.pipeline
def multi_pipeline(v: int, w: int) -> int:
    c1 = multiply(a=v, b=w).set_caching_options(False)
    return c1.output
# or run it in a pipeline
@dsl.pipeline
def math_pipeline(x: int, y: int, z: int) -> int:
    t1 = add(a=x, b=y).set_display_name("add-task").set_caching_options(False)
    t2 = multi_pipeline(v=t1.output, w=z).set_display_name("multiply-pipeline").set_caching_options(False)

    t3 = add(a=t1.output, b=t2.output).set_caching_options(False)
    return t3.output

# pipeline_task = math_pipeline(x=1, y=2, z=3)
# assert pipeline_task.output == 12

# run = client.create_run_from_pipeline_func(math_pipeline, arguments={"x":1, "y":2, "z":3})

@dsl.component()
def split_ids(ids: str) -> list:
    return ids.split(',')


@dsl.component()
def prepend_id(content: str) -> str:
    print(f"prepending: {content} with 'model_id'")
    return f'model_id_{content}'


@dsl.component()
def consume_ids(ids: List[str]) -> str:
    for id in ids:
        print(f'Consuming: {id}')
    return 'completed'


@dsl.component()
def consume_single_id(id: str) -> str:
    print(f'Consuming single: {id}')
    return 'completed'


@dsl.pipeline()
def collecting_parameters(model_ids: str = '',) -> list:
    ids_split_op = split_ids(ids=model_ids)
    with dsl.ParallelFor(ids_split_op.output) as model_id:
        with dsl.ParallelFor(ids_split_op.output) as idx:
            prepend_id_op = prepend_id(content=model_id)
            prepend_id_op.set_caching_options(False)
            
            consume_single_id_op = consume_single_id(id=prepend_id_op.output)
            consume_single_id_op.set_caching_options(False)
    
    consume_ids_op = consume_ids(ids=dsl.Collected(prepend_id_op.output))
    consume_ids_op.set_caching_options(False)

    return dsl.Collected(prepend_id_op.output)

# loop_task = collecting_parameters(model_ids="s1,s2,s3")




@dsl.component()
def split_ids(model_ids: str) -> list:
    return model_ids.split(',')


@dsl.component()
def create_file(file: Output[Artifact], content: str):
    print(f'Creating file with content: {content}')
    with open(file.path, 'w') as f:
        f.write(content)


@dsl.component()
def read_files(files: List[Artifact]) -> str:
    for f in files:
        print(f'Reading artifact {f.name} file: {f.path}')
        with open(f.path, 'r') as f:
            print(f.read())

    return 'files read'


@dsl.component()
def read_single_file(file: Artifact) -> str:
    print(f'Reading file: {file.path}')
    with open(file.path, 'r') as f:
        print(f.read())

    return file.uri

@dsl.component()
def split_chars(model_ids: str) -> list:
    return model_ids.split(',')


@dsl.component()
def create_dataset(data: Output[Dataset], content: str):
    print(f'Creating file with content: {content}')
    with open(data.path, 'w') as f:
        f.write(content)


@dsl.component()
def read_datasets(data: List[Dataset]) -> str:
    for d in data:
        print(f'Reading dataset {d.name} file: {d.path}')
        with open(d.path, 'r') as f:
            print(f.read())

    return 'files read'


@dsl.component()
def read_single_dataset_generate_model(data: Dataset, id: str, results:Output[Model]):
    print(f'Reading file: {data.path}')
    with open(data.path, 'r') as f:
        info = f.read()
        with open(results.path, 'w') as f2:
            f2.write(f"{info}-{id}")
            results.metadata['model'] = info
            results.metadata['model_name'] = f"model-artifact-inner-iteration-{info}-{id}"


@dsl.component()
def read_models(models: List[Model],) -> str:
    for m in models:
        print(f'Reading model {m.name} file: {m.path}')
        with open(m.path, 'r') as f:
            info = f.read()
            print(f"Model raw data: {info}")
            print(f"Model metadata: {m.metadata}")
    return 'models read'
    
@dsl.pipeline()
def single_node_dag(char:str)-> Dataset:
    create_dataset_op = create_dataset(content=char)
    # create_dataset_op.set_caching_options(False)
    return create_dataset_op.outputs["data"]

@dsl.pipeline()
def collecting_artifacts(model_ids: str = '', model_chars: str = '') -> List[Model]:
    ids_split_op = split_ids(model_ids=model_ids)
    # ids_split_op.set_caching_options(False)

    char_split_op = split_chars(model_ids=model_chars)
    # char_split_op.set_caching_options(False)
    
    with dsl.ParallelFor(ids_split_op.output) as model_id:
        create_file_op = create_file(content=model_id)
        # create_file_op.set_caching_options(False)

        read_single_file_op = read_single_file(
            file=create_file_op.outputs['file'])
        # read_single_file_op.set_caching_options(False)

        with dsl.ParallelFor(char_split_op.output) as model_char:
            single_dag_op = single_node_dag(char=model_char)
            # single_dag_op.set_caching_options(False)

            random_subdag_op = read_single_dataset_generate_model_op = read_single_dataset_generate_model(data=single_dag_op.output, id=model_id)
            # read_single_dataset_generate_model_op.set_caching_options(False)
        
        read_models_op = read_models(
            models=dsl.Collected(read_single_dataset_generate_model_op.outputs['results']))
        # read_models_op.set_caching_options(False)

        read_datasets_op = read_datasets(
            data=dsl.Collected(single_dag_op.output))
        # read_datasets_op.set_caching_options(False)
    
    return dsl.Collected(read_single_dataset_generate_model_op.outputs["results"])


@dsl.pipeline()
def collected_artifact_pipeline():
    model_ids = 's1,s2,s3'
    model_chars = 'x,y,z'
    dag = collecting_artifacts(model_ids=model_ids, model_chars=model_chars)
    read_files_op = read_models(models=dag.output)



pipeline_task = collected_artifact_pipeline()


# @dsl.component
# def add_pipeline(a: int, b: int, out_artifact: Output[Artifact]):
#     import json

#     result = json.dumps(a + b)

#     with open(out_artifact.path, 'w') as f:
#         f.write(result)

#     out_artifact.metadata['operation'] = 'addition'


# task = add_pipeline(a=1, b=2)

# # can read artifact contents
# with open(task.outputs['out_artifact'].path) as f:
#     contents = f.read()

# assert json.loads(contents) == 3
# assert task.outputs['out_artifact'].metadata['operation'] == 'addition'