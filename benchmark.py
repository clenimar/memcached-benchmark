import argparse
import time

# pylibmc (implemented in C)
import pylibmc
# python-memcached (implemented in Python)
import memcache


def run(client, target=1000000):
    """run benchmark against a memcached server."""
    # start timer
    starttime = time.time()
    # request count
    r = 0

    while r < target:
        # do request
        client.get('bench_key_53')
        r += 1

    endtime = time.time()
    print(starttime, endtime, r)

    # average RPS
    avg_rps = r / (endtime - starttime)

    return avg_rps


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("address", type=str, help="where's my memcached?")
    parser.add_argument("--target", default=1000000, type=int, help="how many requests to send")
    args = parser.parse_args()

    # start client and load memcached w/ 200 keys
    mc = pylibmc.Client([args.address])
    for n in range(200):
        mc.set('bench_key_%d' % n, 'bench_value_%d' % n)
    
    # run and print results
    print(run(mc, target=args.target))