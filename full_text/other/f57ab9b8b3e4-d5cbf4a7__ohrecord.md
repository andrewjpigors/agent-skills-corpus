---
name: ohrecord
description: "OpenHarmony snapshot_record 录屏 MP4；audio_framework 侧 audio_record_demo 录音、audio_play_demo 音乐播放；camera_framework 侧 camera_record / camera_record_demo 摄像头录像 MP4；asserts 资源、单编/推送/运行与 recv 拉取。脚本 ohrecord.py；camera_record 颜色/时长/帧率/NEON 雷区见本 SKILL 第六节；录屏详见 ohproj/SKILL.md 第十节。"
author: "Created by user"
created: "2026-03-24"
version: "1.6.0"
---

# ohrecord 技能说明

本技能描述 **`snapshot_record`** 录屏 **MP4**、`audio_record_demo` 麦克风录音、**`audio_play_demo`** 本地文件音乐播放（**OHAudio Renderer**）、**`camera_record` / `camera_record_demo`** 摄像头录像 **MP4**。录屏的详细步骤写在 **`src/skills/ohproj/SKILL.md` 第十节**；本文件提供索引与 **`ohrecord.py`** 用法。命令路径与 **`HOWTOSKILLS.md`** 一致：在 **napi_generator 仓库根** 下使用 **`src/skills/ohrecord/...`**。

---

## 一、脚本入口（固化命令）

在 **napi_generator 仓库根**（或任意目录）执行 **`python3 src/skills/ohrecord/ohrecord.py …`** 均可。OpenHarmony **源码根**（含 `build.sh`）由 **`--src`**、环境变量 **`OHOS_SRC`** 或从脚本位置向上查找 **`build.sh`** 推断。

```bash
# 查看本技能涉及的关键路径说明
python3 src/skills/ohrecord/ohrecord.py paths

# 全量编译产品（与日常镜像一致）
python3 src/skills/ohrecord/ohrecord.py build --product rk3568

# 设备：准备录制目录 + SELinux 标签（多设备用 -t 或环境变量 OHRECORD_HDC_TARGET）
python3 src/skills/ohrecord/ohrecord.py prep-device
python3 src/skills/ohrecord/ohrecord.py device-status

# 验证设备上媒体库是否包含「服务端按路径 open」逻辑
python3 src/skills/ohrecord/ohrecord.py verify-device-so

# 录制（秒数、设备侧绝对路径，须落在 /data/test/media 下）
python3 src/skills/ohrecord/ohrecord.py record --seconds 60 --file /data/test/media/demo_1min.mp4

# 拉取 MP4 到本技能目录下 recv/（或 --local 指定路径）
python3 src/skills/ohrecord/ohrecord.py pull --remote /data/test/media/demo_1min.mp4

# 本机产物中查找 libmedia_service.z.so 并校验特征串（编译后）
python3 src/skills/ohrecord/ohrecord.py verify-host-so --product rk3568

# 录屏失败后抓 ScreenCapture 相关 hilog
python3 src/skills/ohrecord/ohrecord.py hilog-capture

# —— 麦克风录音 audio_record_demo（与 snapshot_record 独立）——
python3 src/skills/ohrecord/ohrecord.py audio-paths
# 单编：与 ohbuild 技能一致，--build-target 只写目标名 audio_record_demo（不要写 path:target）
# 等价命令：./build.sh --build-target audio_record_demo --product-name rk3568
python3 src/skills/ohrecord/ohrecord.py audio-build --product rk3568
# 设备上准备 /data/local/tmp
python3 src/skills/ohrecord/ohrecord.py prep-audio
# 将本机编译产物推送到设备（默认 /data/local/tmp/audio_record_demo）
python3 src/skills/ohrecord/ohrecord.py audio-push --product rk3568
# 在设备上执行（参数原样传给二进制；默认自动录 10s）
python3 src/skills/ohrecord/ohrecord.py audio-run -- auto 10
# 运行结束后自动把 WAV/MP3 拉到本技能目录下 recv/（解析程序打印的路径）
python3 src/skills/ohrecord/ohrecord.py audio-run --pull --timeout 120 -- auto 5
python3 src/skills/ohrecord/ohrecord.py audio-run -- start
python3 src/skills/ohrecord/ohrecord.py audio-run -- stop
# 手动拉取（与 pull 相同）：默认保存到 src/skills/ohrecord/recv/文件名
python3 src/skills/ohrecord/ohrecord.py audio-pull --remote /data/local/tmp/audio_record_20260330_120000.wav
python3 src/skills/ohrecord/ohrecord.py pull --remote /data/local/tmp/audio_record_20260330_120000.wav

# —— 音乐播放 audio_play_demo（演示资源在技能 asserts/）——
python3 src/skills/ohrecord/ohrecord.py play-paths
python3 src/skills/ohrecord/ohrecord.py play-build --product rk3568
python3 src/skills/ohrecord/ohrecord.py play-assets
python3 src/skills/ohrecord/ohrecord.py play-push --product rk3568
# 播放 asserts 中的大示例 WAV（耗时可数分钟，勿把 --timeout 设太短）
python3 src/skills/ohrecord/ohrecord.py play-run --preset wav --timeout 1800
python3 src/skills/ohrecord/ohrecord.py play-run --preset mp3 --timeout 600
python3 src/skills/ohrecord/ohrecord.py play-run --media /data/local/tmp/ohrecord_assets/test.mp3

# —— 摄像头录像 camera_record（默认固化工具，最终文件落 /data/local/tmp）——
python3 src/skills/ohrecord/ohrecord.py cam-paths
python3 src/skills/ohrecord/ohrecord.py cam-build --product rk3568
python3 src/skills/ohrecord/ohrecord.py cam-push --product rk3568
python3 src/skills/ohrecord/ohrecord.py cam-prep
python3 src/skills/ohrecord/ohrecord.py cam-run --pull --timeout 240
python3 src/skills/ohrecord/ohrecord.py cam-run --pull --verify -- auto 10
python3 src/skills/ohrecord/ohrecord.py cam-run --pull -- auto 15
python3 src/skills/ohrecord/ohrecord.py cam-run --pull -- start /data/local/tmp/manual.mp4
python3 src/skills/ohrecord/ohrecord.py cam-run -- stop
# 检查拉回 MP4 的容器时长元数据（mvhd/mdhd/stts）
python3 src/skills/ohrecord/ohrecord.py cam-inspect --local src/skills/ohrecord/recv/camera_record_xxx.mp4
```

