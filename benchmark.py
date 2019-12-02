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
    delta = (endtime - starttime)

    # average RPS
    avg_rps = r / delta

    return avg_rps, delta


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("addresses", type=str, help="where's my memcached?")
    parser.add_argument("--target", default=1000000, type=int, help="how many requests to send")
    args = parser.parse_args()
    
    addresses = args.addresses.split(',')
    print(addresses)
    # start client and load memcached w/ 200 keys
    mc = pylibmc.Client(addresses, binary=True)
    for n in range(200):
        mc.set('bench_key_%d' % n, 'bench_value_%d' % n)

    # run and print results
    result = run(mc, target=args.target)
    print("exp. time: %f seconds\navg. rps: %f" % (result[1], result[0]))

