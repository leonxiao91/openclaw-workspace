# GitHub Deploy Skill

自动将代码推送到 GitHub 仓库。

## 配置

- **仓库地址:** https://github.com/leonxiao91/openclaw-workspace
- **分支:** main

## 使用方法

### 部署当前项目

```bash
# 在项目目录执行
github-deploy "提交信息"
```

### 示例

```bash
github-deploy "Add new feature"
```

## 工作流程

1. 确保在 git 仓库中
2. 添加所有更改 `git add -A`
3. 提交代码 `git commit -m "提交信息"`
4. 推送到 GitHub `git push`

## 注意

- 需要先配置 git 用户信息（如果尚未配置）
- 确保有仓库推送权限
