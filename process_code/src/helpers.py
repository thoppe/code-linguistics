import contextlib, tempfile, os

@contextlib.contextmanager
def temp_working_space():
    # when used a context manager, yields the tmp_directory
    tmp_dir = tempfile.mkdtemp()
    cmd_clean = "rm -rf {}".format(tmp_dir)

    try:
        yield tmp_dir
    finally:       
        os.system(cmd_clean)

def sqlite_chunked_itr(conn, cmd, block_size=100):
    cursor = conn.execute(cmd)
    while True:
        result = cursor.fetchmany(size=block_size)
        yield result
        if not result: break
