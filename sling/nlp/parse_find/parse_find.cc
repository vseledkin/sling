//
// Created by viacheslav seledkin on 12/28/17.
//
#include <sstream>
#include <string>
#include <fstream>

#include <iostream>
#include "sling/base/clock.h"
#include "sling/base/init.h"
#include "sling/base/logging.h"
#include "sling/base/types.h"
#include "sling/base/flags.h"
#include "sling/frame/object.h"
#include "sling/frame/serialization.h"
#include "sling/frame/store.h"
#include "sling/nlp/document/document.h"
#include "sling/nlp/document/document-source.h"
#include "sling/nlp/document/document-tokenizer.h"
#include "sling/nlp/parser/parser.h"
#include "sling/nlp/parser/trainer/frame-evaluation.h"
#include "sling/string/printf.h"

DEFINE_string(parser, "", "Input file with flow model");
DEFINE_string(file, "", "File to parse");

DEFINE_int32(indent, 2, "Indentation for SLING output");
DEFINE_bool(gpu, false, "Run parser on GPU");
DEFINE_bool(profile, false, "Profile parser");
DEFINE_bool(fast_fallback, true, "Use fast fallback for parser predictions");

using namespace sling;
using namespace sling::nlp;

int main(int argc, char *argv[]) {
    InitProgram(&argc, &argv);

    LOG(INFO) << "Load parser from " << FLAGS_parser;

    Clock clock;
    clock.start();
    Store global;
    Parser parser;
    if (FLAGS_fast_fallback) parser.EnableFastFallback();
    if (FLAGS_profile) parser.EnableProfiling();
    if (FLAGS_gpu) {
        LOG(INFO) << " GPU mode";
        parser.EnableGPU();
    } else {
        LOG(INFO) << " CPU mode";
    }
    parser.Load(&global, FLAGS_parser);
    global.Freeze();
    clock.stop();
    LOG(INFO) << clock.ms() << " ms loading parser";

    Handle h_person = global.Lookup("/saft/person");
    Handle h_love01 = global.Lookup("/pb/love-01");
    Handle h_arg0 = global.Lookup("/pb/arg0");
    Handle h_arg1 = global.Lookup("/pb/arg1");
    Handle argue = global.Lookup("/pb/clash-01");
    Handle conflict = global.Lookup("/pb/conflict-01");
    Handle confront = global.Lookup("/pb/confront-01");
    Handle adjudicate = global.Lookup("/pb/adjudicate-01");


    std::ifstream infile(FLAGS_file);
    std::string line;
    while (std::getline(infile, line)) {
        //std::istringstream iss(line);
        //std::cout << line << "\n";

        // Parse input text.
        // Create document tokenizer.
        DocumentTokenizer tokenizer;

        // Create document
        Store local(&global);
        Document document(&local);

        // Parse sentence.
        tokenizer.Tokenize(&document, line);

        clock.start();
        parser.Parse(&document);
        document.Update();
        clock.stop();

        //std::cout << ToText(document.top(), 1) << "\n";
        //LOG(INFO) << document.num_tokens() / clock.secs() << " tokens/sec";


        //std::cout << "Text: " << document.GetText() << "\n";
        //std::cout << "Tokens: " << document.num_tokens() << "\n";
        //std::cout << "Spans: " << document.num_spans() << "\n";

        for (int i = 0; i < document.num_spans(); i++) {
            Span *s = document.GetSpanAt(i);
            if (s != NULL) {

                //if (s->Evokes(h_person)) {
                //    Frame f = s->Evoked();
                //    std::cout << "\t\tPerson: " << s->GetText() << ToText(f) << "\n";
                // }
                if (s->Evokes(argue) || s->Evokes(conflict) || s->Evokes(confront) || s->Evokes(adjudicate)) {
                    //std::cout << "Sentence: " << line << "\n";
                    //std::cout << i << "-" << s->GetText() << " Span:\n";
                    Frame f = s->Evoked();
                    //std::cout << "\t\tLove: " << s->GetText() << ToText(f) << "\n";
                    //std::cout << "\t\tLover: " << ToText(f.GetFrame(h_arg0)) << "\n";
                    //std::cout << "\t\tLoves: " << ToText(f.GetFrame(h_arg1)) << "\n";
                    std::cout << "Sentence: " << line << "\n";
                    continue;
                }
                if (false and s->Evokes(h_love01)) {
                    //std::cout << "Sentence: " << line << "\n";
                    //std::cout << i << "-" << s->GetText() << " Span:\n";
                    Frame f = s->Evoked();
                    //std::cout << "\t\tLove: " << s->GetText() << ToText(f) << "\n";
                    //std::cout << "\t\tLover: " << ToText(f.GetFrame(h_arg0)) << "\n";
                    //std::cout << "\t\tLoves: " << ToText(f.GetFrame(h_arg1)) << "\n";
                    Frame f1 = f.GetFrame(h_arg0);
                    Frame f2 = f.GetFrame(h_arg1);
                    if (f1 != Frame::nil() && f1.IsA(h_person) && f2 != Frame::nil() && f2.IsA(h_person)) {
                        std::cout << "Sentence: " << line << "\n";
                    }
                    continue;
                }
            }
        }
    }

    // Output profile report.
    if (FLAGS_profile) {
        myelin::Profile lr(&parser.profile()->lr);
        std::cout << lr.ASCIIReport() << "\n";

        myelin::Profile rl(&parser.profile()->rl);
        std::cout << rl.ASCIIReport() << "\n";

        myelin::Profile ff(&parser.profile()->ff);
        std::cout << ff.ASCIIReport() << "\n";
    }
    return 0;
}
