package(default_visibility = ["//visibility:public"])
licenses(["notice"])

cc_library(
  name = "fasttext-library",
  srcs = [
		"args.cc",
		"dictionary.cc",
		"utils.cc",
		"vector.cc",
		"qmatrix.cc",
		"matrix.cc",
		"productquantizer.cc",
		"fasttext.cc",
		"model.cc",
	],
  hdrs = [
		"args.h",
		"dictionary.h",
		"utils.h",
		"vector.h",
		"qmatrix.h",
		"real.h",
		"matrix.h",
		"productquantizer.h",
		"model.h",
		"fasttext.h",
	]
)

cc_binary(
  name = "fasttext",
	srcs = [
		"main.cc",
	],
	deps = [":fasttext-library"],
	linkstatic = 1
)
