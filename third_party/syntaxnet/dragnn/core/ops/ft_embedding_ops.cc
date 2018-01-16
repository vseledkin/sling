
#include "tensorflow/core/framework/op.h"

namespace syntaxnet {
namespace dragnn {

REGISTER_OP("FastTextEmbeddingInitializer")
    .Attr("vectors: string")
    .Doc(R"doc(
Reads FastText model from file.

vectors: path to FastText model file.
)doc");

}  // namespace dragnn
}  // namespace syntaxnet
