import random
import numpy as np

next_event = "arrival"
next_event_time = 0
next_arrival = 0
now = 0
end_time = 1000
stack_time = {0: 0}
stack_event = {0: "arrival"}
top = len(stack_event) - 1
lambS = 1
lambA = 0.8
previous_event_time = 0
system_size = 0
queue_size = 0


def expRVGenerator(para):
    a = 0
    b = 1
    U = random.uniform(a, b)
    x = -np.log(1 - U) / para
    result = a + (b - a) * x

    return result


def event_ID():
    if next_event == "arrival":
        return 0
    elif next_event == "service":
        return 1
    elif next_event == "departure":
        return 2


def stack_push(event, time):
    global top
    j = len(stack_event)
    top = len(stack_event) - 1

    for x in range(len(stack_time)):
        if stack_time[x] > time:
            j = x
            break

    for i in range(top + 1, -1, -1):
        if i <= j:
            break

        stack_time[i] = stack_time[i - 1]
        stack_event[i] = stack_event[i - 1]

    stack_time[j] = time
    stack_event[j] = event


def stack_pop():
    global top, next_event, next_event_time
    next_event = stack_event[0]
    next_event_time = stack_time[0]
    top = len(stack_event) - 1

    for i in range(0, top):
        stack_time[i] = stack_time[i + 1]
        stack_event[i] = stack_event[i + 1]

    stack_event.pop(top)
    stack_time.pop(top)


def arrival():
    global now, next_event, previous_event_time, next_arrival, queue_size
    now = next_event_time
    next_arrival = now + expRVGenerator(lambA)
    stack_push("arrival", next_arrival)
    if system_size == 0:
        next_event = "service"
    else:
        stack_pop()

    if next_event == "arrival":
        queue_size += 1

    statistics()
    previous_event_time = now


def service():
    global now, next_arrival, previous_event_time, system_size, queue_size
    now = next_event_time
    next_arrival = now + expRVGenerator(lambS)
    stack_push("departure", next_arrival)
    stack_pop()
    system_size += 1
    queue_size -= 1

    if next_event == "arrival":
        queue_size += 1

    statistics()
    previous_event_time = now


def departure():
    global now, next_event, previous_event_time, system_size, queue_size
    now = next_event_time
    system_size -= 1

    if queue_size > 0:
        next_event = "service"
    else:
        stack_pop()

    if next_event == "arrival":
        queue_size += 1

    statistics()
    previous_event_time = now


def statistics():
    pass


while now < end_time:
    print(stack_time)
    print(stack_event)
    if event_ID() == 0:
        arrival()
        continue
    elif event_ID() == 1:
        service()
        continue
    elif event_ID() == 2:
        departure()
        continue
