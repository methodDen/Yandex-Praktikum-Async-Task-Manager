import tasks
from job import Job
from scheduler import Scheduler
from utils import (FILE_NAME_FOR_JOB_FLOW_1, FILE_NAME_FOR_JOB_FLOW_2, FILE_NAME_FOR_JOB_FLOW_3)

# flow 1 : create_dir_job => create_file_job => write_to_file_job => read_from_file_job
# flow 2 : create_dir_job => create_file_job => delete_file_job => delete_dir_job
# flow 3: get_swapi_data, create_file_job (random time + retries)


if __name__ == '__main__':
    # flow 1
    create_dirs_job = Job(fn=tasks.create_dirs_job, max_working_time=5,)
    create_file_job_1 = Job(
        fn=tasks.create_file_job,
        args=(FILE_NAME_FOR_JOB_FLOW_1,),
        max_working_time=5, max_tries=4,
        dependencies=[
            create_dirs_job.id_,
        ])

    write_to_file_job = Job(
        fn=tasks.write_to_file_job,
        args=(FILE_NAME_FOR_JOB_FLOW_1,),
        max_working_time=5,
        dependencies=[
            create_file_job_1.id_,
            create_dirs_job.id_,
        ])

    read_from_file_job = Job(
        fn=tasks.read_from_file_job,
        args=(FILE_NAME_FOR_JOB_FLOW_1,),
        max_working_time=5,
        dependencies=[
            create_file_job_1.id_,
        ])

    # flow 2
    create_file_job_2 = Job(
        fn=tasks.create_file_job,
        args=(FILE_NAME_FOR_JOB_FLOW_2,),
        max_working_time=5,
        dependencies=[
            create_dirs_job.id_,
        ])
    delete_file_job = Job(
        fn=tasks.delete_file_job,
        args=(FILE_NAME_FOR_JOB_FLOW_2,),
        max_working_time=5,
        dependencies=[
            create_file_job_2.id_,
        ])
    delete_dirs_job = Job(
        fn=tasks.delete_dir_job,
        max_working_time=5,
        dependencies=[
            delete_file_job.id_,
        ])

    # flow 3
    get_swapi_data_job = Job(
        fn=tasks.get_swapi_data_job,
        max_working_time=5,
        start_at='2023-08-28 17:35:32',
    )
    create_file_job_3 = Job(
        fn=tasks.create_file_job,
        args=(FILE_NAME_FOR_JOB_FLOW_3,),
        max_working_time=1,
        max_tries=3
    )

    scheduler = Scheduler(pool_size=5)
    try:
        scheduler.run_until_complete(
            [
                create_dirs_job,
                create_file_job_1,
                write_to_file_job,
                read_from_file_job,
                create_file_job_2,
                delete_file_job,
                delete_dirs_job,
                get_swapi_data_job,
                create_file_job_3,
            ]
        )
    except KeyboardInterrupt:
        scheduler.stop()