**环境变量**

| 变量 | 含义 |
|------|------|
| `OHOS_SRC` | 源码根（可选，默认从脚本位置推断） |
| `OHRECORD_HDC_TARGET` | `hdc -t` 序列号，多设备时与 `ohrecord.py -t` 等价 |

---

## 二、核心约定（必读）

| 项 | 说明 |
|----|------|
| **输出目录** | 必须使用 **`/data/test/media`**（与 `file_contexts` 中 `data_test_media_file` 一致）。 |
| **手建目录标签** | `mkdir` 出的目录常为 **`data_file`**，会导致 **`media_service` open 失败 errno=13 (EACCES)**；需 **`chcon u:object_r:data_test_media_file:s0 /data/test/media`** 或等价 **`restorecon`**（以设备支持为准）。 |
| **开发者模式** | `param get const.security.developermode.state` 须为 **true**，否则 `snapshot_record` 直接退出。 |
| **二进制位置（设备）** | 安装后通常在 **`/system/bin/snapshot_record`**；媒体进程加载 **`/system/lib/libmedia_service.z.so`**（视架构可能为 `lib64`）。 |

**camera_record 额外约定**

| 项 | 说明 |
|----|------|
| **默认工具** | `ohrecord.py` 的 `cam-*` 子命令现默认操作 **`camera_record`**，源码目录为 `foundation/multimedia/camera_framework/test/camera_record/`。 |
| **最终 MP4 输出路径** | 默认写到 **`/data/local/tmp/camera_record_%Y%m%d_%H%M%S.mp4`**；`start /data/local/tmp/x.mp4` 也会真正落到传入路径。 |
| **板级固化规避** | 本板子上 **`Recorder::SetOutputFile()` 不能直接接受 `/data/local/tmp` 目标 fd**。因此 `camera_record` 内部固化为：**先录到 `/data/test/media/camera_record_stage_*.mp4`，结束后再自动拷贝到 `/data/local/tmp/*.mp4`，最后清理 stage 文件**。 |
| **cam-prep 行为** | `ohrecord.py cam-prep` 会同时准备 **`/data/local/tmp`** 和 **`/data/test/media`**，并给 `/data/test/media` 补 `data_test_media_file` 标签。 |
| **cam-run --pull 回退逻辑** | `ohrecord.py` 已固化：若 stdout 中没解析出 `camera_record: done <path>`，会自动回退到 **`ls -t /data/local/tmp/camera_record_*.mp4 | head -n 1`** 取最新成品文件。 |
| **本地拉回目录** | `cam-run --pull` 默认把文件拉回到 **`src/skills/ohrecord/recv/`**；只有显式传 `--pull-local` 才会改到其它目录。 |
| **自动校验** | `cam-run --pull --verify` 会先在设备侧检查文件存在、大小大于 1KB，并读取前 12 字节做 `ftyp` 头校验，再执行拉回。拉回本地后，`ohrecord.py` 还会自动解析 **`mvhd/mdhd/stts`** 摘要。 |
| **时长元数据检查** | 新增 **`cam-inspect --local <mp4>`**：直接解析本机 MP4 的 **`mvhd_seconds / mdhd_seconds / stts_seconds / sample_count / stts_first_entries`**，并给出初步诊断。`cam-run --pull --verify` / `pull` 在拉回 MP4 后也会自动打印同类诊断，用于判断“播放器显示异常”究竟是容器时长字段损坏，还是实际送帧/时间轴不对。 |

