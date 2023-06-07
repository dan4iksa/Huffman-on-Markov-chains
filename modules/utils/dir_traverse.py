import os


def traverse_directory(input_path, output_path, matrix, file_operation, buffer=None):
    src_size = 0
    dest_size = 0

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for dir_path, dir_names, filenames in os.walk(input_path):
        if src_size != 0:
            output_path = os.path.join(output_path, os.path.basename(dir_path))

        for dir_name in dir_names:
            path_to_dir = os.path.join(output_path, dir_name)
            if not os.path.exists(path_to_dir):
                os.makedirs(path_to_dir)

        for filename in filenames:
            scr_path = os.path.join(dir_path, filename)
            dest_path = os.path.join(output_path, filename)

            if buffer is not None:
                file_operation(
                    scr_path,
                    dest_path,
                    matrix,
                    buffer
                )
            else:
                file_operation(
                    scr_path,
                    dest_path,
                    matrix,
                )

            src_size += os.path.getsize(scr_path)
            dest_size += os.path.getsize(dest_path)

    return src_size, dest_size
