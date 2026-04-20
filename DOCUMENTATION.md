# Performance Management - Full Detailed Documentation

## 1. Overview
The **Performance Management** app is an enterprise task intelligence system for ERPNext v16. It tracks employee performance through structured task delegation, automated daily checklists, deadline management, and data-driven reporting.

---

## 2. System Flow
1. **Task Creation**: Tasks are created either manually (Delegations, Operational) or automatically generated from **Checklist Templates** by the system scheduler at midnight.
2. **Assignment & Notification**: Upon creation, the assignee is notified via email.
3. **Execution**: The employee starts the task from their workspace, marking it as *In Progress*.
4. **Approval Workflow**: Depending on the priority or task type, a task may require manager approval. The employee submits the task for approval, the manager reviews and provides a decision.
5. **Scoring**: Task scores automatically drop if deadline extensions are granted or the task is completed late.
6. **Monitoring**: Admins and Users track performance via custom Dashboards and built-in Reports.

---

## 3. DocTypes and Forms

### 3.1 Performance Task (`PM-TASK-#####`)
The core operational document. Represents any unit of work.
*   **Fields**:
    *   `Task Title`: Name of the task.
    *   `Task Type`: Delegation, Checklist, Compliance, Operational.
    *   `Status`: Draft → Pending → In Progress → Pending Approval → Approved → Cancelled / Reopened.
    *   `Priority`: Low, Medium, High, Critical. High and Critical tasks automatically check `Requires Approval`.
    *   `Assignee` / `Assigned By`: The user responsible and the manager delegating.
    *   `Deadline` / `Completion Date`: Used to track tardiness and calculate the score.
    *   `Score`: Out of 100, drops on lateness or extensions.
*   **Form Logic & Restrictions**:
    *   If Priority is set to "High", "Critical", or Type is "Compliance", the `Requires Approval` checkbox is checked automatically.
    *   Tasks overdue are indicated via an **Overdue banner** indicator directly on the form dashboard.

### 3.2 Checklist Template (`PM-CL-#####`)
Defines recurring tasks.
*   **Fields**:
    *   `Template Name`, `Task Type`, `Default Priority`.
    *   `Frequency`: Daily, Weekly, Monthly, Quarterly, Half-Yearly, Yearly.
    *   `Active`: Toggles the auto-generation.
    *   `Items` (Child Table): Contains the list of tasks to generate.

### 3.3 Task Extension Request (`PM-EXT-#####`)
Process for an employee to request more time to complete a task.
*   **Fields**:
    *   `Task`, `Requested By`, `Current Deadline`, `Requested Deadline`, `Reason`.
    *   `Approval Status`: Pending, Approved, Rejected.
    *   **Logic**: If approved, updates the original Performance Task's deadline and increments its `Extension Count`, causing a small score penalty.

### 3.4 PM Audit Log
System-maintained doctype capturing state changes for security and auditing purposes. Stores timestamp, user, action, and details.

---

## 4. Workflows (Form-driven Actions)

The app utilizes custom buttons injected directly into the `Performance Task` desk form to drive the state machine:
*   **Start Task**: Changes status from *Pending* to *In Progress*.
*   **Submit for Approval**: If `Requires Approval` is checked, the employee uses this to change status to *Pending Approval*. This fires an email to the assigner.
*   **Mark Complete**: If no approval is required, the assignee can directly mark it as *Approved*.
*   **Approve / Reject**: Managers see these buttons on *Pending Approval* tasks. Rejecting moves the task to *Reopened* and prompts for a rejection reason.
*   **Restart Task**: Assignees can restart a *Reopened* task back to *In Progress*.
*   **Request Extension**: Available for "Delegation" tasks to quickly create a `Task Extension Request`.

---

## 5. Dashboards

The app brings two rich Custom HTML Block dashboards configured dynamically via scripts.
*   **PM User Dashboard**:
    *   Key Performance Indicators (KPIs): Total To-do, Pending Approvals, Awaiting Extensions.
    *   Charts: My Task Completion Trend (7 days), Task Status Distribution (Donut chart).
    *   Global Leaderboard listing top performers in real-time.
*   **PM Admin Dashboard**:
    *   Company-wide task KPIs.
    *   Charts: Global Task Completion Trend, Status Distribution, Checklist Compliance (Tasks completed on time vs late), Overdue Task Trend.
    *   User Performance Overview.

---

## 6. Automation & Scheduling

All automation routines are registered via `hooks.py`:
1.  **Midnight Routine** (`daily`): Generates new `Performance Tasks` from all active `Checklist Templates` matching today's frequency criteria. Sets deadline to end-of-day.
2.  **8:00 AM Routine** (`cron`): Sends HTML email reminders to each user detailing all of their open or overdue tasks.
3.  **Hourly Routine** (`hourly`): Scans for open tasks where the `deadline` is strictly strictly lesser than the current system time/date, setting `Is Overdue`.

---

## 7. Email Notifications

Email triggers are built directly into the `Performance Task` controller:
1.  **Assignment Email**: Sent immediately when a task is created & assigned to someone.
2.  **Submission Email**: Sent to `Assigned By` when a task changes to *Pending Approval*.
3.  **Decision Email**: Sent to `Assignee` when the manager clicks Approve or Reject.
4.  **Daily Morning Digest**: Sent via the 8AM `send_daily_reminders` automation.

---

## 8. Built-in Reports
Located in standard Desk → Workspace → Performance Management → Reports.
1.  **Team Performance Report**: Aggregates avg scores and completion rates per department/employee.
2.  **User Performance**: Direct dive into a single user's metric.
3.  **Checklist Compliance**: Checks if daily templates are actually fulfilled.
4.  **Overdue Task Trend**: Tracks organizational backlog.
5.  **Task Completion Trend**: Velocity of task closures over time.
6.  **Task Status Distribution**: Global perspective on what percentage of tasks are pending vs completed.

---

## 9. Scoring Calculation Engine
Executed safely within the `on_update` doc event.
*   All tasks start at a **Base Score of 100**.
*   **-20 Points** per each extension request granted.
*   **-10 Points** per day late after the deadline, capped at a maximum late penalty of 50.
*   If a task is *Rejected* by a manager and *Reopened*, an immediate **-20 Points** penalty applies to current score.
*   The final score is bounded to a minimum of 0.