**camera_record_demo 兼容说明**

| 项 | 说明 |
|----|------|
| **保留原因** | `interfaces/camera_record_demo/` 仍保留为历史参考与排障样例。 |
| **输出路径特性** | 该旧 demo 当前 `main_ndk.cpp` 仍会忽略 `argv[1]`，真实输出固定在 **`/data/test/media/camera_record_%Y%m%d_%H%M%S.mp4`**。 |
| **使用建议** | 日常录制、脚本固化、回归验证统一优先用 **`camera_record`**；只有对照老链路或追历史问题时才看 `camera_record_demo`。 |

**麦克风录音（`audio_record_demo`）**

| 项 | 说明 |
|----|------|
| **源码与构建** | 源码目录 `foundation/multimedia/audio_framework/test/demo/audio_record_demo/`；**`./build.sh --build-target audio_record_demo --product-name rk3568`**（只填 **BUILD.gn 里的目标名**，规则见 **`src/skills/ohbuild/SKILL.md`**）。**`bundle.json` → `fwk_group`** 中为完整 GN 标签 `//foundation/.../audio_record_demo:audio_record_demo`。 |
| **默认输出目录** | **`/data/local/tmp`**；停止长录：`audio_record_demo stop` 或写入 **`/data/local/tmp/.audio_record_stop`**。 |
| **默认时长** | 无参数或 `auto` 不带秒数时 **10 秒**（不是 30 秒）；要 30 秒请执行 **`auto 30`**。结束条件：**单调时钟**（`CLOCK_MONOTONIC`，失败则回退 `steady_clock`）+ **`auto` 模式按采样参数计算的 PCM 字节上限**（防设备侧短时灌入超量缓冲导致 WAV 极长）。 |
| **格式** | 默认 **WAV**（PCM S16LE）；**`--format mp3`** 先写 WAV 再调用 **`ffmpeg`**（设备需自带 ffmpeg，否则保留 WAV 并在本机转换）。 |
| **设备二进制** | 默认 **`install_enable = false`**，需 **`ohrecord.py audio-push`** 或手动 **`hdc file send`** 到可执行路径（如 **`/data/local/tmp/audio_record_demo`**）并 **`chmod +x`**。 |
| **本机产物目录** | 测试后拉取的 WAV/MP3 默认在 **`src/skills/ohrecord/recv/`**（**`audio-run --pull`**、**`audio-pull`**、**`pull`** 一致；可用 **`--pull-local` / `--local`** 指定其它路径）。 |

**音乐播放（`audio_play_demo`）**

| 项 | 说明 |
|----|------|
| **源码与构建** | `foundation/multimedia/audio_framework/test/demo/audio_play_demo/`；**`./build.sh --build-target audio_play_demo --product-name rk3568`**；已加入 **`bundle.json` → `fwk_group`**。 |
| **演示媒体** | 本技能 **`src/skills/ohrecord/asserts/`**：**`file_example_WAV_10MG.wav`**（PCM 16-bit WAV，解析 fmt/data）、**`test.mp3`**。 |
| **设备流程** | **`play-assets`** → 推到 **`/data/local/tmp/ohrecord_assets/`**；**`play-push`** → 二进制 **`/data/local/tmp/audio_play_demo`**；**`play-run --preset wav|mp3`**。 |
| **MP3** | 设备上需 **`ffmpeg`** 解码为临时 **`/data/local/tmp/.audio_play_demo_decoded.pcm`** 再播放；若无 ffmpeg，请改用 WAV 或在本机转 PCM。 |
| **WAV** | 仅支持 **format 1 PCM、16-bit**；从 **data** 块读入，参数与 **fmt** 一致。 |
| **无声排查** | 渲染流已设 **`AUDIOSTREAM_USAGE_MUSIC`**（避免 UNKNOWN 走错误音量/路由）；请确认设备 **媒体音量** 未静音、耳机/HDMI/喇叭接线正确。 |

**摄像头录像（`camera_record`）**

