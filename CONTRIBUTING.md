# 贡献指北

## 项目版本管理

我们使用[语义化版本](https://semver.org/lang/zh-CN/)进行版本管理。
任何对代码库的更改都不应使用现有版本发布。

## 提交信息格式

提交信息应遵循 [PJ568 提交说明规范](https://github.com/PJ-568/git-commit-regulation)。

## 客户端

### 客户端代码格式

1. 使用两个空格缩进。

### 引入图标

1. 在 [tabler icons](https://tabler.io/icons) 中选择合适的图标时，请使用 `.svg` 格式。
2. 将 `svg` 代码转为 CSS 中的 `background-image:url(data:..)` 格式并存入 `client/css/icon.css` 文件夹中。
3. 在 HTML 中引入。

## 服务端

### 范围

项目当前定义的范围如下：

- `智能体（agent）`：智能体核心实现
- `核心（core）`：基础数据结构与框架
- `命令行（cli）`：命令行接口
- `网页（web）`：网页接口
- `工具（agent/tools）`：智能体工具实现

### 服务端开发环境配置

1. 安装 cargo 和 Rust。
2. 配置 cargo 镜像源（可选）。
3. VSCode 配置：

   - 安装 rust-analyzer 扩展。

### 服务端测试

- 运行 `cargo check` 命令，确保没有代码格式错误。
- 运行 `cargo test` 命令，确保所有测试用例通过。
- 运行 `cargo run` 命令以测试命令行交互模式：
- 运行 `cargo run --serve` 命令，可通过以下命令测试服务模式：

  ```bash
  curl -v -X POST -H "Authorization: YAA-API-KEY yaa" -H "Content-Type: application/json" -d '{ "id": "12345", "title": "测试会话", "startTime": "2025-04-07T12:00:00Z", "character": "测试角色", "status": "in-progress", "messages": [{ "role": "user", "content": "测试消息" }] }' http://127.0.0.1:12345
  ```

### 服务端编译

- 运行 `cargo build` 命令以编译 Debug 版本的二进制文件。
- 运行 `cargo build --release` 命令以编译更小更快的发行版本的二进制文件。

## 提交更改

1. Fork 此仓库，在您的仓库新建一个基于此仓库默认分支（branch）的分支。
2. 在该新建分支对项目进行更改，确保语法不存在问题（运行 `cargo check` 不报错）后应用更改您的仓库。
3. 向我们的仓库提交拉取请求。请确保您遵循了上述说明。
4. 我们将定期审查拉取请求，并告知您我们的问题以及在合并您的拉取请求之前需要进行的任何更改。
5. 我们希望您在 15 日内作出回应，之后如果没有显示活动，您的拉取请求可能会被关闭。

### 注意事项

- 单次 Pull Request 不应提交过多修改，请确保每次提交都针对特定的功能且务必说明本次改动的具体目的，例如：修复某 bug 、优化某方法 等，方便进行 Code Review；
- 对于 bug 的修复，应该将本次 Pull Request 和相对应 bug 的 issue 关联起来，让别人知道该问题已经被修复；
- 对于较大的新功能，你需要先提交 Issues，例如 "添加 XXX 功能"，确认该功能有被添加的必要后，再开始工作；
- 对于一些主观的样式、交互逻辑调整：如颜色、图标的使用，某些预设配置的增减修改等，一般不予通过。但可以在 Discussions 中进行讨论；
- 其他如简单的代码优化、文档修正等，只要修改合理都会被接受。
