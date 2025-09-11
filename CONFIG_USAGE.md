# YAML配置系统使用说明

## 概述

本项目新增了基于YAML配置文件的测试执行系统，可以统一管理测试运行参数，包括设备类型、章节范围、脚本选择等。

## 文件结构

```
├── test_config.yaml              # 主配置文件
├── run_tests.py                  # 主执行脚本
├── common/config_manager.py      # 配置管理模块
├── config_examples/              # 配置示例目录
│   ├── ios_mobile_config.yaml
│   ├── android_mobile_config.yaml
│   ├── pc_browser_config.yaml
│   └── specific_chapters_config.yaml
└── CONFIG_USAGE.md              # 本说明文档
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置测试参数

编辑 `test_config.yaml` 文件，设置你的测试参数：

```yaml
environment:
  is_mobile: true
  device_type: "ios"
  device_id: "your_device_id_here"

test_scope:
  max_chapter: 7

execution:
  script_file: "guide_test_IOS.py"
```

### 3. 运行测试

```bash
# 使用默认配置文件
python3 run_tests.py

# 使用指定配置文件
python3 run_tests.py -c config_examples/ios_mobile_config.yaml

# 仅验证配置文件
python3 run_tests.py --validate-only
```

**执行方式说明：**
系统使用 `python3 -m scripts.script_name` 的方式执行测试脚本，这样可以正确处理模块导入路径，避免 `ModuleNotFoundError: No module named 'common'` 错误。

**自动构建的命令示例：**
```bash
# iOS移动端测试
python3 -m scripts.guide_test_IOS --mobile --device-id your_device_id --max-chapter 7

# Android移动端测试  
python3 -m scripts.guide_test_Android --mobile --device-id your_device_id --max-chapter 7

# PC浏览器测试
python3 -m scripts.guide_test_WechatApp --max-chapter 7
```

## 配置说明

### environment（环境配置）

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `is_mobile` | boolean | 是否在移动端运行 | `true` / `false` |
| `device_type` | string | 设备类型 | `"ios"` / `"android"` / `"pc"` |
| `device_id` | string/null | 设备ID（移动端必填） | `"iPhone_12_Pro"` |
| `enable_recording` | boolean | 是否启用截图记录 | `true` / `false` |

### test_scope（测试范围配置）

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `max_chapter` | integer/null | 最大章节数（1-7） | `7` |
| `skip_chapters` | array | 跳过的章节列表 | `[3, 5]` |
| `specific_chapters` | array | 只运行指定章节 | `[1, 3, 5]` |

### execution（执行配置）

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `script_file` | string | 要执行的脚本文件 | `"guide_test_IOS.py"` |
| `script_args` | array | 脚本参数 | `["--verbose"]` |
| `parallel_execution` | boolean | 是否并行执行 | `true` / `false` |

### server（服务器配置）

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `ws_port` | integer | WebSocket服务器端口 | `15004` |
| `auto_start_server` | boolean | 是否自动启动服务器 | `true` / `false` |

### logging（日志配置）

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `level` | string | 日志级别 | `"DEBUG"` / `"INFO"` / `"WARNING"` / `"ERROR"` |
| `log_file` | string | 日志文件路径 | `"logs/run_{timestamp}.log"` |
| `console_output` | boolean | 是否控制台输出 | `true` / `false` |

## 使用场景

### 场景1：iOS移动端测试

```bash
# 使用iOS配置
python run_tests.py -c config_examples/ios_mobile_config.yaml
```

### 场景2：Android移动端测试

```bash
# 使用Android配置
python run_tests.py -c config_examples/android_mobile_config.yaml
```

### 场景3：PC浏览器测试

```bash
# 使用PC配置
python run_tests.py -c config_examples/pc_browser_config.yaml
```

### 场景4：特定章节测试

```bash
# 只运行指定章节
python run_tests.py -c config_examples/specific_chapters_config.yaml
```

## 配置验证

系统会自动验证配置文件的完整性：

- 检查必需字段是否存在
- 验证字段值的类型和范围
- 检查脚本文件是否存在
- 验证设备配置的合理性

## 错误处理

常见错误及解决方案：

1. **配置文件不存在**
   ```
   FileNotFoundError: 配置文件不存在: test_config.yaml
   ```
   解决：确保配置文件路径正确

2. **YAML格式错误**
   ```
   ValueError: YAML配置文件格式错误
   ```
   解决：检查YAML语法，注意缩进和引号

3. **设备ID缺失**
   ```
   ValueError: 移动端运行需要提供 device_id
   ```
   解决：为移动端配置添加有效的device_id

4. **脚本文件不存在**
   ```
   FileNotFoundError: 脚本文件不存在
   ```
   解决：检查scripts目录下是否存在指定的脚本文件

## 高级用法

### 自定义配置模板

```python
from common.config_manager import ConfigManager

# 创建配置管理器
config_manager = ConfigManager()

# 创建配置模板
config_manager.create_config_template('my_config.yaml')
```

### 编程方式使用配置

```python
from common.config_manager import ConfigManager

# 加载配置
config_manager = ConfigManager('test_config.yaml')
config_manager.load_config()
config_manager.validate_config()

# 获取配置信息
is_mobile = config_manager.is_mobile()
device_id = config_manager.get_device_id()
max_chapter = config_manager.get_max_chapter()
```

## 注意事项

1. **设备ID**：移动端测试必须提供有效的设备ID
2. **章节范围**：章节号必须在1-7之间
3. **脚本文件**：确保scripts目录下存在指定的脚本文件
4. **端口冲突**：确保WebSocket端口未被占用
5. **权限问题**：确保有足够的权限访问设备和文件

## 更新日志

- **v1.0.0**: 初始版本，支持基本的YAML配置功能
- 支持iOS、Android、PC三种运行环境
- 支持章节范围控制
- 支持配置验证和错误处理
