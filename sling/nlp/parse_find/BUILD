package(default_visibility = ["//visibility:public"])

cc_binary(
  name = "parse_find",
  srcs = ["parse_find.cc"],
  deps = [
		"//sling/base",
		"//sling/base:clock",
		"//sling/file:posix",
		"//sling/frame:object",
		"//sling/frame:serialization",
		"//sling/nlp/document",
		"//sling/nlp/document:document-source",
		"//sling/nlp/document:document-tokenizer",
		"//sling/nlp/parser",
		"//sling/nlp/parser/trainer:frame-evaluation",
		"//sling/string:printf",
  ],
)
