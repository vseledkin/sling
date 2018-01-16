#include <string>
#include <unordered_map>
#include <vector>

#include "sling/base/types.h"
#include "third_party/fasttext/fasttext.h"
#include "tensorflow/core/framework/op_kernel.h"
#include "tensorflow/core/framework/tensor.h"
#include "tensorflow/core/framework/tensor_shape.h"

using tensorflow::OpKernel;
using tensorflow::OpKernelConstruction;
using tensorflow::OpKernelContext;
using tensorflow::Tensor;
using tensorflow::TensorShape;
using tensorflow::errors::InvalidArgument;
using tensorflow::error::OUT_OF_RANGE;
using tensorflow::DEVICE_CPU;

namespace syntaxnet {
namespace dragnn {

	class FastTextEmbeddingInitializer : public OpKernel {
	 public:
	  explicit FastTextEmbeddingInitializer(OpKernelConstruction *context)
	      : OpKernel(context) {
	    OP_REQUIRES_OK(context, context->GetAttr("vectors", &vectors_path_));
	    // Sets up number and type of inputs and outputs.
	    OP_REQUIRES_OK(context, context->MatchSignature({}, {}));
	  }

	  void Compute(OpKernelContext *context) override {
	    OP_REQUIRES_OK(context, Load());

	    LOG(INFO) << "Initialized ft " << ft.getDimension() << " pre-trained embeddings ";
	  }

	 private:
	  // Loads the |vocabulary| from the |vocabulary_path_| file.
	  // The file is assumed to list one word per line, including <UNKNOWN>.
	  // The zero-based line number is taken as the id of the corresponding word.
	  tensorflow::Status Load() {
			std::cout  << "Loading FT model: " << vectors_path_ << std::endl;
			ft.loadModel(vectors_path_);
			std::cout  << "Loaded FT model:  " << vectors_path_ << std::endl;
	    return tensorflow::Status::OK();
	  }
	  // Path to fasttext model.
	  string vectors_path_;
		fasttext::FastText ft;
	};


REGISTER_KERNEL_BUILDER(Name("FastTextEmbeddingInitializer").Device(DEVICE_CPU),
                        FastTextEmbeddingInitializer);

}  // namespace dragnn
}  // namespace syntaxnet
