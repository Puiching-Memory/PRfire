from PIL import Image
from ovis.serve.runner import RunnerArguments, OvisRunner
image = Image.open('IMAGE_PATH')
text = 'PROMPT'
runner_args = RunnerArguments(model_path='MODEL_PATH')
runner = OvisRunner(runner_args)
generation = runner.run([image, text])