import datetime

from tools import tasks_tools as tt, return_save as rs

DATE_FORMAT: str = '%Y-%m-%d %H:%M:%S'

def main() -> None:
    completed_tasks: list[dict[str, str]] = rs.tasks_save('json_files/completed_tasks.json')
    deadline_tasks: list[dict[str, str]] = rs.tasks_save('json_files/deadline_tasks.json')

    while True:
        try:
            choice: int = int(input('Please enter an action to perform:\n'
                                    '1. Log A Completed Task\n'
                                    '2. Log A Deadline Task\n'
                                    '3. Show All The Completed Tasks\n'
                                    '4. Show Today Tasks\n'
                                    '5. Show Deadline Tasks\n'
                                    '6. Smart Summary Of Last Week\n'
                                    '7. Exit\n\n'))
            print()
        except ValueError as ve:
            print(f'\nError! {ve}\n')
        else:
            match choice:
                case 1 | 2:
                    task_name: str = input('Please enter a name of the task: ')
                    print()

                    if choice == 1:
                        dates: tuple[datetime.datetime, datetime.datetime] = tt.get_valid_dates('Enter start of the task: ', 'Enter end of the task: ')
                        if dates:
                            start, end = dates
                            completed_tasks: list[dict[str, str]] = tt.log_task(completed_tasks, task_name, start, end, is_deadline=False)
                    else:
                        dates: tuple[datetime.datetime, datetime.datetime] = tt.get_valid_dates('Enter start of the task: ', 'Enter deadline of the task: ')
                        if dates:
                            start, deadline = dates
                            deadline_tasks: list[dict[str, str]] = tt.log_task(deadline_tasks, task_name, start, deadline, is_deadline=True)
                case 3:
                    tt.show_completed_tasks(completed_tasks)
                case 4:
                    tt.show_today_tasks(completed_tasks)
                case 5:
                    tt.show_deadline_tasks(deadline_tasks)
                case 6:
                    tt.smart_summaries(completed_tasks)
                case 7:
                    print('Exiting the program...')
                    break
                case _:
                    print(f'\'{choice}\' is an unrecognizable value!\n')

if __name__ == '__main__':
    main()