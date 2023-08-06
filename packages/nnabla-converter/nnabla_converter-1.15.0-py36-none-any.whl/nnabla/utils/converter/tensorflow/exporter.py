# Copyright (c) 2019 Sony Corporation. All Rights Reserved.
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

from ..onnx import OnnxExporter
from onnx_tf.backend import prepare
import tensorflow as tf
import nnabla.logger as logger
from .common import find_out_terminal_node, check_optimization_criteria


class TensorflowExporter:
    def __init__(self, nnp, batch_size, enable_optimize=False):
        self._nnp = nnp
        self._batch_size = batch_size
        self.check_nnp_variable_name()
        self._enable_optimize = enable_optimize

    def check_nnp_variable_name(self):
        def fix_variable_name(variable_name):
            if "[" in variable_name and "]" in variable_name:
                variable_name = variable_name.replace("[", "_")
                variable_name = variable_name.replace("]", "")
            if "\'" in variable_name:
                variable_name = variable_name.replace("\'", "")
            return variable_name

        network = self._nnp.protobuf.network
        executor = self._nnp.protobuf.executor
        network_name = executor[0].network_name
        parameter_variable = []
        for net in network:
            if net.name == network_name:
                for var in net.variable:
                    if var.type == 'Parameter':
                        parameter_variable.append(var.name)
                        continue
                    var.name = fix_variable_name(var.name)
                for func in net.function:
                    if func.name not in parameter_variable:
                        func.name = fix_variable_name(func.name)
                    for i, name in enumerate(func.input):
                        if name not in parameter_variable:
                            del func.input[i]
                            func.input.insert(i, fix_variable_name(name))
                    for i, name in enumerate(func.output):
                        if name not in parameter_variable:
                            del func.output[i]
                            func.output.insert(i, fix_variable_name(name))
        for var in executor[0].data_variable:
            var.variable_name = fix_variable_name(var.variable_name)
        for var in executor[0].output_variable:
            var.variable_name = fix_variable_name(var.variable_name)

    def execute(self, output):
        onnx_model = OnnxExporter(
            self._nnp, self._batch_size, opset="9").export_model_proto()
        tf_rep = prepare(onnx_model)
        if self._enable_optimize:
            optimizable_state = check_optimization_criteria(
                self._nnp, self._batch_size)
            if optimizable_state['NCHW_TO_NHWC']['status']:
                from .common import OptimizePb
                optimize = OptimizePb(tf_rep.graph.as_graph_def()).execute()
                optimize.export_to_file(output)
                import json
                doc_file = output.replace('.', '_') + '.json'
                with open(doc_file, 'w') as f:
                    json.dump(optimize.get_optimization_rate(), f)
            else:
                logger.warning(
                    "Currently this model does not support optimization")
        else:
            tf_rep.export_graph(output)


class TensorflowLiteExporter:
    def __init__(self, nnp, batch_size, enable_optimize=False):
        self._nnp = nnp
        self._batch_size = batch_size
        self._enable_optimize = enable_optimize

    def check_tf_graph(self, graph):
        for op in graph.get_operations():
            if op.type == "Placeholder":
                shape = graph.get_tensor_by_name(op.name+':0').shape
                if len(shape) > 4:
                    raise ValueError("Dims is larger than 4 is not supported.")

    def execute(self, output):
        onnx_model = OnnxExporter(
            self._nnp, self._batch_size, opset="9").export_model_proto()
        tf_rep = prepare(onnx_model)
        self.check_tf_graph(tf_rep.graph)
        graph_def = tf_rep.graph.as_graph_def()
        if self._enable_optimize:
            optimizable_state = check_optimization_criteria(
                self._nnp, self._batch_size)
            if optimizable_state['NCHW_TO_NHWC']['status']:
                from .common import OptimizePb
                optimize = OptimizePb(graph_def).execute()
                graph_def = optimize.export_graph_def()
                import json
                doc_file = output.replace('.', '_') + '.json'
                with open(doc_file, 'w') as f:
                    json.dump(optimize.get_optimization_rate(), f)
            else:
                logger.warning(
                    "Currently this model does not support optimization")
        tf.reset_default_graph()
        with tf.compat.v1.Session() as session:
            _ = tf.import_graph_def(graph_def, name='')
            inputs, outputs = find_out_terminal_node(
                session.graph_def, postfix=True)

            inputs_tensor = [
                session.graph.get_tensor_by_name(inp) for inp in inputs]
            outputs_tensor = [
                session.graph.get_tensor_by_name(oup) for oup in outputs]

            converter = tf.lite.TFLiteConverter.from_session(
                session, inputs_tensor, outputs_tensor)
            converter.optimizations = [tf.lite.Optimize.DEFAULT]
            converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS,
                                                   tf.lite.OpsSet.SELECT_TF_OPS]
            tflite_model = converter.convert()
            with open(output, 'wb') as f:
                f.write(tflite_model)
