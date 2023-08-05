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

__all__ = [
    'load_component',
    'load_component_from_text',
    'load_component_from_url',
    'load_component_from_file',
]

import collections
import inspect
from typing import Any, Callable, List, Mapping, NamedTuple, Sequence, Union

from kfp.components import _data_passing
from kfp.components import _dynamic
from kfp.components import _naming
from kfp.components import _yaml_utils
from kfp.v2.components import structures

_default_component_name = 'Component'


def load_component(filename=None, url=None, text=None):
  """Loads component from text, file or URL and creates a task factory function.

  Only one argument should be specified.

  Args:
    filename: Path of local file containing the component definition.
    url: The URL of the component file data.
    text: A string containing the component file data.

  Returns:
    A factory function with a strongly-typed signature.
    Once called with the required arguments, the factory constructs a
    pipeline task instance (ContainerOp).
  """
  # TODO: Change this function to return component spec object but it should be
  # callable to construct tasks.
  non_null_args_count = len(
      [name for name, value in locals().items() if value != None])
  if non_null_args_count != 1:
    raise ValueError('Need to specify exactly one source')
  if filename:
    return load_component_from_file(filename)
  elif url:
    return load_component_from_url(url)
  elif text:
    return load_component_from_text(text)
  else:
    raise ValueError('Need to specify a source')


def load_component_from_url(url: str, auth=None):
  """Loads component from URL and creates a task factory function

  Args:
    url: The URL of the component file data
    auth: Auth object for the requests library. See
      https://requests.readthedocs.io/en/master/user/authentication/

  Returns:
    A factory function with a strongly-typed signature.
    Once called with the required arguments, the factory constructs a
    pipeline task instance (ContainerOp).
  """
  component_spec = _load_component_spec_from_url(url, auth)
  url = _fix_component_uri(url)
  return _create_task_factory_from_component_spec(
      component_spec=component_spec,
      component_filename=url,
  )


def load_component_from_file(filename):
  """Loads component from file and creates a task factory function

  Args:
    filename: Path of local file containing the component definition.

  Returns:
    A factory function with a strongly-typed signature.
    Once called with the required arguments, the factory constructs a
    pipeline task instance (ContainerOp).
  """
  component_spec = _load_component_spec_from_file(path=filename)
  return _create_task_factory_from_component_spec(
      component_spec=component_spec,
      component_filename=filename,
  )


def load_component_from_text(text):
  """Loads component from text and creates a task factory function

  Args:
    text: A string containing the component file data.

  Returns:
    A factory function with a strongly-typed signature.
    Once called with the required arguments, the factory constructs a
    pipeline task instance (ContainerOp).
  """
  if text is None:
    raise TypeError
  component_spec = _load_component_spec_from_component_text(text)
  return _create_task_factory_from_component_spec(component_spec=component_spec)


def _fix_component_uri(uri: str) -> str:
  #Handling Google Cloud Storage URIs
  if uri.startswith('gs://'):
    #Replacing the gs:// URI with https:// URI (works for public objects)
    uri = 'https://storage.googleapis.com/' + uri[len('gs://'):]
  return uri


def _load_component_spec_from_file(path) -> structures.ComponentSpec:
  with open(path, 'rb') as component_stream:
    return _load_component_spec_from_yaml_or_zip_bytes(component_stream.read())


def _load_component_spec_from_url(url: str, auth=None):
  if url is None:
    raise TypeError

  url = _fix_component_uri(url)

  import requests
  resp = requests.get(url, auth=auth)
  resp.raise_for_status()
  return _load_component_spec_from_yaml_or_zip_bytes(resp.content)


_COMPONENT_FILE_NAME_IN_ARCHIVE = 'component.yaml'


def _load_component_spec_from_yaml_or_zip_bytes(data: bytes):
  """Loads component spec from binary data.

  The data can be a YAML file or a zip file with a component.yaml file inside.
  """
  import zipfile
  import io
  stream = io.BytesIO(data)
  if zipfile.is_zipfile(stream):
    stream.seek(0)
    with zipfile.ZipFile(stream) as zip_obj:
      data = zip_obj.read(_COMPONENT_FILE_NAME_IN_ARCHIVE)
  return _load_component_spec_from_component_text(data)


def _load_component_spec_from_component_text(text) -> structures.ComponentSpec:
  component_dict = _yaml_utils.load_yaml(text)
  component_spec = structures.ComponentSpec.from_dict(component_dict)

  # Calculating hash digest for the component
  import hashlib
  data = text if isinstance(text, bytes) else text.encode('utf-8')
  data = data.replace(b'\r\n', b'\n')  # Normalizing line endings
  digest = hashlib.sha256(data).hexdigest()
  component_spec._digest = digest

  return component_spec


_inputs_dir = '/tmp/inputs'
_outputs_dir = '/tmp/outputs'
_single_io_file_name = 'data'


def _generate_input_file_name(port_name):
  return _inputs_dir + '/' + _naming._sanitize_file_name(
      port_name) + '/' + _nameing._single_io_file_name