| 项 | 说明 |
|----|------|
| **源码与构建** | `foundation/multimedia/camera_framework/test/camera_record/`；**`./build.sh --build-target camera_record --product-name rk3568`**；**`camera_framework/bundle.json` → `fwk_group`** 已含 **`//foundation/.../test/camera_record:camera_record`**；部件 **`deps.components`** 需含 **`player_framework`**（Recorder）。 |
| **权限** | 原生 token：**`ohos.permission.CAMERA`**、**`ohos.permission.MICROPHONE`**（与录像含音轨一致）。 |
| **子命令** | **`cam-build` / `cam-prep` / `cam-push` / `cam-run`**；**`cam-run --pull`** 优先解析 stdout 中的 **`camera_record: done <path>`**，若缺失则自动回退抓取 **`/data/local/tmp`** 下最新 `camera_record_*.mp4`，并 **`hdc file recv`** 到 **`src/skills/ohrecord/recv/`**。推荐直接使用 **`cam-run --pull --verify`**。 |
| **CLI** | **`auto [秒] [绝对路径.mp4]`** 默认 **10 秒**；**`start [绝对路径.mp4]`** 持续录制直到 **`stop`**；默认文件落 **`/data/local/tmp`**。 |
| **设备二进制** | 默认 **`/data/local/tmp/camera_record`**（**`cam-push`** 推送并 **`chmod 755`**）。 |
| **画质/帧率排障** | 大块发黑「抠图」、低 fps、时长漂移等已写入 **§6.8～§6.11**；改 **`main_ndk.cpp`** 前先读 **§6.9（NEON 溢出）**。 |

---

## 三、与 ohproj / ohbuild / ohhdc / ohservices 的关系

- **ohproj**：原生 HAP 工程流程；**系统镜像与 snapshot_record 无 HAP 依赖**，但 **ohproj/SKILL.md 第十节** 汇总了本次系统侧改动的全文档。
- **ohbuild**：**部件单编时 `--build-target` 使用 GN 目标名**（如 `audio_record_demo`），**不要**写成 `foundation/.../audio_record_demo:audio_record_demo`；详见 **`src/skills/ohbuild/SKILL.md`**。**ohrecord.py `audio-build`** 已按此约定调用 `build.sh`。
- **ohhdc**：通用 `hdc shell` / 安装 HAP；**ohrecord.py** 覆盖 **snapshot_record**、**audio_record_demo**、**audio_play_demo**、**camera_record** 的推送与运行及 **`recv/`** 拉取。
- **ohservices / ohsa.py**：需要 **`dmesg` / 落盘 hilog / 多部件诊断** 时可配合使用。

---

## 四、文档与代码规范

- 修改须符合各部件既有 **MEDIA_LOG / CHECK_AND_RETURN** 等风格；SELinux 禁止为 `media_service` 增加违反 **`domain.te` neverallow** 的 **`data_file:file { create write }`**，应使用 **`data_test_media_file`** + 路径 **`/data/test/media`**。
- 具体文件列表与修改原因见 **ohproj/SKILL.md §10.3**。

---

## 五、camera_record_demo 成功复现与排障手册（本次实战沉淀）

本节只针对 **`camera_framework/test/camera_record_demo/main_ndk.cpp`** 这条录像链路，记录这次从 `0` 字节/`1009` 字节 MP4 到最终生成 **真实 H.264 MP4** 的完整经验，后续再次创建或迁移 `camera_record_demo` 时可直接照此执行。

### 5.1 最终成功结果

- 设备端成功文件：`/data/test/media/camera_record_20260401_181255.mp4`
- 本地拉回文件：`out/rk3568/camera_record_20260401_181255.mp4`
- 文件大小：约 **2.79 MB**
- 解析 `mvhd` 得到时长：约 **8.048s**
- 视频 sample entry：**`avc1`**

### 5.2 最终有效改动

#### A. 避开 `CreateCaptureSession()` 前段的阻塞

在 `HCameraService::CreateCaptureSession()` 中，`HILOG_COMM_INFO("opMode_=...")` 之后原本会调用：

```cpp
CameraReportUtils::GetInstance().updateModeChangePerfInfo(opMode, CameraReportUtils::GetCallerInfo());
```

本次板子上，这一步会把客户端侧 `OH_CameraManager_CreateCaptureSession()` 调用拖进 **binder_ioctl_write_read**，表现为：

- demo 设备侧 stdout 只剩：`camera_record_demo: before CreateCaptureSession`
- service 侧只出现：`HCameraService::CreateCaptureSession opMode_= 0`
- 之后无 `callerToken` / `before NewInstance` / `userId=` 等后续日志

调试时可临时改成：

```cpp
MEDIA_INFO_LOG("HCameraService::CreateCaptureSession skip updateModeChangePerfInfo");
```

也就是**先旁路 perf-reporting IPC**，优先恢复录像主功能。

#### B. 避开 PreviewOutput 回调触发的客户端 CFI 崩溃

`camera_record_demo` 注册了 `OH_PreviewOutput_RegisterCallback()` 后，`VideoOutputStart` 后不久会在客户端 `OS_IPC` 线程触发 **CFI crash**，典型 fault 栈：

- `__cfi_check_fail`
- `libohcamera.so`
- `OHOS::CameraStandard::InnerPreviewOutputCallback::OnFrameStarted() const`

现象：

- `CreateCaptureSession ok`
- `VideoOutputStart ret=0`
- 随后 demo 被 `SIGABRT`
- `camera_host` / `camera_hdi_service` 开始连带报 `412 consumer unregister listener` 或 `504 binder occur error`
- 录像文件为 `0` 字节或极小壳文件

