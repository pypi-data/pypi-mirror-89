#!/usr/bin/env python3

import subprocess
import shlex
import sys
import time

def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor

spinner = spinning_cursor()

if __name__ == "__main__":
    try:
        with subprocess.Popen(shlex.split('docker run -it --rm -p 22 -p 6379:6379 -p 8183:8183 -p 17010:17010 -p 17011:17011 -p 11223:11223 --name zato registry.gitlab.com/zatosource/docker-registry/quickstart:3.2'), stdout=subprocess.PIPE) as proc:
            print('Starting up', flush=True)
            has_ended = False
            for line in proc.stdout:
                if not has_ended:
                    sys.stdout.write(next(spinner))
                    sys.stdout.flush()
                    time.sleep(0.1)
                    sys.stdout.write('\b')
                if line.startswith(b'Quickstart cluster'):
                    print('Cluster started', flush=True)
                    print('\rWeb admin password: ', end="", flush=True)
                    subprocess.run('''docker exec zato /bin/bash -c 'cat /opt/zato/web_admin_password' ''', shell=True, check=False)
                    has_ended = True
                    print('\rPress Ctrl+C to stop\r')
    except Exception as e:
        try:
            subprocess.run('docker rm -f zato', shell=True, check=False)
        except Exception as e:
            raise e
        raise e