def _generate_output_file_name(port_name):
  return _outputs_dir + '/' + _sanitize_file_name(
      port_name) + '/' + _single_io_file_name


def _react_to_incompatible_reference_type(
    input_type,
    argument_type,
    input_name: str,
):
  """Raises error for the case when the argument type is incompatible with the input type."""
  message = ('Argument with type "{}" was passed to the input "{}" that has '
             'type "{}".').format(argument_type, input_name, input_type)
  raise TypeError(message)


# v2 compiler doesn't use any default container task constructor
_container_task_constructor = None


def _create_task_object_from_component_and_arguments(
    component_spec: structures.ComponentSpec, arguments: Mapping[str, Any],
    **kwargs):
  """Creates a task object from component and argument.

    Unlike _container_task_constructor, handles the graph components as well.
    """
  if not isinstance(component_spec.implementation,
                    structures.ContainerImplementation):
    raise NotImplementedError(
        'GraphImplementation is not supported yet in v2 compiler.')

  task = _container_task_constructor(
      component_spec=component_spec,
      arguments=arguments,
      **kwargs,
  )

  return task


class _DefaultValue:

  def __init__(self, value):
    self.value = value

  def __repr__(self):
    return repr(self.value)


#TODO: Refactor the function to make it shorter
def _create_task_factory_from_component_spec(
    component_spec: structures.ComponentSpec,
    component_filename=None,
):
  name = component_spec.name or _default_component_name

  func_docstring_lines = []
  if component_spec.name:
    func_docstring_lines.append(component_spec.name)
  if component_spec.description:
    func_docstring_lines.append(component_spec.description)

  inputs_list = component_spec.inputs or []  #List[InputSpec]
  input_names = [input.name for input in inputs_list]

  #Creating the name translation tables : Original <-> Pythonic
  input_name_to_pythonic = _naming.generate_unique_name_conversion_table(
      input_names, _naming._sanitize_python_function_name)
  pythonic_name_to_input_name = {
      v: k for k, v in input_name_to_pythonic.items()
  }

  digest = getattr(component_spec, '_digest', None)

  def create_task_object_from_component_and_pythonic_arguments(
      pythonic_arguments):
    arguments = {
        pythonic_name_to_input_name[argument_name]: argument_value
        for argument_name, argument_value in pythonic_arguments.items()
        if not isinstance(
            argument_value, _DefaultValue
        )  # Skipping passing arguments for optional values that have not been overridden.
    }
    return _create_task_object_from_component_and_arguments(
        component_spec=component_spec,
        arguments=arguments,
    )

  #Reordering the inputs since in Python optional parameters must come after required parameters
  reordered_input_list = [
      input for input in inputs_list
      if input.default is None and not input.optional
  ] + [
      input for input in inputs_list
      if not (input.default is None and not input.optional)
  ]

  def component_default_to_func_default(component_default: str,
                                        is_optional: bool):
    if is_optional:
      return _DefaultValue(component_default)
    if component_default is not None:
      return component_default
    return inspect.Parameter.empty

  input_parameters = [
      _dynamic.KwParameter(
          input_name_to_pythonic[port.name],
          annotation=(_data_passing.get_canonical_type_for_type_struct(
              str(port.type)) or str(port.type)
                      if port.type else inspect.Parameter.empty),
          default=component_default_to_func_default(port.default,
                                                    port.optional),
      ) for port in reordered_input_list
  ]
  factory_function_parameters = input_parameters  #Outputs are no longer part of the task factory function signature. The paths are always generated by the system.

  task_factory = _dynamic.create_function_from_parameters(
      create_task_object_from_component_and_pythonic_arguments,
      factory_function_parameters,
      documentation='\n'.join(func_docstring_lines),
      func_name=name,
      func_filename=component_filename if
      (component_filename and (component_filename.endswith('.yaml') or
                               component_filename.endswith('.yml'))) else None,
  )
  task_factory.component_spec = component_spec
  return task_factory


_ResolvedCommandLineAndPaths = NamedTuple(
    '_ResolvedCommandLineAndPaths',
    [
        ('command', Sequence[str]),
        ('args', Sequence[str]),
        ('input_uris', Mapping[str, str]),
        ('output_uris', Mapping[str, str]),
        ('input_paths', Mapping[str, str]),
        ('output_paths', Mapping[str, str]),
        ('inputs_consumed_by_value', Mapping[str, str]),
    ],
)