调试/恢复主功能时，先**删除 preview callback 注册**：

```cpp
// PreviewOutput_Callbacks previewCallbacks = { ... };
// OH_PreviewOutput_RegisterCallback(previewOutput, &previewCallbacks);
```

本次成功就是在**去掉 preview callback** 后拿到真实 mp4 的。

### 5.3 最后保留的关键行为

- 仍然保留 `previewConsumer` 的 drain thread（持续 `AcquireBuffer/ReleaseBuffer`）
- `OH_CaptureSession_SetSessionMode(session, NORMAL_VIDEO)` 保持在 `BeginConfig` 之前
- 录像启动顺序仍采用：
  1. `OH_CaptureSession_Start(session)`
  2. `OH_VideoOutput_Start(videoOutput)`
  3. `sleep 400ms`
  4. `recorder->Start()`

不要默认改成“先 `recorder->Start()` 再 `VideoOutputStart()`”；本次多轮实验说明该改动会把问题推到别的地方，不能稳定解决。

### 5.4 这次碰到的主要问题与判断方法

#### 问题 1：MP4 为 0 字节或 1009 字节

判断：

- 设备目录出现 `camera_record_*.mp4`
- 文件大小是 `0` 或约 `1009`
- 没有真实 `moov/mvhd` 有效时长

高概率原因：

- `camera_hdi_service` 持续报 **`412 consumer unregister listener`**
- recorder surface consumer 没真正就绪或被中途打断
- 或客户端先崩导致后续链路全断

#### 问题 2：demo 只打印 `before CreateCaptureSession`

判断：

- 设备侧真实 stdout 只到这一行
- `camera_service` 只看到 `opMode_=0`

做法：

- 不要只看 stdout
- 同时看 `hilog`
- 必要时在 `CreateCaptureSession()` 里加连续前后日志
- 本次最终发现是 `updateModeChangePerfInfo()` 导致的前段阻塞

#### 问题 3：`VideoOutputStart` 后 demo CFI 崩溃

判断：

- `faultlogger` 生成新的 `cppcrash-camera_record_demo-*.log`
- fault thread 常在 `OS_IPC_*`
- 栈里出现：
  - `__cfi_check_fail`
  - `libohcamera.so`
  - `InnerPreviewOutputCallback::OnFrameStarted()`

做法：

- 先停用 `OH_PreviewOutput_RegisterCallback()`
- 重新编译 demo
- 再继续观察录像链路本体

#### 问题 4：以为输出文件在 `/data/local/tmp/*.mp4`

本次是典型误判。

实际代码：

```cpp
int main(int argc, char** argv)
{
    setvbuf(stdout, nullptr, _IONBF, 0);
    SetupNativeToken();
    int sec = kDefaultAutoSec;
    if (argc >= 3 && argv[2] != nullptr) {
        sec = std::max(1, atoi(argv[2]));
    }
    return RunRecord(DefaultOutputPath(), sec);
}
```

`argv[1]` 没被使用，真实输出始终来自：

```cpp
strftime(name, sizeof(name), "/data/test/media/camera_record_%Y%m%d_%H%M%S.mp4", &tmBuf);
```

所以后续排查时必须优先查：

```bash
ls -lt /data/test/media/camera_record_*.mp4 | head
```

### 5.5 推荐的调试/验证步骤

#### 第 1 步：准备设备目录

```bash
python3 src/skills/ohrecord/ohrecord.py prep-device
```

确认 `/data/test/media` 存在且具备 `data_test_media_file` 相关上下文。

#### 第 2 步：推送 demo

```bash
python3 src/skills/ohrecord/ohrecord.py cam-build --product rk3568
python3 src/skills/ohrecord/ohrecord.py cam-push --product rk3568
```

#### 第 3 步：如果调试 service 逻辑，手工替换 `libcamera_service.z.so`

本次手工单编/重链流程可复用：

1. 从 `out/rk3568/obj/.../camera_service.ninja` 找到：
   - `hcamera_service.o` 的 `cxx` 规则
   - `libcamera_service.z.so` 的 `solink` 规则
2. 用 `toolchain.ninja` 里的 `rule cxx` 手工重编 `hcamera_service.o`
3. 手工构造 `libcamera_service.z.so.rsp`
4. 用：

```bash
../../build/toolchain/gcc_solink_wrapper.py ... -- clang++ -shared ...
```

重链 `libcamera_service.z.so`

5. 上板替换：

```bash
hdc file send out/rk3568/multimedia/camera_framework/libcamera_service.z.so /data/local/tmp/libcamera_service.z.so
hdc shell 'mount --bind /data/local/tmp/libcamera_service.z.so /system/lib/libcamera_service.z.so'
hdc shell 'killall camera_service 2>/dev/null'
```

确认生效：

```bash
hdc shell 'strings /system/lib/libcamera_service.z.so | grep -F "skip updateModeChangePerfInfo"'
```

