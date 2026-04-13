<div align="center">

# 📊 Performance Management

**Enterprise Task Intelligence System for ERPNext v16**

A production-ready Frappe app that brings structured task tracking, automated checklist generation, deadline enforcement, approval workflows, and team performance analytics — all from within your ERPNext workspace.

[![Frappe](https://img.shields.io/badge/Frappe-v16-blue?style=flat-square)](https://frappeframework.com)
[![ERPNext](https://img.shields.io/badge/ERPNext-v16-orange?style=flat-square)](https://erpnext.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Requirements](#requirements)
- [Installation](#installation)
- [DocTypes](#doctypes)
- [Automation & Scheduling](#automation--scheduling)
- [Reports](#reports)
- [Scoring System](#scoring-system)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

---

## Overview

**Performance Management** is a custom Frappe application built for ERPNext v16 that helps organizations track employee performance through structured task delegation, automated daily checklists, deadline management, and data-driven reporting.

The system is built around **Performance Tasks** — which can be manually assigned (Delegation), automatically generated from templates (Checklist), or defined for Compliance and Operational purposes.

---

## Key Features

| Feature | Description |
|---|---|
| 🗂 **Performance Tasks** | Structured task tracking with priority, status, approval, and scoring |
| 📋 **Checklist Templates** | Define recurring task sets with frequency (Daily, Weekly, Monthly, etc.) |
| ⏰ **Auto-Generation** | Scheduler creates tasks from templates every day at midnight |
| 📧 **Daily Email Reminders** | Automated HTML reminder emails to each employee at 8:00 AM daily |
| ⚠️ **Overdue Detection** | Hourly job marks tasks as overdue when their deadline day has passed |
| 🔁 **Extension Requests** | Employees can request deadline extensions; managers approve/reject |
| ✅ **Approval Workflow** | Tasks requiring approval go through a formal review process |
| 🏆 **Scoring Engine** | Automatic scoring based on completion timeliness and extensions |
| 📊 **6 Built-in Reports** | Team performance, compliance, trends, distribution, and more |
| 🧾 **Audit Logging** | All critical actions are tracked in `PM Audit Log` |

---

## Requirements

- **Frappe Framework** v16
- **ERPNext** v16
- **Python** 3.10+
- **MariaDB** 10.6+
- **Redis** (cache on port 13000, queue on port 11000)
- An active Frappe bench setup

---

## Installation

### Step 1 — Get the App

```bash
# Navigate to your bench directory
cd /home/frappe/frappe-bench

# Get the app from GitHub
bench get-app https://github.com/your-org/performance_management

# Or if using a local path
bench get-app /path/to/performance_management
```

### Step 2 — Install on Your Site

```bash
bench --site your-site.local install-app performance_management
```

### Step 3 — Run Migrations

```bash
bench --site your-site.local migrate
```

### Step 4 — Start Bench

```bash
bench start
```

The **Performance Management** Workspace will appear on the ERPNext desk automatically after installation.

---

## DocTypes

### 1. `Performance Task` — `PM-TASK-#####`

The core document. Represents any unit of work assigned to an employee.

| Field | Type | Description |
|---|---|---|
| `task_title` | Data | Task name (required) |
| `department` | Link | Department |
| `assigned_to` | Link → User | Responsible employee |
| `assigned_by` | Link → User | Manager who assigned |
| `task_type` | Select | `Delegation`, `Checklist`, `Compliance`, `Operational` |
| `frequency` | Select | `Daily`, `Weekly`, `Monthly`, etc. (copied from template) |
| `status` | Select | `Draft → Pending → In Progress → Pending Approval → Approved → Cancelled` |
| `priority` | Select | `Low`, `Medium`, `High`, `Critical` |
| `deadline` | Datetime | Task deadline (end-of-day for checklist tasks) |
| `completion_date` | Datetime | Auto-set on completion |
| `requires_approval` | Check | If manager sign-off is needed |
| `score` | Float | Auto-calculated (starts at 100) |
| `is_overdue` | Check | Set automatically by hourly scheduler |
| `extension_count` | Int | Number of extensions granted |
| `checklist_template` | Link | Source template for auto-generated tasks |

---

### 2. `Checklist Template` — `PM-CL-#####`

Defines a reusable set of tasks auto-generated on a schedule.

| Field | Type | Description |
|---|---|---|
| `template_name` | Data | Template name (required) |
| `department` | Link | Department |
| `task_type` | Select | `Checklist`, `Compliance`, `Operational` |
| `default_priority` | Select | Priority applied to all generated tasks |
| `active` | Check | Enable/disable this template |
| `frequency` | Select | When to generate tasks (required) |
| `assigned_to` | Link → User | Default assignee |
| `items` | Table | List of `Checklist Template Item` rows |

#### Frequency Schedule

| Frequency | Runs On |
|---|---|
| Daily | Every day at midnight |
| Weekly | Every **Monday** |
| Monthly | **1st** of every month |
| Quarterly | **1st** of Jan, Apr, Jul, Oct |
| Half-Yearly | **1st** of Jan, Jul |
| Yearly | **1st** of Jan |

---

### 3. `Checklist Template Item`

Child table of `Checklist Template`. Each row becomes one `Performance Task`.

| Field | Description |
|---|---|
| `item_title` | The task name |
| `description` | Optional description |
| `is_mandatory` | Marks item as mandatory |

---

### 4. `Task Extension Request` — `PM-EXT-#####`

Formal process for employees to request a deadline extension.

| Field | Description |
|---|---|
| `task` | Performance Task to extend |
| `requested_by` | Employee requesting |
| `current_deadline` | Original deadline |
| `requested_deadline` | Proposed new deadline (required) |
| `reason` | Justification (required) |
| `approval_status` | `Pending` → `Approved` / `Rejected` |
| `approved_by` | Manager who acted on the request |
| `rejection_reason` | Reason if rejected |

---

### 5. `PM Audit Log`

System-maintained audit trail. Automatically records all critical state changes across the app.

---

## Automation & Scheduling

Three automated jobs run without any manual intervention:

### 🕛 Midnight — `create_daily_checklists`

```
hooks.py → scheduler_events["daily"]
```

Fetches all active Checklist Templates and generates `Performance Tasks` based on their frequency.

- **Anti-duplicate:** Skips tasks that already exist for the same date
- **Deadline:** Set to **end-of-day** (`23:59:59`) — tasks are never immediately overdue
- **Frequency:** Copied from template to each generated task

### 🕗 8:00 AM Daily — `send_daily_reminders`

```
hooks.py → scheduler_events["cron"]["0 8 * * *"]
```

Sends a personalized HTML email to each user listing their open/overdue tasks.

**Sample Email:**

```
Hi Somil,

Here are your open tasks for today.

| Task ID      | Title              | Deadline             |
|--------------|--------------------|----------------------|
| PM-TASK-0114 | Daily Sales Report | 2026-04-13 23:59:59  |
| PM-TASK-0098 | Client Follow-up   | 2026-04-12 ⚠ OVERDUE |

Please log in to your Workspace and update your task statuses.
```

> **Why 8 AM?** This ensures the midnight checklist creation job has already run and all today's tasks are present in the database before the reminder fires.

### 🕐 Every Hour — `mark_overdue_tasks`

```
hooks.py → scheduler_events["hourly"]
```

Marks tasks as overdue if their **deadline date has fully passed**.

```sql
-- Only past-day tasks are marked overdue, never today's tasks
DATE(deadline) < CURDATE()
```

---

## Reports

Navigate to **Workspace → Performance Management → Reports**.

| Report | Description |
|---|---|
| **Team Performance Report** | Per-employee, per-task-type analytics with avg score and completion rate |
| **User Performance** | Individual employee performance breakdown |
| **Checklist Compliance** | How well employees complete their checklist tasks |
| **Overdue Task Trend** | Historical view of overdue task patterns |
| **Task Completion Trend** | Completion patterns over time |
| **Task Status Distribution** | Snapshot of all tasks grouped by status |

### Team Performance Report — Filters

| Filter | Description |
|---|---|
| Department | Filter by department |
| Employee | Filter by specific user |
| Task Type | `Delegation`, `Checklist`, `Compliance`, `Operational` |
| Creation Date | Date range |

---

## Scoring System

Tasks are automatically scored upon approval via the `on_update` doc event.

**Formula (base 100):**

```
score = 100
score -= extension_count × 5         # -5 per extension granted
score -= min(delay_days × 10, 50)    # -10 per day late, max -50
final_score = max(0, score)          # floor at 0
```

**Examples:**

| Scenario | Score |
|---|---|
| Approved on time, no extensions | 100 |
| Approved on time, 1 extension | 95 |
| Approved 2 days late, no extensions | 80 |
| Approved 5+ days late | 50 or less |

---

## Configuration

No manual configuration is needed. The `after_install` hook sets up all required defaults.

### Manual Execution (for testing)

```bash
# Manually trigger checklist creation
bench --site your-site.local execute \
  performance_management.performance_management.services.checklist_service.create_daily_checklists

# Manually send reminder emails
bench --site your-site.local execute \
  performance_management.performance_management.utils.automation.send_daily_reminders

# Manually run the overdue marker
bench --site your-site.local execute \
  performance_management.performance_management.utils.automation.mark_overdue_tasks
```

---

## Troubleshooting

### `bench start` fails — "Address already in use" on port 11000 or 13000

Redis was started manually and is still running. Kill those processes first:

```bash
sudo fuser -k 11000/tcp 13000/tcp
bench start
```

### Tasks created as overdue immediately

Ensure you are on the latest version of this app. This was fixed: checklist tasks now get a deadline of `23:59:59` and the overdue marker uses `DATE(deadline) < CURDATE()`.

### Reminder emails not sending

1. Check bench is running: `bench start`
2. Go to ERPNext → Email Queue and look for failed/pending items
3. Verify outbound email settings under **Setup → Email Domain**
4. Check logs: `bench --site your-site.local error-log`

### No tasks generated from a Checklist Template

- Ensure the template has `Active = 1`
- Ensure `Assigned To` is set
- Ensure the template has at least one item in the `Items` table
- Verify the `Frequency` matches today's schedule (e.g., "Weekly" only runs on Monday)

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

<div align="center">
Built with ❤️ using <a href="https://frappeframework.com">Frappe Framework</a>
</div>
