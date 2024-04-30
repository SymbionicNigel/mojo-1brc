from time import time_function, sleep


fn runChallenge() capturing -> None:
    sleep(1)


fn main():
    var nanos = time_function[runChallenge]()
    print("Run Challenge took " + str(nanos / 1e9) + " seconds")
