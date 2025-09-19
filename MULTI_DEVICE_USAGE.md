# 多设备测试使用指南

## 概述

本系统现在支持多设备并行/串行测试，无需手动切换终端和修改配置文件。

## 配置文件

### 多设备配置文件 (multi_device_config.yaml)

```yaml
# 多设备配置
devices:
  - name: "Android设备1"
    device_id: "172.16.36.4:5555"
    device_type: "android"
    ws_port: 5101
    max_chapter: 7
    skip_chapters: []
    script_file: "guide_test_Android.py"
    enable_recording: false
    
  - name: "iOS设备1"
    device_id: "iPhone_12_Pro"
    device_type: "ios" 
    ws_port: 5102
    max_chapter: 7
    skip_chapters: []
    script_file: "guide_test_IOS.py"
    enable_recording: false
    
  - name: "Android设备2"
    device_id: "172.16.36.5:5555"
    device_type: "android"
    ws_port: 5103
    max_chapter: 5
    skip_chapters: [6, 7]
    script_file: "guide_test_Android.py"
    enable_recording: false

# 执行策略配置
execution:
  mode: "parallel"  # parallel | sequential
  max_concurrent: 3  # 最大并发设备数
  wait_for_completion: true  # 是否等待所有设备完成
```

### 单设备配置文件 (test_config.yaml) - 向后兼容

原有的单设备配置文件仍然完全支持，无需修改。

## 使用方法

### 1. 多设备测试

```bash
# 使用多设备配置
python3 run_tests.py --config multi_device_config.yaml
```

### 2. 单设备测试（向后兼容）

```bash
# 使用原有单设备配置
python3 run_tests.py --config test_config.yaml
```

### 3. 配置验证

```bash
# 仅验证配置文件
python3 run_tests.py --config multi_device_config.yaml --validate-only
```

## 执行模式

### 并行执行模式 (parallel)

- 所有设备同时运行测试
- 可设置最大并发数
- 适合资源充足的环境

### 串行执行模式 (sequential)

- 设备按顺序依次运行测试
- 适合资源有限的环境
- 便于调试和监控

## 日志和报告

### 日志文件

每个设备生成独立的日志文件：

```
logs/
├── device_android_172.16.36.4_5555_5101_20250912_143238.log
├── device_ios_iPhone_12_Pro_5102_20250912_143238.log
└── device_android_172.16.36.5_5555_5103_20250912_143238.log
```

### 报告文件

每个设备生成独立的HTML报告：

```
reports/
├── test_report_android_172.16.36.4_5555_20250912.html
├── test_report_ios_iPhone_12_Pro_20250912.html
└── test_report_android_172.16.36.5_5555_20250912.html
```

## 设备配置说明

### 必需字段

- `name`: 设备名称（唯一标识）
- `device_id`: 设备ID
- `device_type`: 设备类型 (android/ios/pc)
- `ws_port`: WebSocket端口号
- `script_file`: 要执行的脚本文件

### 可选字段

- `max_chapter`: 最大章节数（默认7）
- `skip_chapters`: 跳过的章节列表
- `enable_recording`: 是否启用截图记录

## 端口管理

- 系统会自动检测端口冲突
- 如果指定端口被占用，会自动分配可用端口
- 端口范围：5101-65535

## 设备状态检查

启动前会检查设备状态：

- **Android设备**: 检查ADB连接
- **iOS设备**: 检查WDA连接
- **PC设备**: 直接标记为可用

## 执行结果

### 成功示例

```
📊 执行结果汇总:

├── Android设备1: ✅ 成功 - 耗时: 245.32秒
├── iOS设备1: ✅ 成功 - 耗时: 267.18秒
└── Android设备2: ✅ 成功 - 耗时: 198.45秒

📈 统计信息:
├── 总设备数: 3
├── 成功设备数: 3
├── 失败设备数: 0
├── 成功率: 100.0%
└── 总耗时: 267.18秒

🎉 所有设备测试完成！
```

### 失败示例

```
📊 执行结果汇总:

├── Android设备1: ✅ 成功 - 耗时: 245.32秒
├── iOS设备1: ❌ 失败 - 耗时: 45.67秒
│   └── 错误: 设备连接超时
└── Android设备2: ✅ 成功 - 耗时: 198.45秒

📈 统计信息:
├── 总设备数: 3
├── 成功设备数: 2
├── 失败设备数: 1
├── 成功率: 66.7%
└── 总耗时: 245.32秒

⚠️  部分设备测试失败，请检查日志文件
```

## 故障排除

### 常见问题

1. **端口冲突**
   - 系统会自动分配可用端口
   - 检查是否有其他程序占用端口

2. **设备连接失败**
   - 检查ADB连接 (Android)
   - 检查WDA连接 (iOS)
   - 确认设备ID正确

3. **脚本文件不存在**
   - 确认脚本文件路径正确
   - 检查scripts目录

### 调试建议

1. 使用 `--validate-only` 参数验证配置
2. 检查设备状态和连接
3. 查看详细的日志文件
4. 从单设备测试开始，逐步扩展到多设备

## 性能优化

### 并行执行优化

- 根据系统资源调整 `max_concurrent` 参数
- 监控内存和CPU使用情况
- 避免同时运行过多设备

### 资源管理

- 系统会自动清理资源
- 测试结束后释放端口和进程
- 异常情况下也会进行资源清理

## 扩展功能

### 自定义设备配置

可以轻松添加新设备：

```yaml
devices:
  - name: "新设备"
    device_id: "新设备ID"
    device_type: "android"
    ws_port: 5104
    max_chapter: 3
    skip_chapters: [4, 5, 6, 7]
    script_file: "guide_test_Android.py"
```

### 混合设备类型

支持同时运行不同类型的设备：

- Android + iOS + PC
- 不同版本的Android设备
- 不同型号的iOS设备

## 总结

多设备测试功能提供了：

- ✅ 一个命令管理所有设备
- ✅ 自动端口分配和资源管理
- ✅ 独立日志和报告生成
- ✅ 并行和串行执行模式
- ✅ 完整的向后兼容性
- ✅ 详细的执行结果统计

现在你可以轻松地在多个设备上同时运行测试，无需手动切换终端或修改配置文件！
