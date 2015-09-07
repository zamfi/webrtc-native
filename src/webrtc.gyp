{
  'includes': [
    '../third_party/webrtc/src/webrtc/supplement.gypi',
    '../third_party/webrtc/src/webrtc/build/common.gypi',
    '../third_party/webrtc/src/talk/build/common.gypi',
    '../build/config.gypi',
    '../nodejs.gypi',
    'addon.gypi',
  ],
  'targets': [
    {
      'target_name': 'webrtc',
      'sources': [
        'Global.cc',
        'Core.cc',
        'Thread.cc',
        'BackTrace.cc',
        'EventEmitter.cc',
        'Observers.cc',
        'Module.cc',
        'PeerConnection.cc',
        'DataChannel.cc',
        'GetSources.cc',
        'GetUserMedia.cc',
        'MediaStream.cc',
        'MediaStreamTrack.cc',
        'MediaConstraints.cc',
        'Stats.cc',
        'MediaSource.cc',
        'WebcamCapturer.cc',
        'MediaStreamCapturer.cc',
      ],
      'dependencies': [
        '<(DEPTH)/talk/libjingle.gyp:libjingle_peerconnection',
      ],
      'include_dirs': [
        '<(DEPTH)/third_party/jsoncpp/source/include',
        '<(DEPTH)/third_party/libsrtp/srtp',
        '<(DEPTH)/third_party/libyuv/include',
        "<!(node -e \"require('nan')\")",
      ],
      'conditions': [
        ['include_tests==1', {
          'dependencies': [
            '<(DEPTH)/talk/libjingle_tests.gyp:libjingle_unittest_main',
            '<(DEPTH)/talk/libjingle_tests.gyp:libjingle_media_unittest',
            '<(DEPTH)/webrtc/modules/modules.gyp:video_capture_tests',
            '<(DEPTH)/webrtc/modules/modules.gyp:video_render_tests',
          ],
        }],
        ['OS=="linux"', {
          'cflags': [
            '-Wno-deprecated-declarations',
            '-Wno-unused-variable',
            '-Wno-unknown-pragmas',
            '-Wno-unused-result',
          ],
          'cflags_cc': [
            '-std=gnu++11',
            '-Wno-overloaded-virtual',
          ],
          'ldflags': [
            '-Wl,--unresolved-symbols=ignore-in-object-files',
          ],
          'defines': [
            'USE_BACKTRACE',
          ],
          'sources': [
            'WindowRendererLinux.cc',
            'LinuxWindow.cc',
          ],
        }],
        ['OS=="win"', {
          'msvs_disabled_warnings': [
            4267,
            4005,
            4201,
            4506,
          ],
          'sources': [
            'PlatformWin32.cc',
            'WindowRendererWin32.cc',
          ],
        }],
        ['OS=="mac"', {
          'xcode_settings': {
            'OTHER_CFLAGS': [
              '-Wno-deprecated-declarations',
              '-Wno-newline-eof',
              '-Wno-unknown-pragmas',
              '-Wno-unused-result',
            ],
          },
          'defines': [
            'USE_BACKTRACE',
          ],
          'sources': [
            'PlatformMac.cc',
            'WindowRendererMac.mm',
          ],
        }],
      ],
    },
    {
      'target_name': 'All',
      'type': 'none',
      'dependencies': [
        'webrtc',
      ],
    },
  ],
}
