// GENERATED FILE - DO NOT MODIFY
#ifndef tensorflow_core_framework_variable_proto_IMPL_H_
#define tensorflow_core_framework_variable_proto_IMPL_H_

#include "tensorflow/core/framework/variable.pb.h"
#include "tensorflow/core/framework/variable.pb_text.h"
#include "tensorflow/core/lib/strings/proto_text_util.h"
#include "tensorflow/core/lib/strings/scanner.h"

namespace tensorflow {

namespace internal {

void AppendProtoDebugString(
    ::tensorflow::strings::ProtoTextOutput* o,
    const ::tensorflow::VariableDef& msg);
bool ProtoParseFromScanner(
    ::tensorflow::strings::Scanner* scanner, bool nested, bool close_curly,
    ::tensorflow::VariableDef* msg);

void AppendProtoDebugString(
    ::tensorflow::strings::ProtoTextOutput* o,
    const ::tensorflow::SaveSliceInfoDef& msg);
bool ProtoParseFromScanner(
    ::tensorflow::strings::Scanner* scanner, bool nested, bool close_curly,
    ::tensorflow::SaveSliceInfoDef* msg);

}  // namespace internal

}  // namespace tensorflow

#endif  // tensorflow_core_framework_variable_proto_IMPL_H_