#### 第 4 步：运行并拉取

```bash
python3 src/skills/ohrecord/ohrecord.py cam-run --pull -- auto 10
```

若 demo 没打印 `done`，脚本会自动回退找最新 `camera_record_*.mp4`。

#### 第 5 步：验证成功而不是“假成功”

至少做以下检查：

```bash
hdc shell 'ls -lt /data/test/media/camera_record_*.mp4 | head -n 3'
```

成功时应看到：

- 最新文件大小明显大于 `1009`
- 通常为数百 KB 到数 MB

再拉回本地检查：

```bash
python3 src/skills/ohrecord/ohrecord.py pull --remote /data/test/media/camera_record_xxx.mp4
```

若本机无 `ffprobe`，可用简单 MP4 解析脚本读取：

- `moov/mvhd.timescale`
- `mvhd.duration`
- `stsd` 视频 sample entry 是否为 `avc1`

本次成功文件验证结果：

- `size_bytes=2794968`
- `duration_seconds=8.048`
- `video_sample_entry=avc1`

### 5.6 本次最终建议保留的固化经验

1. `cam-run --pull` 不要只依赖 stdout 里的 `done` 路径
2. 默认把 camera 录像真实输出路径认定为 `/data/test/media/camera_record_*.mp4`
3. 如果 demo 先崩，再看 `faultlogger`，不要只盯 `412`
4. 如果 service 只打印 `opMode_=0`，优先检查 `updateModeChangePerfInfo()` 一类前置 IPC
5. 调通录像主功能前，先关掉容易触发跨 DSO CFI 的 preview callback

---

## 六、camera_record 颜色修复与时长排障手册（当前固化链路）

本节针对当前默认使用的 **`foundation/multimedia/camera_framework/test/camera_record/main_ndk.cpp`**，记录“颜色正确但 `RGBA` 直通 recorder 不稳定”的板级修复过程，以及随后出现的 **MP4 时长异常** 排查方法。

### 6.1 当前链路结论

- **颜色问题**：已修正，当前样本已恢复为**单画面**且颜色与预览基本一致。
- **核心策略**：不再走 board 上已证实不可靠的 **camera RGBA -> recorder RGBA** 直通链路。
- **当前实现**：改为 **preview consumer 取 `RGBA8888` 帧 -> 本地转换 `NV12` -> 写入 recorder 的 `VIDEO_SOURCE_SURFACE_YUV` input surface**。

也就是：

```text
camera preview(RGBA8888)
  -> previewConsumer AcquireBuffer
  -> ConvertRgba8888ToNv12()
  -> OH_NativeWindow_RequestBuffer(recorder surface)
  -> SET_UI_TIMESTAMP
  -> FlushBuffer
  -> recorder / avc encoder
```

### 6.2 为什么必须绕开 recorder 的 RGBA 直通

本板上 camera capability 只给出：

- `video[0] format=3 size=640x480 fps=5-10`
- `preview[0] format=3 size=640x480`

进一步抓到 preview raw buffer 后确认：

- 相机送出的就是正常 `RGBA8888`
- 典型参数：`width=640 height=480 stride=2560 size=1228800`

但继续深挖编码侧后发现：

- `GraphicPixelFormat::GRAPHIC_PIXEL_FMT_RGBA_8888`
- -> `VideoPixelFormat::RGBA`
- -> AVC encoder 内部却落到 `COLOR_FORMAT::YUV_420SP_VU`

这就是此前出现：

- 四宫格 / 4 tiled screens
- 颜色严重偏差
- 或 recorder 直接报错、只留下极小壳文件

的根因之一。因此当前技能建议把 **RGBA 先在本地转 YUV(NV12)**，再交给 recorder。

### 6.3 当前 camera_record 关键实现点

#### A. recorder 统一配置为 YUV surface

- `CreateAndConfigureRecorder(..., VIDEO_SOURCE_SURFACE_YUV)`
- `recorder->GetSurface(videoSourceId)`
- `recordSurface` 包成 `OHNativeWindow`
- `SET_FORMAT = GRAPHIC_PIXEL_FMT_YCBCR_420_SP`

#### B. camera 侧只保留 PreviewOutput

当前 `camera_record` 的有效录像数据来源是：

- `OH_CameraManager_CreatePreviewOutput(...)`
- `previewConsumer->AcquireBuffer(...)`

而不是再让 camera 的 `VideoOutput` 直接喂 recorder surface。

#### C. 本地执行 RGBA -> NV12 转换

在 `main_ndk.cpp` 中使用本地函数：

- `ConvertRgba8888ToNv12(...)`
- `WritePreviewFrameToRecorderWindow(...)`

流程是：

