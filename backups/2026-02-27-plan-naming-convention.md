# Plan 保存规范：存放于项目目录，日期命名

## Context

用户要求：每个项目的 plan 都保存在该项目自身的 `plans/` 目录下，不放在 Claude 系统目录（`~/.claude/`）中。命名格式为日期前缀。

当前项目路径：`/home/admin/project/`

## 实施步骤

### Step 1: 更新 MEMORY.md（持久化偏好）

创建 `/home/admin/.claude/projects/-home-admin-project/memory/MEMORY.md`，写入：

```markdown
## Plan 归档规范
- 每次 plan 完成后，将 plan 内容保存到 **项目根目录** 下的 `plans/YYYY-MM-DD-<topic>.md`
- 当前项目：`/home/admin/project/plans/`
- 日期格式：YYYY-MM-DD（计划制定当天）
- topic：2-4 个英文单词，连字符分隔，描述本次 plan 主题
- 不放在 ~/.claude/ 任何子目录下
```

### Step 2: 创建项目 plans 目录

```bash
mkdir -p /home/admin/project/plans
```

### Step 3: 保存本次 plan

将当前 plan 文件内容保存为项目内第一份归档：

```
/home/admin/project/plans/2026-02-27-plan-naming-convention.md
```

## 关键文件

| 文件 | 变更 |
|------|------|
| `/home/admin/.claude/projects/-home-admin-project/memory/MEMORY.md` | 新建，写入 plan 归档规范 |
| `/home/admin/project/plans/` | 新建目录 |
| `/home/admin/project/plans/2026-02-27-plan-naming-convention.md` | 本次 plan 归档 |

## 验证

- `ls /home/admin/project/plans/` → 显示 `2026-02-27-plan-naming-convention.md`
- `cat /home/admin/.claude/projects/-home-admin-project/memory/MEMORY.md` → 包含 plan 归档规范
