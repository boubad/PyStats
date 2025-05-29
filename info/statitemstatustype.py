from enum import IntEnum


class StatItemStatusType(IntEnum):
    ACTIVE = 0
    INACTIVE = 1
    OUTLIER = 2
    INFO = 4
    TRAIN = 8
    COMPUTED = 16
    CLUSTER = 32
    MISSING = 64
    TEST = 128
    UNSET = 256
    