1. 从 `previewBuffer->GetVirAddr()` 读 `RGBA8888`
2. `OH_NativeWindow_NativeWindowRequestBuffer(recorderWindow, ...)`
3. `OH_NativeBuffer_Map()`
4. 把目标 buffer 的 Y / UV 平面按 NV12 写入
5. `SET_UI_TIMESTAMP`
6. `OH_NativeWindow_NativeWindowFlushBuffer(...)`

### 6.4 颜色修复后的新问题：时长异常

颜色修好之后，录像能稳定生成非空 MP4，但先后出现过三类时长异常：

#### 情况 1：播放器显示 0 秒

典型现象：

- 文件大小正常（例如 1MB~3MB）
- `ftyp` 正常
- 但播放器时长显示为 `0`

这类通常不是“播放器 bug”，而是 **容器里的时长元数据就被写坏了**。

#### 情况 2：`auto 10` 录出约 6.9 秒

典型样本：

- `pushed frames=62`
- MP4 解析结果：`mvhd_seconds ≈ 6.9`

这说明：

- 容器字段不再是 0
- 但送给 recorder 的时间轴是**固定帧率人造时间轴**
- 实际帧输入数量又明显低于理论值

于是“实际只送 62 帧”被解释成了 `6.9s`

#### 情况 3：`auto 10` 录出约 14.25 秒 / 11.8 秒

这说明又走到了另一类错误：

- 时间戳单位虽然修过
- 但**录制开始计时点**和**开始向 recorder 送帧的时刻**没有对齐
- 再叠加原来的 warmup / stop polling 粒度，就会把总时长拉长

### 6.5 时长异常的根因分类

#### 根因 A：`SET_UI_TIMESTAMP` 单位理解错误

若把 `SET_UI_TIMESTAMP` 当作 `us` 或混入绝对时间使用，会看到：

- `mvhd_seconds` 明显不合理
- `stts` 前几项 delta 异常大或异常小

本次验证里，错误版本曾出现：

- `mvhd_seconds = 92.192`
- `stts_entries = [(1, 8287692), (60, 9), (1, 9000)]`

这就是典型的**单位不对 + 基准点不对**。

#### 根因 B：按固定帧率假设生成时间轴

如果代码写成：

```cpp
pts += frameIntervalNs;
```

但实际 preview drain 线程并没有稳定拿到目标 fps 的帧，那么：

- `sample_count` 会少
- `stts_total_seconds` 会偏短

#### 根因 C：开始送帧与 `recorder->Start()` 没对齐

如果在：

- `recorder->Start()` 之前就开始送帧
- 或 `Start()` 之后又额外 sleep/warmup

那么 `auto 10` 的输出通常会偏长。

### 6.6 推荐的时长排查方法

不要只看播放器显示。优先做下面三步。

#### 第 1 步：看设备端日志

重点关注：

- `camera_record: recording -> ...`
- `camera_record: pushed frames=<N>`
- `camera_record: done ...`

其中：

- `pushed frames` 能告诉你这次到底实际喂了多少帧
- 如果 `auto 10` 只有 50~60 帧，那就不能再假定是稳定 10fps

#### 第 2 步：用 `cam-inspect` 看 MP4 容器元数据

```bash
python3 src/skills/ohrecord/ohrecord.py cam-inspect \
  --local src/skills/ohrecord/recv/camera_record_xxx.mp4
```

重点看：

- `mvhd_seconds`
- `mdhd_seconds`
- `stts_seconds`
- `sample_count`
- `stts_first_entries`

判断逻辑：

