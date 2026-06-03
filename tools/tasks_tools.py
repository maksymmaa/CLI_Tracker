import datetime, json

from main import DATE_FORMAT


def log_task(tasks: list[dict], task_name: str, start: datetime.datetime, end_or_deadline: datetime.datetime, is_deadline: bool = False) -> list[dict]:
    if not task_name:
        return tasks

    entry: dict[str, str] = {
        'Name': task_name,
        'Start': start.strftime(DATE_FORMAT)
    }

    if is_deadline:
        entry['Deadline'] = end_or_deadline.strftime(DATE_FORMAT)
        entry['Time Left'] = str(end_or_deadline - datetime.datetime.now())
    else:
        entry['Finished'] = end_or_deadline.strftime(DATE_FORMAT)
        entry['Duration'] = str(end_or_deadline - start)

    tasks.append(entry)

    filename: str = 'json_files/deadline_tasks.json' if is_deadline else 'json_files/completed_tasks.json'
    save_to_file(tasks, filename)

    return tasks

def print_table(data: list[dict], headers: dict[str, str], title: str = "") -> None:
    if not data:
        print(f"{title}: no data to display\n")
        return

    width: int = 25

    header_line: str = " | ".join(f"{name:<{width}}" for name in headers.values())
    print(header_line)
    print("-" * len(header_line))

    for entry in data:
        row: str = " | ".join(f"{str(entry.get(key, 'N/A')):<{width}}" for key in headers.keys())
        print(row)

    print("-" * len(header_line) + "\n")

def show_completed_tasks(tasks: list[dict]) -> None:
    headers: dict[str, str] = {
        'Name': 'Task Name',
        'Start': 'Start Time',
        'Finished': 'Finished Time',
        'Duration': 'Duration'
    }
    print_table(tasks, headers, "All Completed Tasks")

def show_today_tasks(tasks: list[dict]) -> None:
    today: str = datetime.datetime.now().strftime('%Y-%m-%d')
    today_tasks: list[dict[str, str]] = [t for t in tasks if t.get('Start', '').startswith(today)]

    headers: dict[str, str] = {
        'Name': 'Task Name',
        'Start': 'Start Time',
        'Finished': 'Finished Time',
        'Duration': 'Duration'
    }
    print_table(today_tasks, headers, f"Tasks for {today}")

def format_timedelta(td: datetime.timedelta) -> str:
    days: int = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    res: str = ""
    if days > 0: res += f"{days}d "
    if hours > 0: res += f"{hours}h "
    res += f"{minutes}m"
    return res

def show_deadline_tasks(tasks: list[dict]) -> None:
    display_data: list[dict[str, str]] = []
    now: datetime.datetime = datetime.datetime.now()

    for t in tasks:
        deadline_dt: datetime.datetime = datetime.datetime.strptime(t['Deadline'], DATE_FORMAT)
        time_left: datetime.timedelta = deadline_dt - now

        temp_task: dict[str, str] = t.copy()
        temp_task['TimeLeft']: str = format_timedelta(time_left) if time_left.total_seconds() > 0 else "EXPIRED"
        display_data.append(temp_task)

    headers: dict[str, str] = {
        'Name': 'Task Name',
        'Start': 'Started',
        'Deadline': 'Deadline Time',
        'TimeLeft': 'Time Remaining'
    }
    print_table(display_data, headers, "Active Deadlines")

def get_valid_dates(prompt_start: str, prompt_end: str) -> tuple[datetime.datetime, datetime.datetime] | None:
    try:
        start_str: str = input(prompt_start)
        end_str: str = input(prompt_end)
        print()

        start_dt: datetime.datetime = datetime.datetime.strptime(start_str, DATE_FORMAT)
        end_dt: datetime.datetime = datetime.datetime.strptime(end_str, DATE_FORMAT)

        if end_dt < start_dt:
            print("Error: end/deadline time cannot be before start time!\n")
            return None

        return start_dt, end_dt
    except ValueError:
        print("Error: invalid date format! Use YYYY-MM-DD HH:MM:SS\n")
        return None

def smart_summaries(tasks: list[dict[str, str]]) -> None:
    if not tasks:
        print('There are no tasks yet!\n')
        return

    now: datetime.datetime = datetime.datetime.now()
    last_week: datetime.datetime = now - datetime.timedelta(days=7)
    last_week_tasks: list[dict[str, str]] = []
    last_week_days: dict[str, float] = dict.fromkeys(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 0)

    for t in tasks:
        if last_week <= datetime.datetime.strptime(t['Start'], DATE_FORMAT) < now:
            last_week_tasks.append(t)

    for t in last_week_tasks:
        parts: list[str] = t['Duration'].split(', ')
        if len(parts) == 2:
            days_str, time_str = parts
            days: int = int(days_str.split(' ')[0])
        else:
            days = 0
            time_str: str = parts[0]
        h, m, s = map(int, time_str.split(':'))
        last_week_days[datetime.datetime.strptime(t['Start'], DATE_FORMAT).strftime('%A')] += datetime.timedelta(days, h, m, s).total_seconds()

    max_value: float = 0
    max_day: str = 'N/A'

    for k, v in last_week_days.items():
        if v > max_value:
            max_value = v
            max_day = k

    print(f'The most productive day of the last week is: {max_day.upper()} with the productive time of: {max_value / 3600:.2f} hours\n')

def save_to_file(tasks: list[dict[str, str]], filename) -> None:
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(tasks, file, indent=4)
        print('Saved successfully!\n')
    except Exception as e:
        print(f'\nError! {e}\n')

def read_from_file(filename) -> str:
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data: str = json.load(file)
    except FileNotFoundError as fnfe:
        print(f'\nError! {fnfe}\n')

    return data