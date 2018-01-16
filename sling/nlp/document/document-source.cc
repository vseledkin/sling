// Copyright 2017 Google Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "sling/nlp/document/document-source.h"

#include <vector>

#include "sling/base/logging.h"
#include "sling/base/macros.h"
#include "sling/file/file.h"
#include "sling/frame/object.h"
#include "sling/frame/serialization.h"
#include "sling/stream/input.h"
#include "sling/stream/stream.h"
#include "sling/stream/zipfile.h"

namespace sling {
namespace nlp {

// Iterator implementation which assumes one encoded document per input file.
class EncodedDocumentSource : public DocumentSource {
 public:
  EncodedDocumentSource(const std::vector<string> &files) {
    files_ = files;
    index_ = 0;
  }

  bool NextSerialized(string *name, string *contents) override {
    if (index_ >= files_.size()) return false;
    *name = files_[index_];
    CHECK(File::ReadContents(files_[index_], contents));
    index_++;

    return true;
  }

  void Rewind() override {
    index_ = 0;
  }

 private:
  std::vector<string> files_;
  int index_;
};

// Iterator implementation for zip archives..
// Assumes that each encoded document is a separate file in the zip archive.
class ZipDocumentSource : public DocumentSource {
 public:
  ZipDocumentSource(const string &file) {
    file_ = file;
    reader_ = new ZipFileReader(file);
    current_ = 0;
  }

  ~ZipDocumentSource() override {
    delete reader_;
  }

  bool NextSerialized(string *name, string *contents) override {
    if (current_ == reader_->files().size()) return false;

    const auto &entry = reader_->files()[current_];
    *name = entry.filename;

    InputStream *stream = reader_->Read(entry);
    Input input(stream);
    char ch;
    while (input.Next(&ch)) {
      contents->push_back(ch);
    }
    delete stream;
    ++current_;

    return true;
  }

  void Rewind() override {
    current_ = 0;
  }

 private:
  ZipFileReader *reader_ = nullptr;
  string file_;
  int current_;
};

Document *DocumentSource::Next(Store *store) {
  string name, contents;
  if (!NextSerialized(&name, &contents)) return nullptr;
  //LOG(INFO) << " decode " << contents;
  //StringDecoder decoder(store, contents);
  // change default format of corpus to text by vseledkin
	//LOG(INFO) << " !decoding from text! " << name;
  StringReader decoder(store, contents);
  //LOG(INFO) << " decoded " << decoder.Decode().AsText();
  //return new Document(decoder.Decode().AsFrame());
  return new Document(decoder.Read().AsFrame());
}

Document *DocumentSource::Next(Store *store, string *name) {
  string contents;
  if (!NextSerialized(name, &contents)) return nullptr;
  //LOG(INFO) << " !decoding from binary!";
	StringReader decoder(store, contents);
  //StringDecoder decoder(store, contents);
  return new Document(decoder.Read().AsFrame());
}

namespace {

bool HasSuffix(const string &s, const string &suffix) {
  int len = suffix.size();
  return (s.size() >= len) && (s.substr(s.size() - len) == suffix);
}

}  // namespace

DocumentSource *DocumentSource::Create(const string &file_pattern) {
  // TODO: Add more formats as needed.
  if (HasSuffix(file_pattern, ".zip")) {
    return new ZipDocumentSource(file_pattern);
  } else {
    std::vector<string> files;
    CHECK(File::Match(file_pattern, &files));
    return new EncodedDocumentSource(files);
  }

  return nullptr;
}

}  // namespace nlp
}  // namespace sling
