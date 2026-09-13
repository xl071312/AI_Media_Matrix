# 【Phase 3 Chrome重启指南】

**当前问题**: CDP WebSocket连接被拒绝

**错误信息**:
```
Rejected an incoming WebSocket connection from the http://127.0.0.1:9222 origin.
Use --remote-allow-origins=http://127.0.0.1:9222
```

---

## 解决方案

### 步骤1: 完全关闭Chrome
1. 右键任务栏Chrome图标 → 退出
2. 确认所有Chrome窗口关闭
3. 检查任务管理器，确保没有chrome.exe残留

### 步骤2: 启动新Profile Chrome
打开CMD或PowerShell，运行：

```powershell
& "C:\Program Files\Google\Chrome\Application\chrome.exe" `
  --remote-debugging-port=9222 `
  --user-data-dir="C:\workspace\AI_Media_Matrix\browser_profiles\douyin_benchmark_v2" `
  --no-first-run `
  --no-default-browser-check `
  --remote-allow-origins=http://127.0.0.1:9222
```

### 步骤3: 登录抖音
1. Chrome打开后访问 `https://www.douyin.com`
2. 完成登录（二维码或手机号）
3. 如有验证码，**手动完成**
4. **保持窗口打开**

### 步骤4: 验证CDP
新命令行运行：
```powershell
curl.exe http://127.0.0.1:9222/json/version
```

返回JSON则成功。

### 步骤5: 通知我
完成后回复"Chrome已就绪"

---

## 注意事项

- 使用独立Profile `douyin_benchmark_v2`，不影响日常Chrome
- `--remote-allow-origins=http://127.0.0.1:9222` 是必要参数（非`*`）
- 登录态会保存在这个Profile中，后续可复用
- 不要关闭这个Chrome窗口

---

**等待Lan操作完成后继续执行DOM采集**
