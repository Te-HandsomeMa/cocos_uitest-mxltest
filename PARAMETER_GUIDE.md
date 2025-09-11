# 测试配置参数说明文档

## 概述

本文档详细说明了 `test_config.yaml` 配置文件和 `run_tests.py` 脚本的参数配置和使用方法。

## 1. test_config.yaml 配置文件参数

### 1.1 运行环境配置 (environment)

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `is_mobile` | boolean | ✅ | - | 是否在移动端运行 (True: 移动端, False: PC浏览器) |
| `device_type` | string | ✅ | - | 设备类型，可选值：`android`、`ios`、`pc` |
| `device_id` | string | 条件必填 | - | 设备ID，移动端必填，PC端可为空。格式：`IP:端口` 或设备序列号 |
| `enable_recording` | boolean | ❌ | false | 是否启用截图记录功能 |

**示例：**
```yaml
environment:
  is_mobile: True
  device_type: "android"
  device_id: "172.16.36.4:5555"
  enable_recording: false
```

### 1.2 测试范围配置 (test_scope)

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `max_chapter` | integer | ❌ | null | 运行的最大章节数 (1-7)，null表示运行所有章节 |
| `skip_chapters` | array | ❌ | [] | 要跳过的章节列表，例如：[2, 5] |
| `specific_chapters` | array | ❌ | [] | 只运行特定章节，例如：[1, 3, 7] |

**示例：**
```yaml
test_scope:
  max_chapter: 7
  skip_chapters: [2, 5]  # 跳过第2章和第5章
  specific_chapters: [1, 3, 7]  # 只运行第1、3、7章
```

### 1.3 服务器配置 (server)

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `ws_port` | integer | ❌ | 5101 | WebSocket服务器端口 |
| `auto_start_server` | boolean | ❌ | true | 是否自动启动服务器 |

**示例：**
```yaml
server:
  ws_port: 5101
  auto_start_server: true
```

### 1.4 执行脚本配置 (execution)

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `script_file` | string | ✅ | - | 要执行的脚本文件名 (相对于scripts目录) |
| `script_args` | array | ❌ | [] | 传递给脚本的额外参数 |
| `parallel_execution` | boolean | ❌ | false | 是否并行执行多个脚本 |
| `parallel_scripts` | array | ❌ | [] | 要并行执行的脚本列表 |

**示例：**
```yaml
execution:
  script_file: "guide_test_Android.py"
  script_args: ["--verbose", "--debug"]
  parallel_execution: false
  parallel_scripts: []
```

### 1.5 日志配置 (logging)

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `log_file` | string | ❌ | "logs/run_{timestamp}.log" | 日志文件路径，{timestamp}会被替换为时间戳 |

**示例：**
```yaml
logging:
  log_file: "logs/run_{timestamp}.log"
```

### 1.6 测试数据配置 (test_data)

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `data_file` | string | ❌ | "configs/element_data.py" | 测试数据文件路径 |
| `use_default_data` | boolean | ❌ | true | 是否使用默认测试数据 |

**示例：**
```yaml
test_data:
  data_file: "configs/element_data.py"
  use_default_data: true
```

## 2. run_tests.py 命令行参数

### 2.1 基本参数

| 参数 | 简写 | 类型 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--config` | `-c` | string | test_config.yaml | 指定配置文件路径 |
| `--validate-only` | - | flag | false | 仅验证配置文件，不执行测试 |

### 2.2 使用示例

#### 基本使用
```bash
# 使用默认配置文件运行测试
python3 run_tests.py

# 使用自定义配置文件
python3 run_tests.py -c my_config.yaml

# 仅验证配置文件
python3 run_tests.py --validate-only
```

#### 配置文件验证
```bash
# 验证默认配置文件
python3 run_tests.py --validate-only

# 验证自定义配置文件
python3 run_tests.py -c custom_config.yaml --validate-only
```

## 3. 完整配置示例

### 3.1 Android 设备测试配置
```yaml
# test_config.yaml
environment:
  is_mobile: True
  device_type: "android"
  device_id: "172.16.36.4:5555"
  enable_recording: true

