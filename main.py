from job import Job

if __name__ == '__main__':
    create_dir_job = Job('create_dir')
    rename_dir_job = Job('rename_dir', dependencies=[create_dir_job])
    delete_dir_job = Job('delete_dir', dependencies=[create_dir_job, rename_dir_job])
    create_file_job = Job('create_file', dependencies=[create_dir_job])
