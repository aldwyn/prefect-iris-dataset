from prefect import Flow 
from prefect.tasks.prefect import create_flow_run, wait_for_flow_run
from datetime import timedelta, datetime
from prefect.schedules import IntervalSchedule


schedule = IntervalSchedule(
    start_date=datetime.utcnow() + timedelta(seconds=1),
    interval=timedelta(minutes=1),
)

with Flow("main-scheduled-flow") as flow:
    # result = data_science_flow(upstream_tasks=[data_engineering_flow])
    flow_a = create_flow_run(flow_name="data-engineering", project_name='main', parameters={'test_data_ratio': 0.3})
    wait_for_flow_a = wait_for_flow_run(flow_a, raise_final_state=True)

    flow_b = create_flow_run(flow_name="data-science", project_name='main', parameters={'train_test_dict': wait_for_flow_a.result})
    wait_for_flow_b = wait_for_flow_run(flow_b, raise_final_state=True)

    flow_b.set_upstream(wait_for_flow_a)


if __name__ == '__main__':
    flow.run()