test_scope:
  max_chapter: 7
  skip_chapters: []

server:
  ws_port: 5101
  auto_start_server: true

execution:
  script_file: "guide_test_Android.py"
  script_args: []

logging:
  log_file: "logs/android_test_{timestamp}.log"

test_data:
  data_file: "configs/element_data.py"
  use_default_data: true
```

### 3.2 iOS 设备测试配置
```yaml
# test_config.yaml
environment:
  is_mobile: True
  device_type: "ios"
  device_id: "00008020-000A1A1A12345678"
  enable_recording: false

test_scope:
  max_chapter: 5
  skip_chapters: [6, 7]

server:
  ws_port: 5102
  auto_start_server: true

execution:
  script_file: "guide_test_IOS.py"
  script_args: ["--verbose"]

logging:
  log_file: "logs/ios_test_{timestamp}.log"

test_data:
  data_file: "configs/element_data.py"
  use_default_data: true
```

### 3.3 PC 浏览器测试配置
```yaml
# test_config.yaml
environment:
  is_mobile: False
  device_type: "pc"
  device_id: ""
  enable_recording: true

test_scope:
  max_chapter: 3
  specific_chapters: [1, 2, 3]

server:
  ws_port: 5103
  auto_start_server: true

execution:
  script_file: "guide_test_WechatApp.py"
  script_args: []

logging:
  log_file: "logs/pc_test_{timestamp}.log"

test_data:
  data_file: "configs/element_data.py"
  use_default_data: true
```

## 4. 常见使用场景

### 4.1 快速测试特定章节
```yaml
test_scope:
  specific_chapters: [1, 3, 5]  # 只测试第1、3、5章
```

### 4.2 跳过有问题的章节
```yaml
test_scope:
  max_chapter: 7
  skip_chapters: [2, 4]  # 跳过第2章和第4章
```

### 4.3 调试模式运行
```yaml
execution:
  script_file: "guide_test_Android.py"
  script_args: ["--debug", "--verbose"]
```

### 4.4 启用截图记录
```yaml
environment:
  enable_recording: true
```

## 5. 注意事项

1. **设备ID格式**：
   - Android: `IP:端口` (如: `172.16.36.4:5555`) 或设备序列号
   - iOS: 设备UDID (如: `00008020-000A1A1A12345678`)
   - PC: 可为空字符串

2. **章节范围**：
   - 章节编号从1开始
   - `max_chapter` 和 `specific_chapters` 不能同时使用
   - `skip_chapters` 可以与 `max_chapter` 配合使用

3. **脚本文件**：
   - 脚本文件必须存在于 `scripts/` 目录下
   - 文件名不需要包含路径，只需要文件名

4. **日志文件**：
   - 日志目录会自动创建
   - `{timestamp}` 会被自动替换为当前时间戳

5. **配置文件验证**：
   - 建议在运行前使用 `--validate-only` 参数验证配置
   - 验证失败时会显示具体的错误信息

## 6. 故障排除

### 6.1 常见错误

1. **配置文件不存在**
   ```
   FileNotFoundError: 配置文件不存在: test_config.yaml
   ```
   解决：确保配置文件存在于项目根目录

2. **设备ID缺失**
   ```
   ValueError: 移动端运行需要提供 device_id
   ```
   解决：为移动端测试配置正确的设备ID

3. **脚本文件不存在**
   ```
   FileNotFoundError: 脚本文件不存在: scripts/guide_test_Android.py
   ```
   解决：确保指定的脚本文件存在于scripts目录

4. **YAML格式错误**
   ```
   ValueError: YAML配置文件格式错误
   ```
   解决：检查YAML文件的语法和缩进

### 6.2 调试建议

1. 使用 `--validate-only` 参数验证配置
2. 检查设备连接状态
3. 确认端口未被占用
4. 查看日志文件获取详细错误信息