- **`mvhd/mdhd/stts` 都接近 0**：时间戳几乎没递增
- **`sample_count` 太少且时长偏短**：按固定 fps 假设写时间轴，但实际送帧不足
- **首个 `stts` entry` 明显超大**：起始基准时间/单位有问题
- **总时长明显偏长**：开始送帧时刻早于真正开始计时，或 stop 边界太松

#### 第 3 步：把 `cam-run --pull --verify` 当成标准流程

```bash
python3 src/skills/ohrecord/ohrecord.py cam-run --pull --verify -- auto 10
```

这条命令已经固化了：

- 设备端存在性检查
- 文件大小检查
- `ftyp` 头检查
- 拉回本地
- 本地 MP4 元数据摘要打印

### 6.7 当前建议保留的经验

1. 颜色问题优先通过 **RGBA -> NV12 本地转换** 解决，不要再赌 board 上的 RGBA 直通 recorder。
2. 看“时长有问题”时，必须把问题拆成：
   - 容器时长字段坏了
   - 还是时间轴逻辑不准
3. 先看 `pushed frames=<N>`，再决定是否能按固定 fps 推断时间。
4. `SET_UI_TIMESTAMP` 一定要谨慎处理单位与基准点；混入绝对时间很容易把 `stts` 打坏。
5. 后续若再改 `camera_record` 的时长逻辑，必须用 **`cam-inspect`** 对比：
   - `mvhd_seconds`
   - `mdhd_seconds`
   - `stts_seconds`
   - `sample_count`
   而不是只看播放器 UI。
6. 若改 **RGBA→NV12 的 SIMD**，必须先读 **§6.9**，避免 int16 溢出再现「抠图」假像。

### 6.8 帧率偏低与 preview drain 优化（已固化）

**典型现象**

- 设备日志 `pushed frames` 只有 **40～55**（10s 录制），`cam-inspect` 折算约 **4～5fps**。
- 运动物体**拖影**重，观感像幻灯片。

**根因归纳**

1. **`AcquireBuffer` 失败分支里 `sleep(10ms)`**  
   队列一空就按 10ms 节拍等，轮询上限约 **100Hz**，叠加每帧转码耗时，有效帧率被压得很低。

2. **预览 BufferQueue 默认深度为 3**（`SURFACE_DEFAULT_QUEUE_SIZE`）  
   单线程路径里要 `Acquire` + `RequestBuffer` + `Map` + **RGBA→NV12** + `Flush`，处理偏慢时**相机侧易堵、易丢帧**。

3. **整帧 RGBA→NV12 纯标量 C 循环**在嵌入式上偏重（Y 平面占大头）。

**已在 `main_ndk.cpp` 固化的改动**

| 项 | 说明 |
|----|------|
| **`SetQueueSize(8)`** | 在 `IConsumerSurface::Create()` 之后尽早调用；日志行：`preview consumer SetQueueSize(8) ret=...` |
| **空队列等待** | 改为 `std::this_thread::yield()` + **`sleep(200µs)`**，禁止再用 **10ms** |
| **NEON 加速 Y 平面** | UV 仍标量，降低 CPU 占用、缩短持锁时间 |
| **NV12 预览快路径** | `PickNv12PreviewMatchingVideoSize`：若能力表存在与 **video 同尺寸**的 **`CAMERA_FORMAT_YUV_420_SP`** 预览，则选用该 profile；`WritePreviewFrameToRecorderWindow` 对 **`GRAPHIC_PIXEL_FMT_YCBCR_420_SP`** 走 **memcpy**，跳过 RGBA 转码（**本板仅 RGBA 预览时此分支不命中**） |

**实测对比（rk3568，`auto 10`）**

- 优化前：约 **44** 帧，折算 **~4.5fps**。
- 优化后：约 **74** 帧，折算 **~7.5fps**（能力表 **fps=5–10**，剩余差距多在 **NativeWindow Map/Flush 与编码消费**）。

### 6.9 画质雷区：NEON 用 int16 累加 Y →「抠图」大块发黑（必读）

**典型现象**

- 成片里**大面积纯黑**、只残留少量前景，像**抠图/遮罩**坏了。
- **上一轮纯标量转码**画面正常，**一加 NEON 就变样**。

**根因（确定性）**

- Y（BT601 限幅）常用：  
  `Y = ((66*R + 129*G + 25*B + 128) >> 8) + 16`
- 当 **R、G、B 接近 255** 时，括号内和约 **56227**，**超过 `int16` 最大值 32767**。
- 若 NEON 用 **`int16x8` 做该和式的向量累加**，会发生**有符号溢出**，Y 变成乱值 → 大量接近 **0（黑）** → H.264 压缩后表现为**大块内容「被吃掉」**。

**硬性规则**

- 对上述和式做 SIMD 时，**中间必须用 `int32x4`（或更宽）累加**，再饱和窄化到 8bit。
- **禁止**用 int16 向量承载 **`66*R+129*G+25*B+128`** 的完整未右移和。

**修复后验证**

- 同场景录像应恢复**连续背景与亮部**；可参考已拉回的 **`camera_record_20260402_143324.mp4`** 一类样本做对比。

### 6.10 时长边界（与上述轮次同期固化）

| 项 | 说明 |
|----|------|
| 首帧 PTS | 至少 **1ms**（`kMinFirstPtsNs`），避免 `stts` 首项 **`(1, 0)`** |
| `auto N` 计时 | 使用 **`steady_clock` 绝对截止时间**，避免 `elapsed += kPollMs` 长期漂移 |
| 停止送帧 | `Stop` 前 **`previewPushEnabled = false`** + 短 **settle**，减少尾部多送帧导致 **`mvhd` 偏长** |

### 6.11 再改 `camera_record` 时的回归清单（建议照单执行）

1. `./build.sh --build-target camera_record --product-name rk3568`
2. `python3 src/skills/ohrecord/ohrecord.py cam-push --product rk3568`
3. `python3 src/skills/ohrecord/ohrecord.py cam-run --pull --verify -- auto 10`
4. `python3 src/skills/ohrecord/ohrecord.py cam-inspect --local src/skills/ohrecord/recv/camera_record_*.mp4`（取最新）
5. **肉眼**：全图亮度连续、**无大块黑**、无色偏与四宫格
6. 若修改 **SIMD 颜色转换**：**§6.9** 逐条自检，并可在白场/肤色/灰背景上与标量结果**抽点比对**
