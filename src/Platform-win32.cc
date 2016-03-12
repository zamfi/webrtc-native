
/*
* The MIT License (MIT)
*
* Copyright (c) 2015 vmolsa <ville.molsa@gmail.com> (http://github.com/vmolsa)
*
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documentation files (the "Software"), to deal
* in the Software without restriction, including without limitation the rights
* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
* copies of the Software, and to permit persons to whom the Software is
* furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included in
* all copies or substantial portions of the Software.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
* OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
* THE SOFTWARE.
*
*/

#include "Platform.h"
#include <webrtc/base/ssladapter.h>
#include <webrtc/base/win32socketinit.h>
#include <webrtc/base/win32socketserver.h>

using namespace WebRTC;

class PlatformWorker : public rtc::Thread {
  public:    
    virtual void Run();
};

void PlatformWorker::Run() {
  LOG(LS_INFO) << __PRETTY_FUNCTION__;
  bool running = false;
  
  rtc::Thread::SetAllowBlockingCalls(true);
  
  do {
    running = rtc::Thread::ProcessMessages(1);
  } while(running);
}

PlatformWorker *worker;

void Platform::Init() {
  LOG(LS_INFO) << __PRETTY_FUNCTION__;
  
  worker = new PlatformWorker();
  worker->Start();
  
  rtc::EnsureWinsockInit();
  rtc::InitializeSSL();
  rtc::ThreadManager::Instance()->SetCurrentThread(worker);
  
  if (rtc::ThreadManager::Instance()->CurrentThread() != worker) {
    LOG(LS_ERROR) << "Internal Thread Error!";
    abort();
  }
}

void Platform::Dispose() {
  LOG(LS_INFO) << __PRETTY_FUNCTION__;
  
  worker->Stop();  
  rtc::CleanupSSL();
  
  delete worker;
}