def _resolve_command_line_and_paths(
    component_spec: structures.ComponentSpec,
    arguments: Mapping[str, str],
    input_value_generator: Callable[[str], str],
    input_uri_generator: Callable[[str], str],
    output_uri_generator: Callable[[str], str],
    input_path_generator: Callable[[str], str],
    output_path_generator: Callable[[str], str],
) -> _ResolvedCommandLineAndPaths:
  """Resolves the command line argument placeholders.

  Also produces the maps of the generated inpuit/output paths.
  """
  argument_values = arguments

  if not isinstance(component_spec.implementation,
                    structures.ContainerImplementation):
    raise TypeError('Only container components have command line to resolve')

  inputs_dict = {
      input_spec.name: input_spec for input_spec in component_spec.inputs or []
  }
  container_spec = component_spec.implementation.container

  # Preserving the order to make the kubernetes output names deterministic
  output_uris = collections.OrderedDict()
  output_paths = collections.OrderedDict()

  unconfigurable_output_paths = container_spec.file_outputs or {}
  for output in component_spec.outputs or []:
    if output.name in unconfigurable_output_paths:
      output_paths[output.name] = unconfigurable_output_paths[output.name]

  input_uris = collections.OrderedDict()
  input_paths = collections.OrderedDict()
  inputs_consumed_by_value = {}

  def expand_command_part(arg) -> Union[str, List[str], None]:
    if arg is None:
      return None
    if isinstance(arg, (str, int, float, bool)):
      return str(arg)

    if isinstance(arg, structures.InputValuePlaceholder):
      input_name = arg.input_name
      input_spec = inputs_dict[input_name]
      input_value = argument_values.get(input_name, None)
      if input_value is not None:
        input_value = input_value_generator(input_name)
        inputs_consumed_by_value[input_name] = input_value
        return input_value
      else:
        if input_spec.optional:
          return None
        else:
          raise ValueError('No value provided for input {}'.format(input_name))

    elif isinstance(arg, structures.InputUriPlaceholder):
      input_name = arg.input_name
      input_value = argument_values.get(input_name, None)
      if input_value is not None:
        input_uri = input_uri_generator(input_name)
        input_uris[input_name] = input_uri
        return input_uri
      else:
        input_spec = inputs_dict[input_name]
        if input_spec.optional:
          # Even when we support default values there is no need to check for a
          # default here. In current execution flow (called by python task
          # factory), the missing argument would be replaced with the default
          # value by python itself.
          return None
        else:
          raise ValueError('No value provided for input {}'.format(input_name))

    elif isinstance(arg, structures.InputPathPlaceholder):
      input_name = arg.input_name
      input_value = argument_values.get(input_name, None)
      if input_value is not None:
        input_path = input_path_generator(input_name)
        input_paths[input_name] = input_path
        return input_path
      else:
        input_spec = inputs_dict[input_name]
        if input_spec.optional:
          # Even when we support default values there is no need to check for a
          # default here. In current execution flow (called by python task
          # factory), the missing argument would be replaced with the default
          # value by python itself.
          return None
        else:
          raise ValueError('No value provided for input {}'.format(input_name))

    elif isinstance(arg, structures.OutputUriPlaceholder):
      output_name = arg.output_name
      output_uri = output_uri_generator(output_name)
      if arg.output_name in output_uris:
        if output_uris[output_name] != output_uri:
          raise ValueError(
              'Conflicting output URIs specified for port {}: {} and {}'.format(
                  output_name, output_uris[output_name], output_uri))
      else:
        output_uris[output_name] = output_uri

      return output_uri

    elif isinstance(arg, structures.OutputPathPlaceholder):
      output_name = arg.output_name
      output_filename = output_path_generator(output_name)
      if arg.output_name in output_paths:
        if output_paths[output_name] != output_filename:
          raise ValueError(
              'Conflicting output files specified for port {}: {} and {}'
              .format(output_name, output_paths[output_name], output_filename))
      else:
        output_paths[output_name] = output_filename

      return output_filename

    elif isinstance(arg, structures.ConcatPlaceholder):
      expanded_argument_strings = expand_argument_list(arg.items)
      return ''.join(expanded_argument_strings)

    elif isinstance(arg, structures.IfPlaceholder):
      arg = arg.if_structure
      condition_result = expand_command_part(arg.condition)
      from distutils.util import strtobool
      condition_result_bool = condition_result and strtobool(
          condition_result
      )  # Python gotcha: bool('False') == True; Need to use strtobool;
      # Also need to handle None and []
      result_node = arg.then_value if condition_result_bool else arg.else_value
      if result_node is None:
        return []
      if isinstance(result_node, list):
        expanded_result = expand_argument_list(result_node)
      else:
        expanded_result = expand_command_part(result_node)
      return expanded_result

    elif isinstance(arg, structures.IsPresentPlaceholder):
      argument_is_present = argument_values.get(arg.input_name,
                                                None) is not None
      return str(argument_is_present)
    else:
      raise TypeError('Unrecognized argument type: {}'.format(arg))

  def expand_argument_list(argument_list):
    expanded_list = []
    if argument_list is not None:
      for part in argument_list:
        expanded_part = expand_command_part(part)
        if expanded_part is not None:
          if isinstance(expanded_part, list):
            expanded_list.extend(expanded_part)
          else:
            expanded_list.append(str(expanded_part))
    return expanded_list

  expanded_command = expand_argument_list(container_spec.command)
  expanded_args = expand_argument_list(container_spec.args)

  return _ResolvedCommandLineAndPaths(
      command=expanded_command,
      args=expanded_args,
      input_uris=input_uris,
      output_uris=output_uris,
      input_paths=input_paths,
      output_paths=output_paths,
      inputs_consumed_by_value=inputs_consumed_by_value,
  )
